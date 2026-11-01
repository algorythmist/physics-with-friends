import numpy as np
from scipy.integrate import quad
from sympy.stats import P, E, variance, density, Die, Normal
from sympy.stats.rv import RandomSymbol
from sympy import simplify, Symbol, log, Abs, Expr, lambdify


def _as_pdf(arg, var):
    # RandomSymbols carry a distribution, so their pdf must be extracted before it can be integrated
    if isinstance(arg, RandomSymbol):
        return density(arg)(var)
    # Anything else must already be a pdf expression in `var`, otherwise the integral below is meaningless
    if isinstance(arg, Expr):
        return arg
    raise TypeError(f"Expected a RandomSymbol or sympy Expr, got {type(arg)}")


def kl_divergence(X, Y, var=None):
    """Compute the Kullback-Leibler divergence KL(X || Y).

    Args:
        X (RandomSymbol | Expr): A sympy.stats RandomSymbol (its pdf is derived
            automatically) or a sympy Expr already representing a pdf in terms
            of `var`.
        Y (RandomSymbol | Expr): Same as `X`.
        var (Symbol | None): Integration variable. Defaults to a fresh
            Symbol('x') if not given.

    Returns:
        float: The KL divergence KL(X || Y), computed via numerical integration.

    Raises:
        TypeError: If `X` or `Y` is neither a RandomSymbol nor a sympy Expr.
    """
    var = var or Symbol('x') # Shared integration variable for both densities
    p_pdf = _as_pdf(X, var)
    q_pdf = _as_pdf(Y, var)
    integrand = lambdify(var, p_pdf * log(p_pdf / q_pdf), 'numpy') # sympy's symbolic integrate struggled to close-form this, so integrate numerically instead
    result, _ = quad(integrand, -np.inf, np.inf)
    return result


def l1_distance(X, Y, var=None):
    """Compute the L1 (total variation-scale) distance between two densities.

    Args:
        X (RandomSymbol | Expr): A sympy.stats RandomSymbol (its pdf is derived
            automatically) or a sympy Expr already representing a pdf in terms
            of `var`.
        Y (RandomSymbol | Expr): Same as `X`.
        var (Symbol | None): Integration variable. Defaults to a fresh
            Symbol('x') if not given.

    Returns:
        float: The L1 distance integral(|p(x) - q(x)| dx), computed via numerical integration.

    Raises:
        TypeError: If `X` or `Y` is neither a RandomSymbol nor a sympy Expr.
    """
    var = var or Symbol('x')
    p_pdf = _as_pdf(X, var)
    q_pdf = _as_pdf(Y, var)
    integrand = lambdify(var, Abs(p_pdf - q_pdf), 'numpy') # sympy's symbolic integrate struggled to close-form this, so integrate numerically instead
    result, _ = quad(integrand, -np.inf, np.inf)
    return result

X, Y = Die('X', 6), Die('Y', 6) # Define two six sided dice
Z = Normal('Z', 0, 1) # Declare a Normal random variable with mean 0, std 1

print(P(X>3)) # Probability X is greater than 3
print(E(X+Y)) # Expectation of the sum of two dice
print(variance(X+Y)) # Variance of the sum of two dice

print(simplify(P(Z>1))) # Probability of Z being greater than 1

W = Normal('W', 1, 1) # A second Normal, shifted in mean, to compare against Z
print(l1_distance(Z, W)) # L1 distance between the two Normal densities

print(l1_distance(Z, X))
