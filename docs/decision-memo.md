# Meridian Foundation Reserve — Investment Committee Decision Memo

**Target Account:** Meridian Foundation Reserve ($100.0M Total Capital Base)  
**Intended User:** Investment Committee / Chief Investment Officer  
**Author:** Elliot  
**Date / Horizon:** November 18, 2026 | Seven-Year Evaluation Horizon with Annual Rebalancing  
**Status:** DRAFT FRAMEWORK — Pending Final Model Execution & Changed-Input Test in Step 3  

---

> **Required Disclosures:**  
> 1. *AI Disclosure:* This analysis and decision support framework was developed with the assistance of artificial intelligence tools (Google Gemini / Antigravity). All calculations, logic, and final investment recommendations are the independent work and responsibility of Elliot.  
> 2. *Regulatory Disclaimer:* This document is an educational demonstration prepared for FIN 43900 at Purdue University and does not constitute formal investment advice or a professional solicitation.  

---

## 1. Executive Summary & Committee Action

- **Mandate Objective:** Preserve capital and achieve an annualized return of **CPI + 4.0%** (nominal target **6.50%** net of fees, assuming 2.50% inflation) over rolling five-year periods while supporting quarterly distributions of **$0.75M** ($3.0M annually).
- **Core Finding Across Three Portfolios:**
  1. **Equal Weight Baseline (25% each):** Holds abundant liquidity (50.0% reserve share) and low volatility (5.21%), but **fails the return objective** (5.20% vs. 6.50% required).
  2. **Strategic 60/40 Benchmark:** Clears the return hurdle (6.80% ≥ 6.50%) at 10.46% volatility, but **violates the client's own mandate** by holding **0.0% in reserve-eligible assets** (failing the mandatory 3.0% floor).
  3. **Constrained Optimized Portfolio:** Identifies an institutional allocation (**0% Bills / 20% 10-Yr / 25% IG Bonds / 55% Global Equity**) that cures the reserve breach (20.0% ≥ 3.0%), achieves the return hurdle (6.51% ≥ 6.50%), and reduces volatility to **9.44%** (-102 bps vs. 60/40 benchmark).
- **Draft Committee Recommendation:** `[PENDING FINAL REINVESTMENT DECISION: ADOPT / ALLOCATE / PILOT / REJECT]`

---

## 2. Institutional Mandate & Portfolio Universe

| Holding Sleeve | Asset Class | Reserve-Eligible? | Liquidity Window | Issuer Concentration |
|---|---|:---:|:---:|:---:|
| **Treasury bills** | Cash Equivalents / Sovereign | **Yes** | 1 business day | Exempt (U.S. Treasury) |
| **Treasury 10-year note** | Intermediate Sovereign Debt | **Yes** | 1 business day | Exempt (U.S. Treasury) |
| **Investment-grade bond fund** | Corporate / Diversified Credit | No | 3 business days | Exempt (Pooled Fund) |
| **Global equity index fund** | Public Global Equities | No | 2 business days | Exempt (Pooled Fund) |

---

## 3. Comparative Portfolio Analysis

*(To be populated with exact frozen outputs from `visible_output.json`)*

| Portfolio | Weights (Bills / 10-Yr / IG / Eq) | Expected Return | Volatility | Reserve Share | Mandate Verdict |
|---|:---:|---:|---:|---:|:---:|
| **Equal Weight** | 25.0% / 25.0% / 25.0% / 25.0% | 5.20% | 5.21% | 50.0% | **FAIL: Return Shortfall (-1.30 pp)** |
| **Strategic Benchmark (60/40)** | 0.0% / 0.0% / 40.0% / 60.0% | 6.80% | 10.46% | 0.0% | **FAIL: Reserve Floor (0.0% < 3.0%)** |
| **Constrained Optimized** | 0.0% / 20.0% / 25.0% / 55.0% | 6.51% | 9.44% | 20.0% | **PASSES EVERY CHECKABLE RULE** |

---

## 4. Risks, Monitoring Triggers, and Reversal Conditions

`[To be finalized in Step 3 after Changed-Input Test]`
- Primary operational monitor: 10-Year Treasury Yield (`DGS10`) point-in-time signal.
- Reversal triggers: Threshold breaches in equity correlation, inflation spikes above 3.5%, or portfolio drawdown exceeding risk tolerance.
