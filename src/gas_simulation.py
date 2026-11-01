#!/usr/bin/env python3
"""
2D Ideal Gas Thermodynamics Simulation

Point particles bounce elastically off the walls of a 2D box.
All initial conditions are configurable via interactive sliders.
The speed distribution is compared against the 2D Maxwell-Boltzmann prediction.

Physics:
  - mass = 1, kB = 1
  - Temperature T = <KE> = <v²>/2  (equipartition: 2 DOF → <E> = kBT)
  - 2D Maxwell-Boltzmann: f(v) = (v/T) exp(-v²/2T)
  - Mean speed:          <v>   = sqrt(πT/2)
  - RMS speed:           v_rms = sqrt(2T)
  - Most probable speed: v_p   = sqrt(T)
"""

import sys
import math
import random
import numpy as np
import pygame

# ── Window / layout ────────────────────────────────────────────────────────────
WIN_W, WIN_H  = 1380, 740
BOX_MARGIN    = 20
BOX_SIZE      = WIN_H - 2 * BOX_MARGIN   # 700 px square simulation area
PANEL_X       = BOX_SIZE + 2 * BOX_MARGIN + 10   # right-panel left edge
PANEL_W       = WIN_W - PANEL_X - 10

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
        return (int(20 + 80 * s), int(100 + 80 * s), int(230 - 130 * s))
    s = (t - 0.5) * 2
    return (int(100 + 120 * s), int(180 - 100 * s), int(100 - 80 * s))


# ── Slider widget ──────────────────────────────────────────────────────────────
class Slider:
    TRACK_H = 6
    KNOB_R  = 8

    def __init__(self, x, y, w, label, lo, hi, value, integer=False, fmt=None):
        self.x, self.y, self.w = x, y, w
        self.label   = label
        self.lo, self.hi = lo, hi
        self.value   = float(value)
        self.integer = integer
        self.fmt     = fmt or ("{:d}" if integer else "{:.2f}")
        self.dragging = False

    @property
    def _frac(self):
        return (self.value - self.lo) / (self.hi - self.lo)

    @property
    def _knob_x(self):
        return self.x + int(self._frac * self.w)

    def draw(self, surf, font_sm):
        val_str  = self.fmt.format(int(self.value) if self.integer else self.value)
        label_surf = font_sm.render(f"{self.label}: {val_str}", True, GRAY)
        surf.blit(label_surf, (self.x, self.y - 17))

        cy = self.y + self.KNOB_R
        # track
        pygame.draw.rect(surf, DGRAY,
                         (self.x, cy - self.TRACK_H // 2, self.w, self.TRACK_H),
                         border_radius=3)
        # filled
        fill_w = max(int(self._frac * self.w), 0)
        if fill_w:
            pygame.draw.rect(surf, CYAN,
                             (self.x, cy - self.TRACK_H // 2, fill_w, self.TRACK_H),
                             border_radius=3)
        # knob
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


# ── Particle ───────────────────────────────────────────────────────────────────
class Particle:
    __slots__ = ("x", "y", "vx", "vy")

    def __init__(self, x, y, vx, vy):
        self.x, self.y   = float(x), float(y)
        self.vx, self.vy = float(vx), float(vy)

    @property
    def speed(self):
        return math.hypot(self.vx, self.vy)

    @property
    def ke(self):
        return 0.5 * (self.vx * self.vx + self.vy * self.vy)

    def step(self, dt: float, box: float):
        self.x += self.vx * dt
        self.y += self.vy * dt
        # elastic wall reflections
        if self.x < 0:
            self.x  = -self.x
            self.vx =  abs(self.vx)
        elif self.x > box:
            self.x  = 2 * box - self.x
            self.vx = -abs(self.vx)
        if self.y < 0:
            self.y  = -self.y
            self.vy =  abs(self.vy)
        elif self.y > box:
            self.y  = 2 * box - self.y
            self.vy = -abs(self.vy)


# ── Simulation ─────────────────────────────────────────────────────────────────
class Simulation:

    # ── slider row spacing ─────────────────────────────────────
    _SL_STEP = 52   # px between consecutive slider rows

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("2D Ideal Gas – Thermodynamics Simulation")
        self.clock = pygame.time.Clock()

        self.font_lg  = pygame.font.SysFont("monospace", 20, bold=True)
        self.font_med = pygame.font.SysFont("monospace", 15)
        self.font_sm  = pygame.font.SysFont("monospace", 13)

        # ── Sliders (x, y, w, label, lo, hi, default) ──────────
        sx, sw = PANEL_X, PANEL_W - 10
        sy0    = 42      # first slider y

        self.sl_n    = Slider(sx, sy0 + 0 * self._SL_STEP, sw,
                              "N particles",     10,  600,  200, integer=True)
        self.sl_vmin = Slider(sx, sy0 + 1 * self._SL_STEP, sw,
                              "Min speed",       0.0, 500.0,  50.0)
        self.sl_vmax = Slider(sx, sy0 + 2 * self._SL_STEP, sw,
                              "Max speed",       1.0, 1000.0, 500.0)
        self.sl_xmin = Slider(sx, sy0 + 3 * self._SL_STEP, sw,
                              "X min (0–1)",     0.0, 1.0,  0.0)
        self.sl_xmax = Slider(sx, sy0 + 4 * self._SL_STEP, sw,
                              "X max (0–1)",     0.0, 1.0,  1.0)
        self.sl_ymin = Slider(sx, sy0 + 5 * self._SL_STEP, sw,
                              "Y min (0–1)",     0.0, 1.0,  0.0)
        self.sl_ymax = Slider(sx, sy0 + 6 * self._SL_STEP, sw,
                              "Y max (0–1)",     0.0, 1.0,  1.0)

        self.sliders = [
            self.sl_n, self.sl_vmin, self.sl_vmax,
            self.sl_xmin, self.sl_xmax, self.sl_ymin, self.sl_ymax,
        ]

        # ── Buttons ─────────────────────────────────────────────
        by  = sy0 + 7 * self._SL_STEP + 4
        bw, bh = 118, 28
        self.btn_reset = Button(sx,              by, bw, bh, "Reset [R]")
        self.btn_pause = Button(sx + bw + 6,     by, bw, bh, "Pause [Spc]")
        self.btn_vecs  = Button(sx + 2*(bw + 6), by, bw, bh, "Vectors [V]")
        self.buttons   = [self.btn_reset, self.btn_pause, self.btn_vecs]

        # ── Histogram position ──────────────────────────────────
        self._hist_y  = by + bh + 32
        self._hist_h  = WIN_H - self._hist_y - 90

        self.paused    = False
        self.show_vecs = False
        self.particles: list[Particle] = []
        self._reset()

    # ── helpers ────────────────────────────────────────────────
    def _reset(self):
        N     = int(self.sl_n.value)
        vmin  = self.sl_vmin.value
        vmax  = max(self.sl_vmax.value, vmin + 1e-3)
        xmin  = self.sl_xmin.value * BOX_SIZE
        xmax  = max(self.sl_xmax.value, self.sl_xmin.value + 0.01) * BOX_SIZE
        ymin  = self.sl_ymin.value * BOX_SIZE
        ymax  = max(self.sl_ymax.value, self.sl_ymin.value + 0.01) * BOX_SIZE

        self.particles = []
        for _ in range(N):
            x     = random.uniform(xmin, xmax)
            y     = random.uniform(ymin, ymax)
            speed = random.uniform(vmin, vmax)
            angle = random.uniform(0, 2 * math.pi)
            self.particles.append(
                Particle(x, y, speed * math.cos(angle), speed * math.sin(angle))
            )

    def _temperature(self) -> float:
        if not self.particles:
            return 0.0
        return sum(p.ke for p in self.particles) / len(self.particles)

    # ── drawing ────────────────────────────────────────────────
    def _draw_box(self):
        r = pygame.Rect(BOX_MARGIN, BOX_MARGIN, BOX_SIZE, BOX_SIZE)
        pygame.draw.rect(self.screen, BOX_BG,   r)
        pygame.draw.rect(self.screen, BOX_LINE, r, 2)

    def _draw_particles(self):
        speeds = [p.speed for p in self.particles]
        s_max  = max(speeds) if speeds else 1.0

        for p in self.particles:
            t  = p.speed / s_max
            c  = speed_color(t)
            px = BOX_MARGIN + int(p.x)
            py = BOX_MARGIN + int(p.y)
            pygame.draw.circle(self.screen, c, (px, py), 3)

            if self.show_vecs and p.speed > 1e-6:
                scale = 20.0 / p.speed
                ex = int(px + p.vx * scale)
                ey = int(py + p.vy * scale)
                pygame.draw.line(self.screen, YELLOW, (px, py), (ex, ey), 1)

    def _draw_sliders(self):
        self.screen.blit(
            self.font_lg.render("Parameters", True, WHITE), (PANEL_X, 10)
        )
        for sl in self.sliders:
            sl.draw(self.screen, self.font_sm)

    def _draw_buttons(self):
        for btn in self.buttons:
            btn.draw(self.screen, self.font_med)

    def _draw_histogram(self):
        hx = PANEL_X
        hy = self._hist_y
        hw = PANEL_W - 10
        hh = self._hist_h

        speeds = [p.speed for p in self.particles]
        if not speeds:
            return

        # background
        pygame.draw.rect(self.screen, BOX_BG,   (hx, hy, hw, hh))
        pygame.draw.rect(self.screen, BOX_LINE, (hx, hy, hw, hh), 1)

        # histogram
        s_max  = max(speeds) * 1.1 or 1.0
        n_bins = 40
        bins   = [0] * n_bins
        for s in speeds:
            idx = min(int(s / s_max * n_bins), n_bins - 1)
            bins[idx] += 1
        bin_max = max(bins) or 1

        bw = hw / n_bins
        for i, cnt in enumerate(bins):
            bar_h = int((cnt / bin_max) * (hh - 4))
            pygame.draw.rect(
                self.screen, speed_color(i / n_bins),
                (hx + int(i * bw), hy + hh - bar_h, max(int(bw) - 1, 1), bar_h)
            )

        # theoretical 2D Maxwell-Boltzmann curve: f(v) = (v/T) exp(-v²/2T)
        T = self._temperature()
        if T > 0:
            vs  = np.linspace(0, s_max, 300)
            fv  = (vs / T) * np.exp(-vs ** 2 / (2 * T))
            fmx = fv.max()
            if fmx > 0:
                pts = [
                    (int(hx + v / s_max * hw),
                     int(hy + hh - (f / fmx) * (hh - 4)))
                    for v, f in zip(vs, fv)
                ]
                pygame.draw.lines(self.screen, YELLOW, False, pts, 2)

        # label
        lbl = self.font_med.render("Speed distribution  — yellow: Maxwell-Boltzmann", True, GRAY)
        self.screen.blit(lbl, (hx, hy - 20))

    def _draw_stats(self):
        speeds = [p.speed for p in self.particles]
        if not speeds:
            return
        T      = self._temperature()
        mean_v = sum(speeds) / len(speeds)
        rms_v  = math.sqrt(sum(s * s for s in speeds) / len(speeds))

        x = PANEL_X
        y = WIN_H - 78
        lines = [
            (f"T = <KE> = {T:.4f}", ORANGE),
            (f"<v>  meas {mean_v:.4f}   theory {math.sqrt(math.pi * T / 2):.4f}", GREEN),
            (f"vrms meas {rms_v:.4f}   theory {math.sqrt(2 * T):.4f}", CYAN),
            (f"vp   (most probable)    theory {math.sqrt(max(T, 0)):.4f}", GRAY),
        ]
        for text, color in lines:
            self.screen.blit(self.font_sm.render(text, True, color), (x, y))
            y += 18

    # ── event handling ─────────────────────────────────────────
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
                    self.paused = not self.paused
                    self.btn_pause.label = "Resume [Spc]" if self.paused else "Pause [Spc]"
                if self.btn_vecs.clicked(event.pos):
                    self.show_vecs = not self.show_vecs
                    self.btn_vecs.label = "Vecs: ON  [V]" if self.show_vecs else "Vectors [V]"

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for sl in self.sliders:
                    sl.handle_mouseup()

            if event.type == pygame.MOUSEMOTION:
                for sl in self.sliders:
                    sl.handle_mousemove(event.pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                    self.btn_pause.label = "Resume [Spc]" if self.paused else "Pause [Spc]"
                if event.key == pygame.K_r:
                    self._reset()
                if event.key == pygame.K_v:
                    self.show_vecs = not self.show_vecs
                    self.btn_vecs.label = "Vecs: ON  [V]" if self.show_vecs else "Vectors [V]"

        return True

    # ── main loop ──────────────────────────────────────────────
    def run(self):
        dt = 1.0 / 60.0
        while True:
            if not self._handle_events():
                break

            if not self.paused:
                for p in self.particles:
                    p.step(dt, BOX_SIZE)

            self.screen.fill(BG)
            self._draw_box()
            self._draw_particles()
            self._draw_sliders()
            self._draw_buttons()
            self._draw_histogram()
            self._draw_stats()

            if self.paused:
                s = self.font_lg.render("PAUSED", True, YELLOW)
                self.screen.blit(s, (BOX_MARGIN + 10, BOX_MARGIN + 10))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Simulation().run()
