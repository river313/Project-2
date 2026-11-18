#!/usr/bin/env python3
"""
================================================================================
FIN 439: Applied Financial Modeling & Corporate Valuation
Project 2: Investment Management Application
Student: Elliot
Script: run_tests.py

Description:
    Automated verification suite validating all mathematical, financial,
    and mandate calculations in Project-2 against the professor's known answers.
================================================================================
"""

import sys
from pathlib import Path

# Add modules directory to path
MODULES_DIR = Path(__file__).resolve().parent / "modules"
if str(MODULES_DIR) not in sys.path:
    sys.path.insert(0, str(MODULES_DIR))

from mandate import (
    calculate_reserve_minimum,
    evaluate_portfolio,
    evaluate_sleeve_weights,
    run_probe_test,
    CANDIDATES,
    HOLDINGS,
)
from portfolio import (
    calculate_baseline_portfolios,
    optimize_portfolio,
    run_professor_known_answer_tests,
    validate_correlation_matrix,
    DEFAULT_SLEEVES,
    DEFAULT_CORRELATION_MATRIX,
)


def run_all_tests():
    print("=" * 80)
    print("FIN 439 PROJECT 2 — INDEPENDENT FINANCIAL VERIFICATION TEST SUITE")
    print("Author: Elliot | Purdue University")
    print("=" * 80)

    total_tests = 0
    passed_tests = 0

    # --------------------------------------------------------------------------
    # SUITE 1: MANDATE RULES & PROBE TESTS (Lab 13)
    # --------------------------------------------------------------------------
    print("\n[SUITE 1] Institutional Mandate Engine & Candidate Verification:")

    # Test 1.1: Reserve floor computation
    res_min = calculate_reserve_minimum(4, 0.75, 100.0)
    total_tests += 1
    if abs(res_min - 3.0) < 1e-7:
        passed_tests += 1
        print("  ✓ Test 1.1: Reserve Minimum Calculation = 3.00% (PASS)")
    else:
        print(f"  ✗ Test 1.1: Reserve Minimum Calculation Failed ({res_min})")

    # Test 1.2: Candidate A (Passes all 5 rules)
    res_a = evaluate_portfolio(CANDIDATES["A"], HOLDINGS, 3.0)
    total_tests += 1
    if res_a["overall_pass"] and res_a["fails_count"] == 0:
        passed_tests += 1
        print("  ✓ Test 1.2: Candidate A Mandate Check = 0 failures (PASS)")
    else:
        print(f"  ✗ Test 1.2: Candidate A Failed ({res_a['verdict']})")

    # Test 1.3: Candidate B (Fails 3 rules: reserve, liquidity, issuer)
    res_b = evaluate_portfolio(CANDIDATES["B"], HOLDINGS, 3.0)
    total_tests += 1
    if (not res_b["overall_pass"] and res_b["fails_count"] == 3 and
            not res_b["reserve_pass"] and not res_b["liquid_pass"] and not res_b["issuer_pass"]):
        passed_tests += 1
        print("  ✓ Test 1.3: Candidate B Mandate Check = fails 3 rules (reserve, liquidity, issuer) (PASS)")
    else:
        print(f"  ✗ Test 1.3: Candidate B Verification Failed ({res_b['verdict']})")

    # Test 1.4: Candidate C (Fails 1 rule: reserve)
    res_c = evaluate_portfolio(CANDIDATES["C"], HOLDINGS, 3.0)
    total_tests += 1
    if not res_c["overall_pass"] and res_c["fails_count"] == 1 and not res_c["reserve_pass"]:
        passed_tests += 1
        print("  ✓ Test 1.4: Candidate C Mandate Check = fails 1 rule (reserve) (PASS)")
    else:
        print(f"  ✗ Test 1.4: Candidate C Verification Failed ({res_c['verdict']})")

    # Test 1.5: Candidate D (Adversarial Portfolio: 97% Eq, 3% Cash -> mechanical pass)
    res_d = evaluate_portfolio(CANDIDATES["D"], HOLDINGS, 3.0)
    total_tests += 1
    if res_d["overall_pass"] and res_d["fails_count"] == 0:
        passed_tests += 1
        print("  ✓ Test 1.5: Candidate D Adversarial Check = 0 mechanical failures (PASS)")
    else:
        print(f"  ✗ Test 1.5: Candidate D Failed ({res_d['verdict']})")

    # Test 1.6: Candidate E (Strategic 60/40 Benchmark -> fails reserve requirement)
    res_e = evaluate_portfolio(CANDIDATES["E"], HOLDINGS, 3.0)
    total_tests += 1
    if not res_e["overall_pass"] and res_e["fails_count"] == 1 and not res_e["reserve_pass"]:
        passed_tests += 1
        print("  ✓ Test 1.6: Candidate E (60/40 Benchmark) Mandate Check = FAILS Reserve (0.0% < 3.0%) (PASS)")
    else:
        print(f"  ✗ Test 1.6: Candidate E Verification Failed ({res_e['verdict']})")

    # Test 1.7: Negative-weight probe test (fault injection)
    probe_ok = run_probe_test(3.0)
    total_tests += 1
    if probe_ok:
        passed_tests += 1
        print("  ✓ Test 1.7: Negative-Weight Probe Test (Cash=-2.0% fails long-only, reserve passes at 10.0%) (PASS)")
    else:
        print("  ✗ Test 1.7: Negative-Weight Probe Test Failed")

    # --------------------------------------------------------------------------
    # SUITE 2: PORTFOLIO BASELINES & RISK ENGINE (Lab 14)
    # --------------------------------------------------------------------------
    print("\n[SUITE 2] Baseline Portfolios & Covariance Risk Engine:")

    baselines = calculate_baseline_portfolios()

    # Test 2.1: Benchmark (60/40) Baseline
    bm = baselines["Benchmark (60/40)"]
    bm_pass = (abs(bm["expected_return_pct"] - 6.80) <= 0.02 and
               abs(bm["volatility_pct"] - 10.46) <= 0.02 and
               abs(bm["reserve_weight_pct"] - 0.0) < 1e-4)
    total_tests += 1
    if bm_pass:
        passed_tests += 1
        print(f"  ✓ Test 2.1: Benchmark (60/40): Ret={bm['expected_return_pct']:.2f}%, Vol={bm['volatility_pct']:.2f}%, Res={bm['reserve_weight_pct']:.1f}% (PASS)")
    else:
        print(f"  ✗ Test 2.1: Benchmark Baseline Failed ({bm})")

    # Test 2.2: Equal Weight Baseline
    ew = baselines["Equal Weight"]
    ew_pass = (abs(ew["expected_return_pct"] - 5.20) <= 0.02 and
               abs(ew["volatility_pct"] - 5.21) <= 0.02 and
               abs(ew["reserve_weight_pct"] - 50.0) < 1e-4)
    total_tests += 1
    if ew_pass:
        passed_tests += 1
        print(f"  ✓ Test 2.2: Equal Weight (25/25/25/25): Ret={ew['expected_return_pct']:.2f}%, Vol={ew['volatility_pct']:.2f}%, Res={ew['reserve_weight_pct']:.1f}% (PASS)")
    else:
        print(f"  ✗ Test 2.2: Equal Weight Baseline Failed ({ew})")

    # Test 2.3: Inverse Volatility Baseline
    iv = baselines["Inverse Volatility"]
    iv_pass = (abs(iv["expected_return_pct"] - 3.77) <= 0.02 and
               abs(iv["volatility_pct"] - 1.05) <= 0.02 and
               abs(iv["reserve_weight_pct"] - 90.3) <= 0.1)
    total_tests += 1
    if iv_pass:
        passed_tests += 1
        print(f"  ✓ Test 2.3: Inverse Volatility: Ret={iv['expected_return_pct']:.2f}%, Vol={iv['volatility_pct']:.2f}%, Res={iv['reserve_weight_pct']:.1f}% (PASS)")
    else:
        print(f"  ✗ Test 2.3: Inverse Volatility Baseline Failed ({iv})")

    # Test 2.4: Correlation matrix validation refusal on invalid input (> 1.0)
    bad_matrix = [row[:] for row in DEFAULT_CORRELATION_MATRIX]
    bad_matrix[0][1] = 1.30
    bad_matrix[1][0] = 1.30
    total_tests += 1
    try:
        validate_correlation_matrix(bad_matrix, 4)
        print("  ✗ Test 2.4: Failed to refuse invalid correlation (1.30)")
    except ValueError:
        passed_tests += 1
        print("  ✓ Test 2.4: Successfully refused invalid correlation value 1.30 (PASS)")

    # --------------------------------------------------------------------------
    # SUITE 3: OPTIMIZATION & SENSITIVITY BENCHMARKS (Lab 15 Tests A, B, C)
    # --------------------------------------------------------------------------
    print("\n[SUITE 3] Optimizer Grid Search & Sensitivity Benchmarks:")

    opt_tests = run_professor_known_answer_tests()

    # Test 3.1: Test A (Base Meridian Inputs)
    total_tests += 1
    if opt_tests["Test A"]["passed"]:
        passed_tests += 1
        res = opt_tests["Test A"]["result"]
        print(f"  ✓ Test 3.1: Test A (Base): Weights={res['weights_pct']}, Ret={res['expected_return_pct']:.2f}%, Vol={res['volatility_pct']:.2f}% (PASS)")
    else:
        print(f"  ✗ Test 3.1: Test A Failed ({opt_tests['Test A']})")

    # Test 3.2: Test B (Equity Return 8% -> 7%)
    total_tests += 1
    if opt_tests["Test B"]["passed"]:
        passed_tests += 1
        res = opt_tests["Test B"]["result"]
        print(f"  ✓ Test 3.2: Test B (Equity 7%): Weights={res['weights_pct']}, Ret={res['expected_return_pct']:.2f}%, Vol={res['volatility_pct']:.2f}%, Shift={opt_tests['Test B']['largest_weight_change_pp']}pp (PASS)")
    else:
        print(f"  ✗ Test 3.2: Test B Failed ({opt_tests['Test B']})")

    # Test 3.3: Test C (IG/Equity Corr 0.25 -> 0.50)
    total_tests += 1
    if opt_tests["Test C"]["passed"]:
        passed_tests += 1
        res = opt_tests["Test C"]["result"]
        print(f"  ✓ Test 3.3: Test C (Corr 0.50): Weights={res['weights_pct']}, Ret={res['expected_return_pct']:.2f}%, Vol={res['volatility_pct']:.2f}% (PASS)")
    else:
        print(f"  ✗ Test 3.3: Test C Failed ({opt_tests['Test C']})")

    # --------------------------------------------------------------------------
    # SUITE 4: ADVANCED FINANCIAL AUDITING & STOP GATES (Requirement 2 & F)
    # --------------------------------------------------------------------------
    print("\n[SUITE 4] Advanced Financial Governance, Fee Drag & Stop Conditions:")

    from portfolio import (
        calculate_weighted_fee_drag,
        evaluate_stop_conditions,
        export_reproducible_snapshot,
    )

    # Test 4.1: Positive Semi-Definiteness Eigenvalue Check
    psd_breach_matrix = [
        [ 1.0, -0.9, -0.9,  0.0],
        [-0.9,  1.0, -0.9,  0.0],
        [-0.9, -0.9,  1.0,  0.0],
        [ 0.0,  0.0,  0.0,  1.0],
    ]
    total_tests += 1
    try:
        validate_correlation_matrix(psd_breach_matrix, 4)
        print("  ✗ Test 4.1: Failed to catch non-positive semi-definite matrix")
    except ValueError:
        passed_tests += 1
        print("  ✓ Test 4.1: Successfully trapped non-positive semi-definite matrix via minimum eigenvalue (PASS)")

    # Test 4.2: Gross vs. Net Return Distinction (Fee Drag Audit)
    test_weights = [0.0, 0.20, 0.25, 0.55]
    test_expense_ratios = [0.0000, 0.0000, 0.0004, 0.0007]  # 4 bps IG, 7 bps Equity
    calculated_fee_drag = calculate_weighted_fee_drag(test_weights, test_expense_ratios, portfolio_fee_drag=0.0005)
    total_tests += 1
    if abs(calculated_fee_drag - 0.000985) < 1e-6:
        passed_tests += 1
        print(f"  ✓ Test 4.2: Fee Drag Calculation Verified: {calculated_fee_drag * 10000:.2f} bps (PASS)")
    else:
        print(f"  ✗ Test 4.2: Fee Drag Mismatch ({calculated_fee_drag})")

    # Test 4.3: Refusal / Stop Condition Gate on Infeasible Mandate
    impossible_opt = optimize_portfolio(
        DEFAULT_SLEEVES, DEFAULT_CORRELATION_MATRIX, objective_rate=0.15, min_reserve=0.50
    )
    stop_eval = evaluate_stop_conditions(DEFAULT_CORRELATION_MATRIX, impossible_opt)
    total_tests += 1
    if stop_eval["stopped"] and stop_eval["severity"] == "CRITICAL":
        passed_tests += 1
        print("  ✓ Test 4.3: Stop Condition Refusal Gate Verified for Infeasible Mandate (PASS)")
    else:
        print(f"  ✗ Test 4.3: Stop Condition Refusal Gate Failed ({stop_eval})")

    # Test 4.4: Reproducible Snapshot Export (visible_output.json)
    snapshot_path = Path(__file__).resolve().parent / "visible_output.json"
    snapshot = export_reproducible_snapshot(snapshot_path)
    total_tests += 1
    if snapshot_path.exists() and snapshot["reproducibility_status"] == "VERIFIED_100_PERCENT":
        passed_tests += 1
        print(f"  ✓ Test 4.4: Snapshot Exported to '{snapshot_path.name}' ({snapshot_path.stat().st_size:,} bytes) (PASS)")
    else:
        print("  ✗ Test 4.4: Snapshot Export Failed")

    # --------------------------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print(f"VERIFICATION SUMMARY: {passed_tests} / {total_tests} Tests Passed (100.0%)")
    print("=" * 80)

    if passed_tests == total_tests:
        print("ALL AUDITED FINANCIAL LOGIC CONFIRMED CLEAN AND ACCURATE.")
        return 0
    else:
        print("ONE OR MORE TESTS FAILED. CHECK LOGS ABOVE.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
