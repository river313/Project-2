# Data Card: 10-Year Treasury Constant Maturity Rate (DGS10)

**Course:** FIN 43900 — Applied Financial Modeling & Corporate Valuation (Purdue University)  
**Student:** Elliot  
**Client / Case Study:** Meridian Foundation Reserve ($100M Reserve Allocation)  
**Module Lineage:** Lab 16 (Provenance Gate) & Lab 17 (Point-in-Time Audit)  
**As-of Cutoff Date:** October 5, 2026 (Annual Rebalancing Review)  

---

## 1. Provenance and Metadata

| Field | Description / Verified Specification |
|---|---|
| **Series Name** | 10-Year Treasury Constant Maturity Rate |
| **Series ID** | [DGS10](https://fred.stlouisfed.org/series/DGS10) |
| **Data Provider** | Board of Governors of the Federal Reserve System / U.S. Department of the Treasury |
| **Source Endpoints** | • FRED (Current): `https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10`<br>• ALFRED (Vintage): `https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=YYYY-MM-DD` |
| **Units** | Percent (%), Not Seasonally Adjusted |
| **Frequency** | Daily (business trading days) |
| **Reporting Lag** | 1 Business Day (published late afternoon following market close; Monday trades reflect Friday close) |
| **Revision Characteristics** | Market yields are transaction-based and unrevised (0 revisions observed in sample) |

---

## 2. Point-in-Time Verification (Cutoff: October 5, 2026)

The table below reconciles what was known to an investment committee meeting on **October 5, 2026** against current database values:

| Provenance Metric | Vintage Known on Oct 5, 2026 | Current Value Today | Discrepancy / Revision | Verification Status |
|---|---:|---:|---:|:---:|
| **Latest Known Date** | **October 2, 2026** (Friday) | October 27, 2026 | +17 Trading Days | **MATCH (PASS)** |
| **Observed Yield** | **5.28%** | 4.99% | -29 bps market change | **MATCH (PASS)** |
| **Historical Observations Revised** | — | — | **0 revisions** | **MATCH (PASS)** |

### Look-Ahead Bias Prevention Rationale:
On Monday, October 5, 2026, the trading session had not yet closed. A committee making portfolio decisions at 10:00 AM could know yields only through Friday, October 2, 2026 (**5.28%**). Utilizing the subsequent October 27 yield (**4.99%**) or assuming instant same-day yield knowledge creates forward leakage and distorts historical tracking.

---

## 3. Institutional Relevance to Meridian Foundation Mandate

1. **Direct Universe Inclusion (Statement S3):**
   - The Meridian Foundation holds **Treasury 10-year notes** as an approved sovereign instrument qualifying toward the mandatory **3.0% reserve liquidity floor** ($3.0M for 4 quarters of $0.75M disbursements).
   - In the baseline optimization, Treasury 10-year notes capture a **20.0% allocation** ($20.0M), making the 10-year yield a primary driver of reserve yield and interest rate duration risk.
2. **Benchmark Sovereign Fixed Income Anchor (Statement S4):**
   - Statement S4 establishes a strategic policy benchmark of **60% Global Equities / 40% U.S. Investment-Grade Bonds**.
   - The 10-year Treasury yield anchors the risk-free term premium for the Investment-Grade Bond Fund sleeve and governs the duration-risk profile of the reserve fund.
3. **Point-in-Time Signal Role for Project 2:**
   - Serves as the primary macroeconomic state variable for annual rebalancing decisions.
   - When 10-year yields fluctuate, the opportunity cost between cash equivalents (Treasury bills) and intermediate sovereign debt (10-year notes) shifts, directly altering the optimal reserve structure.
