#!/usr/bin/env python3
"""
================================================================================
FIN 439: Applied Financial Modeling & Corporate Valuation
Project 2: Investment Management Application
Student: Elliot
Module: modules/mandate.py

Description:
    Evaluates candidate and baseline portfolios against the Meridian Foundation
    investment mandate (Lab 13). Implements mechanical constraint checks for:
      1. Weights sum to 100%
      2. Long-only constraint (lowest weight >= 0.0%)
      3. Reserve requirement (reserve-eligible weight >= reserve minimum)
      4. Five-business-day liquidity requirement (redeemable <= 5 days >= 90.0%)
      5. Single-company issuer concentration ceiling (aggregate <= 8.0%)
      6. Calendar-year loss rule (flagged as "requires CIO clarification")

    Reused directly from Lab 13 with full fidelity.
================================================================================
"""

from __future__ import annotations
import sys
from typing import Any, Dict, List, Tuple

# ==============================================================================
# EDITABLE INPUTS (Meridian Foundation Reserve Case)
# ==============================================================================

RESERVE_SIZE = 100.0            # Reserve portfolio size in USD millions
QUARTERLY_DISTRIBUTION = 0.75   # Payout in USD millions every quarter
QUARTERS_TO_COVER = 4           # Twelve months of payouts (4 quarters)
LIQUIDITY_WINDOW = 5            # Liquidity window in business days
MINIMUM_LIQUID_SHARE = 90.0     # Minimum percent redeemable within window
ISSUER_LIMIT = 8.0              # Maximum percent allocated to any single company

# Holdings Reference Table
# Format: (Holding Name, Issuer, Business Days to Redeem, Reserve-Eligible)
HOLDINGS: List[Tuple[str, str, int, bool]] = [
    ("Cash", "none", 0, True),
    ("Treasury bills", "U.S. Treasury", 1, True),
    ("Treasury 10-year note", "U.S. Treasury", 1, True),
    ("Global equity index fund", "diversified fund", 2, False),
    ("Investment-grade bond fund", "diversified fund", 3, False),
    ("Private real estate fund", "diversified fund", 90, False),
    ("Acme Corp bonds", "Acme Corp", 4, False),
    ("Acme Corp stock", "Acme Corp", 1, False),
]

# Issuer Exemptions: Cash, U.S. Treasury, and diversified funds are exempt.
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}

# Candidate Portfolios from Lab 13
CANDIDATES: Dict[str, Dict[str, float]] = {
    "A": {
        "Cash": 2.0,
        "Treasury bills": 2.0,
        "Treasury 10-year note": 10.0,
        "Global equity index fund": 60.0,
        "Investment-grade bond fund": 26.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 0.0,
    },
    "B": {
        "Cash": 1.0,
        "Treasury bills": 0.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 55.0,
        "Investment-grade bond fund": 20.0,
        "Private real estate fund": 15.0,
        "Acme Corp bonds": 5.0,
        "Acme Corp stock": 4.0,
    },
    "C": {
        "Cash": 1.0,
        "Treasury bills": 1.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 70.0,
        "Investment-grade bond fund": 20.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 8.0,
    },
    # Candidate D: Adversarial Portfolio (Passes mechanical checks, offends S4/S9)
    "D": {
        "Cash": 3.0,
        "Treasury bills": 0.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 97.0,
        "Investment-grade bond fund": 0.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 0.0,
    },
    # Candidate E: Benchmark Portfolio (60% Global Equity, 40% IG Bonds)
    "E": {
        "Cash": 0.0,
        "Treasury bills": 0.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 60.0,
        "Investment-grade bond fund": 40.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 0.0,
    },
}


# ==============================================================================
# COMPUTATION ENGINE
# ==============================================================================

def calculate_reserve_minimum(quarters: int = QUARTERS_TO_COVER,
                              distribution: float = QUARTERLY_DISTRIBUTION,
                              reserve_size: float = RESERVE_SIZE) -> float:
    """Computes reserve minimum: quarters * distribution / reserve_size as a percent (3.0%)."""
    return (quarters * distribution / reserve_size) * 100.0


def evaluate_portfolio(weights: Dict[str, float],
                       holdings_table: List[Tuple[str, str, int, bool]] = HOLDINGS,
                       reserve_min_pct: float = 3.0) -> Dict[str, Any]:
    """
    Evaluates a candidate portfolio against mandate constraints.
    Returns calculated metrics, status strings, boolean flags, and final rule failure count.
    """
    # Create lookup mappings from holdings table
    issuer_map = {row[0]: row[1] for row in holdings_table}
    days_map = {row[0]: row[2] for row in holdings_table}
    reserve_eligible_map = {row[0]: row[3] for row in holdings_table}

    # 1. Weights sum to 100%
    total_weight = sum(weights.values())
    sum_pass = abs(total_weight - 100.0) < 1e-4

    # 2. Lowest weight not negative (long-only)
    min_weight = min(weights.values()) if weights else 0.0
    long_only_pass = min_weight >= -1e-7

    # 3. Reserve-eligible weight at least reserve minimum
    reserve_weight = sum(w for h, w in weights.items() if reserve_eligible_map.get(h, False))
    reserve_pass = reserve_weight >= (reserve_min_pct - 1e-7)

    # 4. Weight redeemable within liquidity window at least minimum liquid share
    liquid_weight = sum(w for h, w in weights.items() if days_map.get(h, 999) <= LIQUIDITY_WINDOW)
    liquid_pass = liquid_weight >= (MINIMUM_LIQUID_SHARE - 1e-7)

    # 5. Largest single company at most issuer limit (non-exempt issuers aggregated together)
    company_totals: Dict[str, float] = {}
    for h, w in weights.items():
        issuer = issuer_map.get(h, "none")
        if issuer not in EXEMPT_ISSUERS:
            company_totals[issuer] = company_totals.get(issuer, 0.0) + w

    largest_company_weight = max(company_totals.values()) if company_totals else 0.0
    issuer_pass = largest_company_weight <= (ISSUER_LIMIT + 1e-7)

    # Specific failure descriptions for transparency
    failure_details: List[str] = []
    if not sum_pass:
        failure_details.append(f"Weights sum to {total_weight:.2f}% (must be 100.0%)")
    if not long_only_pass:
        failure_details.append(f"Short position detected: min weight {min_weight:.2f}% < 0.0%")
    if not reserve_pass:
        failure_details.append(f"Reserve allocation {reserve_weight:.1f}% < {reserve_min_pct:.1f}% floor")
    if not liquid_pass:
        failure_details.append(f"5-day liquidity {liquid_weight:.1f}% < {MINIMUM_LIQUID_SHARE:.0f}% minimum")
    if not issuer_pass:
        failure_details.append(f"Single-issuer concentration {largest_company_weight:.1f}% > {ISSUER_LIMIT:.0f}% cap")

    # Count checkable failures
    checkable_passes = [sum_pass, long_only_pass, reserve_pass, liquid_pass, issuer_pass]
    fails_count = sum(1 for p in checkable_passes if not p)

    if fails_count == 0:
        verdict = "passes every checkable rule"
        overall_pass = True
    else:
        verdict = f"fails {fails_count} rule(s)"
        overall_pass = False

    return {
        "total_weight": total_weight,
        "sum_pass": sum_pass,
        "sum_str": f"{total_weight:.1f} {'pass' if sum_pass else 'FAIL'}",
        "min_weight": min_weight,
        "long_only_pass": long_only_pass,
        "long_only_str": f"{min_weight:.1f} {'pass' if long_only_pass else 'FAIL'}",
        "reserve_weight": reserve_weight,
        "reserve_pass": reserve_pass,
        "reserve_str": f"{reserve_weight:.1f} {'pass' if reserve_pass else 'FAIL'}",
        "liquid_weight": liquid_weight,
        "liquid_pass": liquid_pass,
        "liquid_str": f"{liquid_weight:.1f} {'pass' if liquid_pass else 'FAIL'}",
        "largest_company_weight": largest_company_weight,
        "issuer_pass": issuer_pass,
        "issuer_str": f"{largest_company_weight:.1f} {'pass' if issuer_pass else 'FAIL'}",
        "calendar_loss_str": "requires CIO clarification",
        "fails_count": fails_count,
        "failure_details": failure_details,
        "overall_pass": overall_pass,
        "verdict": verdict,
    }


def evaluate_sleeve_weights(sleeve_weights: Dict[str, float], reserve_min_pct: float = 3.0) -> Dict[str, Any]:
    """
    Evaluates weights given for the 4 core sleeves:
      - Treasury bills (Reserve: Yes, Liquidity: 1d, Exempt)
      - Treasury 10-year note (Reserve: Yes, Liquidity: 1d, Exempt)
      - Investment-grade bond fund (Reserve: No, Liquidity: 3d, Exempt)
      - Global equity index fund (Reserve: No, Liquidity: 2d, Exempt)
    """
    full_weights = {
        "Cash": sleeve_weights.get("Cash", 0.0),
        "Treasury bills": sleeve_weights.get("Treasury bills", 0.0),
        "Treasury 10-year note": sleeve_weights.get("Treasury 10-year note", 0.0),
        "Global equity index fund": sleeve_weights.get("Global equity index fund", 0.0),
        "Investment-grade bond fund": sleeve_weights.get("Investment-grade bond fund", 0.0),
        "Private real estate fund": sleeve_weights.get("Private real estate fund", 0.0),
        "Acme Corp bonds": sleeve_weights.get("Acme Corp bonds", 0.0),
        "Acme Corp stock": sleeve_weights.get("Acme Corp stock", 0.0),
    }
    return evaluate_portfolio(full_weights, HOLDINGS, reserve_min_pct)


def run_probe_test(reserve_min_pct: float = 3.0) -> bool:
    """
    Executes the negative-weight probe test:
    In Candidate A, set Cash to -2.0% and Global Equity to 64.0%.
    Verifies lowest weight reads -2.0 FAIL, reserve passes at 10.0 pass, and fails_count == 1.
    """
    probe_weights = dict(CANDIDATES["A"])
    probe_weights["Cash"] = -2.0
    probe_weights["Global equity index fund"] = 64.0

    res = evaluate_portfolio(probe_weights, HOLDINGS, reserve_min_pct)
    passed = (
        res["sum_pass"] is True and
        res["long_only_pass"] is False and
        res["reserve_pass"] is True and
        abs(res["reserve_weight"] - 10.0) < 1e-4 and
        res["liquid_pass"] is True and
        res["issuer_pass"] is True and
        res["fails_count"] == 1
    )
    return passed
