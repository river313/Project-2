# Meridian Foundation Reserve — Investment Management Application

**Course:** FIN 43900 — Applied Financial Modeling & Corporate Valuation (Purdue University)  
**Student / Author:** Elliot  
**Client / Case Study:** Meridian Foundation Reserve ($100M Total Reserve Fund)  
**Evaluation Horizon:** Seven Years with Annual Rebalancing  

---

> ### Required Opening Disclosures
> 1. **AI Use Disclosure:** This investment management application, quantitative risk engine, and portfolio documentation were developed with the assistance of artificial intelligence tools (Google Gemini / Antigravity) for code generation, architectural scaffolding, and preliminary drafting. Elliot directed the project design, established the mandate constraints and test cases, independently authored the pre-execution AI-off predictions, reviewed and verified all executed outputs, and bears ultimate student responsibility for the analysis and decision framework.
> 2. **Regulatory & Academic Disclaimer:** This application is an educational demonstration prepared for FIN 43900 at Purdue University and does not constitute formal investment advice or a professional fiduciary solicitation.

---

## 1. Quick Start: One Command to Reproduce Results

### Prerequisites & Dependency Installation
From the `Project-2` directory, install required packages:
```powershell
pip install -r requirements.txt
```

### Reproduce All Verification Tests (Automated Test Suite)
To independently verify all financial calculations, mandate constraints, and sensitivity benchmarks:
```powershell
python run_tests.py
```
*(On local environments where Python is not in system PATH, run: `& "..\Python-3.13.15\python.exe" run_tests.py`)*

### Launch the Interactive Streamlit Web Application
To run the interactive portfolio management application in your browser:
```powershell
streamlit run app.py
```
*(On local environments: `& "..\Python-3.13.15\python.exe" -m streamlit run app.py`)*

---

## 2. Project Architecture & Directory Structure

```text
Project-2/
├── .gitignore                              # Excludes bytecode, environments, and secrets
├── app.py                                  # Main Streamlit web application (5 interactive tabs)
├── run_tests.py                            # Automated verification test suite (18 tests)
├── requirements.txt                        # Pinned project dependencies
├── README.md                               # Project overview and reproduction instructions
├── project_audit.py                        # Manifest audit checker
├── project-submission-manifest-template.csv # 12-row submission manifest
├── visible_output.json                     # Audited frozen financial snapshot
├── modules/
│   ├── mandate.py                          # Lab 13 institutional mandate evaluation engine
│   ├── portfolio.py                        # Lab 14-15 risk engine, baselines, and grid optimizer
│   └── point_in_time.py                    # Lab 16-17 FRED/ALFRED PIT interest rate engine
├── docs/
│   ├── decision-memo.md                    # Investment committee recommendation & decision memo
│   ├── validation-and-ai-use.md            # Validation record & Locked Changed-Input Record
│   └── data-card-dgs10.md                  # Audited Data Card for 10-Year Treasury Yield (DGS10)
└── data/                                   # Historical series & cached inputs
```

---

## 3. Core Mandate & Portfolio Summary

- **Total Reserve Fund Size:** $100.0 Million
- **Quarterly Outflow Commitment:** $0.75 Million ($3.0 Million annually)
- **Mandated Cash/Treasury Floor:** Twelve months of distributions held exclusively in daily-liquid sovereign debt ($4 \times \$0.75\text{M} = \$3.0\text{M}$, or **3.0%**)
- **Nominal Return Hurdle:** CPI Baseline ($2.5\%$) + Real Growth Target ($4.0\%$) = **6.50% net of investment costs**
- **Five-Day Liquidity:** Minimum **90.0%** of portfolio redeemable within 5 business days
- **Single-Company Concentration:** Maximum **8.0%** in any single non-exempt corporate issuer

### Portfolio Comparison Summary:

| Portfolio Specification | Weights (Bills / 10-Yr / IG / Eq) | Gross Return | Total Drag | Net Return | Annual Volatility (σ) | Reserve Share | 1-Yr 5th Pct Net Return | Mandate Verdict |
|---|:---:|---:|---:|---:|---:|---:|---:|:---:|
| **Equal Weight** | 25.0% / 25.0% / 25.0% / 25.0% | 5.20% | 12.8 bps | 5.07% | 5.21% | 50.0% | -3.50% | **FAIL: Return Target (-1.43 pp net)** |
| **Strategic 60/40 Benchmark** | 0.0% / 0.0% / 40.0% / 60.0% | 6.80% | 15.8 bps | 6.64% | 10.46% | 0.0% | -10.57% | **FAIL: Reserve Floor (0.0% < 3.0%)** |
| **Portfolio C (Gross Opt)** | 0.0% / 20.0% / 25.0% / 55.0% | 6.51% | 14.8 bps | 6.36% | 9.44% | 20.0% | -9.17% | **FAIL: Net Hurdle (-14 bps net)** |
| **Portfolio D (Net Candidate)** | 0.0% / 20.0% / 20.0% / 60.0% | 6.66% | 15.0 bps | 6.51% | 10.07% | 20.0% | -10.05% | **Passes evaluated mechanical constraints (S3, S5, S6) & net hurdle (S4); S9 unresolved** |

*Note on Portfolio D:* Proposed for a **Conditional Pilot Allocation ($20M)** requiring Elliot's and Committee approval, with formal monitoring triggers, rather than an unconditional $100M commitment. Remaining $80M is retained in existing sovereign cash/short Treasuries (compliance is not asserted for unallocated funds). Modeled net return (6.51%) clears the 6.50% hurdle by a narrow 1.0 bp margin of safety.

*Stress Testing Disclosure:* Stress Vector 4 (Historical Observation Window: "All Months" vs. "Last 36 Months") is reported as incomplete / not executed because no legitimate monthly historical price series CSV was supplied. In strict compliance with anti-fabrication standards, no synthetic price series were fabricated.

### Phase 2 Changed-Input Experiment (Global Equity Return: 8.00% → 7.50%):
- **Pre-Execution Locked Commit:** [`657453e`](https://github.com/river313/Project-2/commit/657453e4c2e756adcb715aee07bdaca804a8dd83)
- **Completed Experiment Commit:** [`010d658`](https://github.com/river313/Project-2/commit/010d658abea60afc35a50fb74803d885b29c9a04)
- **Case 1 (Fixed-Weight Portfolio D):** Net return drops to **6.21%** (breaches 6.50% hurdle by -29 bps).
- **Case 2 (Grid-Search Reoptimization):** Shifts to `[0%, 10%, 20%, 70%]`, clearing net return (6.52%) but surging volatility to **11.57%** (+150 bps) and 95% VaR to **-12.51%** (P(Loss > 10%) = 7.66%).
- **Fiduciary Impact:** Reversal of recommendation—committee rejects automated reoptimization to prevent excessive equity tail risk.
