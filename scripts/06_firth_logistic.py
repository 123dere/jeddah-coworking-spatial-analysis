"""Firth bias-reduced logistic regression for a public analytical CSV.

Model:
  cw_presence ~ business_density + built_up_pct + road_density

Inference:
- penalized likelihood-ratio p-values
- penalized profile-likelihood confidence intervals

This implementation standardizes predictors internally for numerical stability
and transforms slopes back to original units for reporting.
"""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from scipy.optimize import minimize, brentq
from scipy.special import expit
from scipy.stats import chi2

PREDICTORS = ["business_density", "built_up_pct", "road_density"]

def prepare(df):
    df = df.dropna(subset=["cw_presence"] + PREDICTORS).copy()
    y = df["cw_presence"].astype(float).to_numpy()
    x_raw = df[PREDICTORS].astype(float).to_numpy()
    means = x_raw.mean(axis=0)
    sds = x_raw.std(axis=0, ddof=0)
    if np.any(sds <= 0):
        raise ValueError("A predictor has zero variance.")
    z = (x_raw - means) / sds
    X = np.column_stack([np.ones(len(z)), z])
    return y, X, means, sds

def pll(beta, X, y):
    eta = X @ beta
    ordinary = np.sum(y * eta - np.logaddexp(0.0, eta))
    p = expit(eta)
    w = np.clip(p * (1.0 - p), 1e-12, None)
    info = X.T @ (X * w[:, None])
    sign, logdet = np.linalg.slogdet(info)
    if sign <= 0 or not np.isfinite(logdet):
        return -np.inf
    return ordinary + 0.5 * logdet

def objective(beta, X, y):
    value = pll(beta, X, y)
    return 1e100 if not np.isfinite(value) else -value

def fit_firth(X, y):
    result = minimize(objective, np.zeros(X.shape[1]), args=(X, y), method="BFGS")
    if not result.success:
        result = minimize(objective, result.x, args=(X, y), method="Nelder-Mead",
                          options={"maxiter": 15000})
    beta = result.x
    return beta, pll(beta, X, y)

def constrained_pll(X, y, fixed_index, fixed_value, full_beta):
    k = X.shape[1]
    free = [i for i in range(k) if i != fixed_index]
    start = full_beta[free]

    def fn(free_beta):
        beta = np.zeros(k)
        beta[free] = free_beta
        beta[fixed_index] = fixed_value
        return objective(beta, X, y)

    result = minimize(fn, start, method="BFGS")
    if not result.success:
        result = minimize(fn, result.x, method="Nelder-Mead", options={"maxiter": 15000})
    return -result.fun

def plr_test(X, y, full_beta, full_pll, index):
    null_pll = constrained_pll(X, y, index, 0.0, full_beta)
    stat = max(0.0, 2.0 * (full_pll - null_pll))
    return stat, chi2.sf(stat, 1)

def profile_ci(X, y, full_beta, full_pll, index, level=0.95):
    cutoff = chi2.ppf(level, 1)
    estimate = full_beta[index]

    def root(v):
        fixed = constrained_pll(X, y, index, v, full_beta)
        return 2.0 * (full_pll - fixed) - cutoff

    step = 0.25
    lo = estimate - step
    for _ in range(60):
        if root(lo) >= 0:
            break
        step *= 1.5
        lo = estimate - step
    lower = brentq(root, lo, estimate)

    step = 0.25
    hi = estimate + step
    for _ in range(60):
        if root(hi) >= 0:
            break
        step *= 1.5
        hi = estimate + step
    upper = brentq(root, estimate, hi)
    return lower, upper

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output", type=Path, default=Path("outputs/firth_results_public.csv"))
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    y, X, means, sds = prepare(df)
    beta_std, full_pll = fit_firth(X, y)

    rows = []
    for j, name in enumerate(PREDICTORS, start=1):
        lr, p = plr_test(X, y, beta_std, full_pll, j)
        lo_std, hi_std = profile_ci(X, y, beta_std, full_pll, j)

        beta = beta_std[j] / sds[j-1]
        lo = lo_std / sds[j-1]
        hi = hi_std / sds[j-1]

        rows.append({
            "predictor": name,
            "beta": beta,
            "odds_ratio": np.exp(beta),
            "profile_ci_low": np.exp(lo),
            "profile_ci_high": np.exp(hi),
            "plr_chisq": lr,
            "plr_p": p,
        })

    out = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False)
    print(out.to_string(index=False))
    print(f"\nN={len(y)}, events={int(y.sum())}")
    print(f"Saved: {args.output}")

if __name__ == "__main__":
    main()
