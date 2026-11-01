#!/usr/bin/env python3
"""
2D Gravitational N-Body Simulation

Extension of gas_simulation.py: particles of equal mass attract each other via
Newtonian gravity.  They still bounce elastically off the walls of the box.

Physics (m configurable, kB = 1):
  F_ij = G m² (r_j − r_i) / (|r_ij|² + ε²)^(3/2)   [softened to prevent singularities]
  a_i  = G m  Σ_{j≠i} (r_j − r_i) / (|r_ij|² + ε²)^(3/2)
  KE   = Σ  ½ m |v_i|²
  PE   = Σ_{i<j}  −G m² / sqrt(|r_ij|² + ε²)

Integration: Velocity Verlet with elastic wall reflections, 4 substeps per frame.
Force computation is fully vectorised with NumPy (O(N²)).
"""

import sys
import math
import random
import numpy as np
import pygame

# ── Window / layout ────────────────────────────────────────────────────────────
WIN_W, WIN_H = 1380, 740
BOX_MARGIN   = 20
BOX_SIZE     = WIN_H - 2 * BOX_MARGIN        # 700 px square
PANEL_X      = BOX_SIZE + 2 * BOX_MARGIN + 10
PANEL_W      = WIN_W - PANEL_X - 10

# ── Palette ────────────────────────────────────────────────────────────────────
BG       = (15,  15,  20)
BOX_BG   = (22,  22,  30)
BOX_LINE = (200, 200, 200)
WHITE    = (255, 255, 255)
GRAY     = (160, 160, 160)
DGRAY    = ( 55,  55,  68)
YELLOW   = (255, 215,   0)
ORANGE   = (255, 140,   0)
GREEN    = ( 80, 200, 120)
CYAN     = ( 80, 200, 220)
RED      = (220,  80,  80)


def speed_color(t: float) -> tuple:
    """Blue (slow) → green → red (fast), t ∈ [0, 1]."""
    if t < 0.5:
        s = t * 2
        return (int(20 + 80*s), int(100 + 80*s), int(230 - 130*s))
    s = (t - 0.5) * 2
    return (int(100 + 120*s), int(180 - 100*s), int(100 - 80*s))


# ── Slider widget ──────────────────────────────────────────────────────────────
class Slider:
    TRACK_H = 6
    KNOB_R  = 8

    def __init__(self, x, y, w, label, lo, hi, value, integer=False, fmt=None):
        self.x, self.y, self.w = x, y, w
        self.label    = label
        self.lo, self.hi = lo, hi
        self.value    = float(value)
        self.integer  = integer
        self.fmt      = fmt or ("{:d}" if integer else "{:.2f}")
        self.dragging = False

    @property
    def _frac(self):
        return (self.value - self.lo) / (self.hi - self.lo)

    @property
    def _knob_x(self):
        return self.x + int(self._frac * self.w)

    def draw(self, surf, font_sm):
        val_str = self.fmt.format(int(self.value) if self.integer else self.value)
        surf.blit(font_sm.render(f"{self.label}: {val_str}", True, GRAY),
                  (self.x, self.y - 17))
        cy = self.y + self.KNOB_R
        pygame.draw.rect(surf, DGRAY,
                         (self.x, cy - self.TRACK_H // 2, self.w, self.TRACK_H),
                         border_radius=3)
        fw = max(int(self._frac * self.w), 0)
        if fw:
            pygame.draw.rect(surf, CYAN,
                             (self.x, cy - self.TRACK_H // 2, fw, self.TRACK_H),
                             border_radius=3)
        kx = self._knob_x
        pygame.draw.circle(surf, DGRAY, (kx, cy), self.KNOB_R)
        pygame.draw.circle(surf, CYAN,  (kx, cy), self.KNOB_R - 2)
        pygame.draw.circle(surf, WHITE, (kx, cy), self.KNOB_R, 1)

    def handle_mousedown(self, pos):
        kx = self._knob_x
        cy = self.y + self.KNOB_R
        if math.hypot(pos[0] - kx, pos[1] - cy) <= self.KNOB_R + 6:
            self.dragging = True

    def handle_mousemove(self, pos):
        if self.dragging:
            frac = max(0.0, min(1.0, (pos[0] - self.x) / self.w))
            raw  = self.lo + frac * (self.hi - self.lo)
            self.value = float(round(raw)) if self.integer else raw

    def handle_mouseup(self):
        self.dragging = False


# ── Button widget ──────────────────────────────────────────────────────────────
class Button:
    def __init__(self, x, y, w, h, label):
        self.rect    = pygame.Rect(x, y, w, h)
        self.label   = label
        self.hovered = False

    def draw(self, surf, font):
        bg = (75, 75, 95) if self.hovered else (45, 45, 60)
        pygame.draw.rect(surf, bg,   self.rect, border_radius=4)
        pygame.draw.rect(surf, GRAY, self.rect, 1, border_radius=4)
        t = font.render(self.label, True, WHITE)
        surf.blit(t, t.get_rect(center=self.rect.center))

    def clicked(self, pos) -> bool:
        return self.rect.collidepoint(pos)

    def update_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)


# ── N-body state ───────────────────────────────────────────────────────────────
class GravityState:
    """Holds particle positions/velocities and integrates the equations of motion."""

    def __init__(self, pos: np.ndarray, vel: np.ndarray,
                 m: float, G: float, soft: float):
        self.pos  = pos.astype(np.float64)   # (N, 2)
        self.vel  = vel.astype(np.float64)   # (N, 2)
        self.m    = m
        self.G    = G
        self.soft = soft
        self.acc  = self._compute_acc()

    # ── force kernel ───────────────────────────────────────────────
    def _compute_acc(self) -> np.ndarray:
        """
        Softened pairwise gravity, fully vectorised.
          diff[i,j] = pos[j] − pos[i]   →   attraction is towards j
          a_i = G m Σ_{j≠i} diff[i,j] / (|diff|² + ε²)^(3/2)
        """
        # (N, N, 2):  diff[i,j] = pos[j] - pos[i]
        diff = self.pos[np.newaxis, :, :] - self.pos[:, np.newaxis, :]
        r2   = np.einsum('ijk,ijk->ij', diff, diff) + self.soft ** 2   # (N, N)
        r3   = r2 ** 1.5
        np.fill_diagonal(r3, np.inf)   # no self-force
        return self.G * self.m * np.einsum('ij,ijk->ik', 1.0 / r3, diff)  # (N, 2)

    # ── wall reflections ───────────────────────────────────────────
    def _reflect(self, vel: np.ndarray):
        """Elastic wall reflections; modifies pos in-place and the given vel array."""
        lo_x = self.pos[:, 0] < 0
        hi_x = self.pos[:, 0] > BOX_SIZE
        lo_y = self.pos[:, 1] < 0
        hi_y = self.pos[:, 1] > BOX_SIZE

        self.pos[lo_x, 0]  = -self.pos[lo_x, 0]
        vel[lo_x, 0]       =  np.abs(vel[lo_x, 0])

        self.pos[hi_x, 0]  = 2 * BOX_SIZE - self.pos[hi_x, 0]
        vel[hi_x, 0]       = -np.abs(vel[hi_x, 0])

        self.pos[lo_y, 1]  = -self.pos[lo_y, 1]
        vel[lo_y, 1]       =  np.abs(vel[lo_y, 1])

        self.pos[hi_y, 1]  = 2 * BOX_SIZE - self.pos[hi_y, 1]
        vel[hi_y, 1]       = -np.abs(vel[hi_y, 1])

    # ── integrator ─────────────────────────────────────────────────
    def step(self, dt: float, n_sub: int = 4):
        """Velocity Verlet with n_sub substeps per call."""
        sub = dt / n_sub
        for _ in range(n_sub):
            # drift
            self.pos  += self.vel * sub + 0.5 * self.acc * sub ** 2
            vel_half   = self.vel + 0.5 * self.acc * sub
            # wall bounce at mid-step, then recompute forces at new positions
            self._reflect(vel_half)
            self.acc   = self._compute_acc()
            # second half-kick
            self.vel   = vel_half + 0.5 * self.acc * sub

    # ── energy ─────────────────────────────────────────────────────
    def energy(self) -> tuple[float, float, float]:
        v2 = np.einsum('ij,ij->i', self.vel, self.vel)
        KE = 0.5 * self.m * v2.sum()

        diff = self.pos[np.newaxis, :, :] - self.pos[:, np.newaxis, :]
        r2   = np.einsum('ijk,ijk->ij', diff, diff) + self.soft ** 2
        r    = np.sqrt(r2)
        np.fill_diagonal(r, np.inf)
        PE   = -0.5 * self.G * self.m ** 2 * np.sum(1.0 / r)   # ½ avoids double-counting

        return float(KE), float(PE), float(KE + PE)


# ── Main simulation ────────────────────────────────────────────────────────────
class Simulation:

    _SL_STEP = 44          # vertical spacing between slider rows (px)
    _N_SLIDERS = 10

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("2D Gravitational N-Body Simulation")
        self.clock    = pygame.time.Clock()
        self.font_lg  = pygame.font.SysFont("monospace", 20, bold=True)
        self.font_med = pygame.font.SysFont("monospace", 15)
        self.font_sm  = pygame.font.SysFont("monospace", 13)

        # ── Sliders ─────────────────────────────────────────────
        sx, sw = PANEL_X, PANEL_W - 10
        s0     = 42        # y of first slider

        self.sl_n    = Slider(sx, s0 + 0*self._SL_STEP, sw,
                              "N particles",    10,   200,   60,   integer=True)
        self.sl_vmin = Slider(sx, s0 + 1*self._SL_STEP, sw,
                              "Min speed",       0,   300,   10)
        self.sl_vmax = Slider(sx, s0 + 2*self._SL_STEP, sw,
                              "Max speed",       1,   500,  100)
        self.sl_mass = Slider(sx, s0 + 3*self._SL_STEP, sw,
                              "Mass m",        0.1,   100,    1.0)
        self.sl_G    = Slider(sx, s0 + 4*self._SL_STEP, sw,
                              "G (×1000)",       1,  5000,  500,  fmt="{:.0f}")
        self.sl_soft = Slider(sx, s0 + 5*self._SL_STEP, sw,
                              "Softening ε",     1,   100,   15)
        self.sl_xmin = Slider(sx, s0 + 6*self._SL_STEP, sw,
                              "X min (0–1)",   0.0,   1.0,  0.0)
        self.sl_xmax = Slider(sx, s0 + 7*self._SL_STEP, sw,
                              "X max (0–1)",   0.0,   1.0,  1.0)
        self.sl_ymin = Slider(sx, s0 + 8*self._SL_STEP, sw,
                              "Y min (0–1)",   0.0,   1.0,  0.0)
        self.sl_ymax = Slider(sx, s0 + 9*self._SL_STEP, sw,
                              "Y max (0–1)",   0.0,   1.0,  1.0)

        self.sliders = [
            self.sl_n, self.sl_vmin, self.sl_vmax,
            self.sl_mass, self.sl_G, self.sl_soft,
            self.sl_xmin, self.sl_xmax, self.sl_ymin, self.sl_ymax,
        ]

        # ── Buttons ──────────────────────────────────────────────
        by = s0 + self._N_SLIDERS * self._SL_STEP + 4
        bw, bh = 106, 26
        self.btn_reset  = Button(sx,              by, bw, bh, "Reset [R]")
        self.btn_pause  = Button(sx + bw + 4,     by, bw, bh, "Pause [Spc]")
        self.btn_vecs   = Button(sx + 2*(bw + 4), by, bw, bh, "Vectors [V]")
        self.btn_trails = Button(sx + 3*(bw + 4), by, bw, bh, "Trails: ON")
        self.buttons    = [self.btn_reset, self.btn_pause, self.btn_vecs, self.btn_trails]

        # ── Energy plot (bottom of panel) ────────────────────────
        self._plot_y   = by + bh + 18        # label y
        self._plot_h   = WIN_H - self._plot_y - 82
        self._energy_hist: list[tuple] = []
        self._hist_max  = 300

        # ── Persistence-of-vision trail surface ──────────────────
        self._trail_surf = pygame.Surface((BOX_SIZE, BOX_SIZE))
        self._trail_surf.fill(BOX_BG)
        # Semi-transparent overlay applied each frame to fade old trails
        self._fade_surf  = pygame.Surface((BOX_SIZE, BOX_SIZE))
        self._fade_surf.fill(BOX_BG)
        self._fade_surf.set_alpha(18)           # controls trail length

        # ── State flags ──────────────────────────────────────────
        self.paused      = False
        self.show_vecs   = False
        self.show_trails = True

        self.state: GravityState | None = None
        self._reset()

    # ── Helpers ────────────────────────────────────────────────────────────────
    def _reset(self):
        N     = int(self.sl_n.value)
        vmin  = self.sl_vmin.value
        vmax  = max(self.sl_vmax.value, vmin + 1e-3)
        m     = self.sl_mass.value
        G     = self.sl_G.value * 1000.0
        soft  = self.sl_soft.value
        xmin  = self.sl_xmin.value * BOX_SIZE
        xmax  = max(self.sl_xmax.value, self.sl_xmin.value + 0.01) * BOX_SIZE
        ymin  = self.sl_ymin.value * BOX_SIZE
        ymax  = max(self.sl_ymax.value, self.sl_ymin.value + 0.01) * BOX_SIZE

        pos = np.array([[random.uniform(xmin, xmax), random.uniform(ymin, ymax)]
                        for _ in range(N)], dtype=np.float64)
        vel = np.empty_like(pos)
        for i in range(N):
            spd        = random.uniform(vmin, vmax)
            angle      = random.uniform(0, 2 * math.pi)
            vel[i, 0]  = spd * math.cos(angle)
            vel[i, 1]  = spd * math.sin(angle)

        self.state = GravityState(pos, vel, m, G, soft)
        self._energy_hist.clear()
        self._trail_surf.fill(BOX_BG)

    def _sync_live_params(self):
        """G, m, ε can change live (no respawn needed)."""
        self.state.G    = self.sl_G.value * 1000.0
        self.state.m    = self.sl_mass.value
        self.state.soft = self.sl_soft.value

    # ── Drawing ────────────────────────────────────────────────────────────────
    def _draw_box_border(self):
        pygame.draw.rect(self.screen, BOX_LINE,
                         (BOX_MARGIN, BOX_MARGIN, BOX_SIZE, BOX_SIZE), 2)

    def _update_and_draw_trails(self, speeds: np.ndarray, s_max: float):
        """Fade trail surface, stamp current positions, then blit."""
        self._trail_surf.blit(self._fade_surf, (0, 0))
        for i, p in enumerate(self.state.pos):
            t = speeds[i] / s_max
            c = speed_color(t)
            pygame.draw.circle(self._trail_surf, c, (int(p[0]), int(p[1])), 2)
        self.screen.blit(self._trail_surf, (BOX_MARGIN, BOX_MARGIN))

    def _draw_particles(self, speeds: np.ndarray, s_max: float):
        for i, (p, v) in enumerate(zip(self.state.pos, self.state.vel)):
            t  = speeds[i] / s_max
            c  = speed_color(t)
            px = BOX_MARGIN + int(p[0])
            py = BOX_MARGIN + int(p[1])
            pygame.draw.circle(self.screen, c,    (px, py), 4)
            pygame.draw.circle(self.screen, WHITE, (px, py), 4, 1)
            if self.show_vecs and speeds[i] > 1e-6:
                scale = 20.0 / speeds[i]
                pygame.draw.line(self.screen, YELLOW,
                                 (px, py),
                                 (int(px + v[0] * scale), int(py + v[1] * scale)), 1)

    def _draw_com(self):
        """Draw centre-of-mass crosshair."""
        com = self.state.pos.mean(axis=0)
        cx  = BOX_MARGIN + int(com[0])
        cy  = BOX_MARGIN + int(com[1])
        pygame.draw.line(self.screen, ORANGE, (cx - 8, cy), (cx + 8, cy), 1)
        pygame.draw.line(self.screen, ORANGE, (cx, cy - 8), (cx, cy + 8), 1)
        pygame.draw.circle(self.screen, ORANGE, (cx, cy), 4, 1)

    def _draw_energy_plot(self):
        hx = PANEL_X
        hy = self._plot_y + 20
        hw = PANEL_W - 10
        hh = self._plot_h

        pygame.draw.rect(self.screen, BOX_BG,   (hx, hy, hw, hh))
        pygame.draw.rect(self.screen, BOX_LINE, (hx, hy, hw, hh), 1)
        self.screen.blit(
            self.font_med.render("Energy history", True, GRAY), (hx, self._plot_y)
        )

        hist = self._energy_hist
        if len(hist) < 2:
            return

        KEs = [h[0] for h in hist]
        PEs = [h[1] for h in hist]
        TEs = [h[2] for h in hist]

        all_vals = KEs + PEs + TEs
        v_min, v_max = min(all_vals), max(all_vals)
        span = v_max - v_min or 1.0
        n    = len(hist)

        def to_screen(val, idx):
            x = hx + int(idx / (n - 1) * hw)
            y = hy + hh - 4 - int((val - v_min) / span * (hh - 8))
            return (x, y)

        for series, color, label in [
            (KEs, GREEN,  "KE"),
            (PEs, RED,    "PE"),
            (TEs, YELLOW, "E_total"),
        ]:
            pts = [to_screen(series[i], i) for i in range(n)]
            pygame.draw.lines(self.screen, color, False, pts, 1)

        # Current values beneath chart
        KE, PE, TE = hist[-1]
        y = hy + hh + 6
        for label, val, color in [("KE", KE, GREEN), ("PE", PE, RED), ("E_total", TE, YELLOW)]:
            txt = self.font_sm.render(f"{label}  {val:>12.1f}", True, color)
            self.screen.blit(txt, (hx, y));  y += 17

    def _draw_panel(self):
        self.screen.blit(
            self.font_lg.render("Parameters", True, WHITE), (PANEL_X, 10)
        )
        note = self.font_sm.render(
            "m, G, ε update live  |  N/spawn require Reset", True, DGRAY
        )
        self.screen.blit(note, (PANEL_X, WIN_H - 14))
        for sl in self.sliders:
            sl.draw(self.screen, self.font_sm)
        for btn in self.buttons:
            btn.draw(self.screen, self.font_med)

    # ── Events ─────────────────────────────────────────────────────────────────
    def _handle_events(self) -> bool:
        mx, my = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.update_hover((mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for sl in self.sliders:
                    sl.handle_mousedown(event.pos)
                if self.btn_reset.clicked(event.pos):
                    self._reset()
                if self.btn_pause.clicked(event.pos):
                    self._toggle_pause()
                if self.btn_vecs.clicked(event.pos):
                    self._toggle_vecs()
                if self.btn_trails.clicked(event.pos):
                    self._toggle_trails()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for sl in self.sliders:
                    sl.handle_mouseup()

            if event.type == pygame.MOUSEMOTION:
                for sl in self.sliders:
                    sl.handle_mousemove(event.pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: self._toggle_pause()
                if event.key == pygame.K_r:     self._reset()
                if event.key == pygame.K_v:     self._toggle_vecs()
                if event.key == pygame.K_t:     self._toggle_trails()

        return True

    def _toggle_pause(self):
        self.paused = not self.paused
        self.btn_pause.label = "Resume [Spc]" if self.paused else "Pause [Spc]"

    def _toggle_vecs(self):
        self.show_vecs = not self.show_vecs
        self.btn_vecs.label = "Vecs: ON  [V]" if self.show_vecs else "Vectors [V]"

    def _toggle_trails(self):
        self.show_trails = not self.show_trails
        self.btn_trails.label = "Trails: ON" if self.show_trails else "Trails: OFF"
        if not self.show_trails:
            self._trail_surf.fill(BOX_BG)

    # ── Main loop ──────────────────────────────────────────────────────────────
    def run(self):
        dt    = 1.0 / 60.0
        frame = 0

        while True:
            if not self._handle_events():
                break

            if not self.paused:
                self._sync_live_params()
                self.state.step(dt, n_sub=4)

                if frame % 6 == 0 and len(self._energy_hist) < self._hist_max:
                    self._energy_hist.append(self.state.energy())
                elif frame % 6 == 0:
                    self._energy_hist.pop(0)
                    self._energy_hist.append(self.state.energy())
                frame += 1

            # ── render ─────────────────────────────────────────────
            self.screen.fill(BG)

            speeds = np.sqrt(np.einsum('ij,ij->i', self.state.vel, self.state.vel))
            s_max  = speeds.max() or 1.0

            if self.show_trails:
                self._update_and_draw_trails(speeds, s_max)
            else:
                # draw plain box background
                pygame.draw.rect(self.screen, BOX_BG,
                                 (BOX_MARGIN, BOX_MARGIN, BOX_SIZE, BOX_SIZE))

            self._draw_box_border()
            self._draw_com()
            self._draw_particles(speeds, s_max)
            self._draw_panel()
            self._draw_energy_plot()

            if self.paused:
                self.screen.blit(
                    self.font_lg.render("PAUSED", True, YELLOW),
                    (BOX_MARGIN + 10, BOX_MARGIN + 10)
                )

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Simulation().run()