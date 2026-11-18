# Meridian Foundation Reserve — Investment Management Application

**Course:** FIN 43900 — Applied Financial Modeling & Corporate Valuation (Purdue University)  
**Student / Author:** Elliot  
**Client / Case Study:** Meridian Foundation Reserve ($100M Total Reserve Fund)  
**Evaluation Horizon:** Seven Years with Annual Rebalancing  

---

> ### Required Opening Disclosures
> 1. **AI Use Disclosure:** This investment management application and portfolio analysis system was designed and constructed with the assistance of artificial intelligence tools (Google Gemini / Antigravity). All architectural decisions, mathematical logic, financial interpretations, and final committee recommendations are the independent work and responsibility of Elliot.
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

| Portfolio | Weights (Bills / 10-Yr / IG / Eq) | Gross Return | Net Return | Volatility | Reserve Share | Mandate Verdict |
|---|:---:|---:|---:|---:|:---:|:---:|
| **Equal Weight** | 25.0% / 25.0% / 25.0% / 25.0% | 5.20% | 5.07% | 5.21% | 50.0% | **FAIL: Return Target (-1.43 pp net)** |
| **Strategic 60/40 Benchmark** | 0.0% / 0.0% / 40.0% / 60.0% | 6.80% | 6.64% | 10.46% | 0.0% | **FAIL: Reserve Floor (0.0% < 3.0%)** |
| **Lab 15 Baseline Optimal** | 0.0% / 20.0% / 25.0% / 55.0% | 6.51% | 6.36% | 9.44% | 20.0% | **PASSES HARD RULES; Short on Net** |
| **Net-Return Candidate** | 0.0% / 20.0% / 20.0% / 60.0% | 6.66% | 6.51% | 10.07% | 20.0% | **PASSES ALL RULES & NET HURDLE** |

*Note on Net-Return Candidate:* Per investment committee guidelines, the Net-Return Optimized portfolio is designated as the primary candidate for further evaluation (not as a guaranteed or unconditionally approved investment).
