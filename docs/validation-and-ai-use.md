# Project 2 Financial Validation and AI Use Register

**Course:** FIN 43900 — Applied Financial Modeling & Corporate Valuation (Purdue University)  
**Student:** Elliot  
**Client / Case Study:** Meridian Foundation Reserve ($100M Reserve Allocation)  
**Deliverable File:** `docs/validation-and-ai-use.md`  
**Status:** STEP 5A PREPARED — 18 Automated Unit Tests Passed (100%); Locked Changed-Input Record Template Prepared for Elliot's AI-Off Precommit  

---

> ### Required Opening Disclosures
> 1. **AI Use Disclosure:** This validation record documents all AI tools and models utilized during Project 2 development. All mathematical formulations, financial logic, code implementations, and testing protocols were independently reviewed, checked, and verified by Elliot.
> 2. **Regulatory & Academic Disclaimer:** This analysis is an educational demonstration prepared for FIN 43900 at Purdue University and does not constitute formal investment advice or a professional fiduciary solicitation.

---

## 1. Automated Mathematical & Financial Test Suite

All core calculations are independently tested via [`run_tests.py`](../run_tests.py). The test suite executes **18 distinct tests** across four validation suites, confirming zero numerical drift:

### Test Suite Summary:
1. **Suite 1: Mandate Constraints & Fault Injection (Lab 13 — 7 Tests):**
   - **Reserve Liquidity Floor:** $4 \times \$0.75\text{M} / \$100\text{M} = 3.00\%$ (**PASS**).
   - **Candidate A:** Mechanical check against all 5 rules (**PASS**, 0 failures).
   - **Candidate B:** Flags deficient reserve ($1.0\%$), deficient liquidity ($85.0\%$), and Acme concentration breach ($9.0\%$) (**PASS**, fails 3 rules).
   - **Candidate C:** Flags deficient reserve ($2.0\%$) while passing liquidity and concentration (**PASS**, fails 1 rule).
   - **Candidate D:** Adversarial check confirms mechanical pass with 0 failures while isolating fiduciary mismatch against Statements S4 and S9 (**PASS**).
   - **Candidate E (Benchmark 60/40):** Confirms client's policy benchmark fails the $3.0\%$ reserve floor (**PASS**, fails 1 rule).
   - **Negative-Weight Probe Test:** Injects Cash = $-2.0\%$ into Candidate A; verifies long-only failure ($-2.0\%$), reserve pass ($10.0\%$), and exact rule isolation (**PASS**).
2. **Suite 2: Covariance Risk Engine & Baselines (Lab 14 — 4 Tests):**
   - **Benchmark (60/40):** Gross Return $6.80\%$, Volatility $10.46\%$, Reserve $0.0\%$ (**PASS**).
   - **Equal Weight:** Gross Return $5.20\%$, Volatility $5.21\%$, Reserve $50.0\%$ (**PASS**).
   - **Inverse Volatility:** Gross Return $3.77\%$, Volatility $1.05\%$, Reserve $90.3\%$ (**PASS**).
   - **Correlation Refusal Gate:** Rejects correlation values outside $[-1.0, +1.0]$ by raising `ValueError` (**PASS**).
3. **Suite 3: Optimizer Grid Search & Sensitivity Benchmarks (Lab 15 — 3 Tests):**
   - **Test A (Base Meridian):** Lowest-volatility qualifying allocation = `[0% Bills, 20% 10-Yr, 25% IG, 55% Eq]`, Gross Return = $6.51\%$, Volatility = $9.44\%$ (**PASS**).
   - **Test B (Equity Return 8% -> 7%):** Qualifying allocations drop $142 \rightarrow 18$; optimal allocation shifts to `[0%, 10%, 10%, 80%]`, Gross Return = $6.53\%$, Volatility = $12.94\%$, largest weight shift = $25.0\text{ pp}$ (**PASS**).
   - **Test C (IG/Equity Correlation 0.25 -> 0.50):** Optimal allocation shifts to `[0%, 40%, 0%, 60%]`, Gross Return = $6.52\%$, Volatility = $9.73\%$, IG bonds liquidated from $25\%$ to $0\%$ (**PASS**).
4. **Suite 4: Advanced Supervisory & Fiduciary Integrity Checks (SR 26-2 — 4 Tests):**
   - **Positive Semi-Definiteness:** Computes eigenvalues of correlation matrix; verifies all $\lambda_i > 0$ ($\lambda_{\min} = 0.1704$) (**PASS**).
   - **Institutional Fee Drag Audit:** Verifies weighted fund expenses ($4.9\text{ bps}$) plus advisory drag ($10\text{ bps}$); confirms gross $6.51\%$ yields net $6.36\%$ (**PASS**).
   - **Refusal Stop Gate (Objective Rate):** Rejects unrealistic return hurdle ($15.0\%$) and confirms `feasible=False` with explicit refusal message (**PASS**).
   - **Reproducible Snapshot Sync:** Confirms [`visible_output.json`](../visible_output.json) serializes cleanly with matching keys and verified baseline data (**PASS**).

---

## 2. Locked Changed-Input Record

> [!IMPORTANT]
> **Strict Anti-Fabrication & Rubric Standard (Category 5 — 75 Points):**  
> Under course requirements, Elliot must independently select one load-bearing input with AI closed, write the prediction, and commit/push to GitHub **before** executing the model. No changed-input test may be executed prior to this precommit.
> 
> **Main Portfolio Candidate for Investment Analysis:**  
> - **Net-Return Optimized Candidate:** `[0% Treasury bills, 20% 10-year Treasuries, 20% investment-grade bonds, 60% global equities]`  
> - **Modeled Expected Net Return:** $6.51\%$ (Gross $6.66\%$, Fee Drag $15.0\text{ bps}$) vs. $6.50\%$ Objective Hurdle  
> - **Annualized Volatility:** $10.07\%$ | **Reserve Allocation:** $20.0\%$ (Passes $\ge 3.0\%$ floor)  
> - *Fiduciary Status:* Designated as the main candidate for further evaluation (not as a guaranteed or unconditionally approved investment).

### A. Pre-Execution Setup & Prediction (AI-Off, Authored by Elliot Before Running Model)

- **Input Being Changed:**  
  `[ELLIOT TO FILL OUT — e.g., Global Equity Expected Return / Reserve Liquidity Floor / Equity Ceiling / Correlation]`

- **Original Value (with units):**  
  `[ELLIOT TO FILL OUT — e.g., 8.00% / 3.00% / 100% / 0.25]`

- **New Value (with units):**  
  `[ELLIOT TO FILL OUT — e.g., 7.50% / 5.00% / 50.0% / 0.50]`

- **My Independent AI-Off Prediction:**  
  *Write your qualitative and quantitative predictions with AI tools completely closed:*  
  - *Predicted direction and magnitude of portfolio weights:* `[ELLIOT TO FILL OUT]`  
  - *Predicted direction of expected return (gross and net):* `[ELLIOT TO FILL OUT]`  
  - *Predicted direction of portfolio volatility:* `[ELLIOT TO FILL OUT]`  
  - *Predicted effect on reserve allocation and liquidity:* `[ELLIOT TO FILL OUT]`  
  - *Predicted effect on investment decision (Adopt / Allocate / Pilot / Reject / Rebalance):* `[ELLIOT TO FILL OUT]`  

- **Git Commit Hash (Pre-Run):**  
  `[ELLIOT TO FILL OUT — commit hash of this file pushed to GitHub BEFORE running test]`

- **Pre-Run Timestamp:**  
  `[ELLIOT TO FILL OUT — UTC / Local date and time of commit]`

---

### B. Actual Results (To Be Recorded AFTER Model Is Run)

*Do not populate this section until the pre-run commit above is recorded and pushed to GitHub.*

- **Execution Command Line Used:**  
  `[TO BE RECORDED POST-RUN — exact terminal command executed]`

- **Baseline Model Outputs (Before Change):**
  - Portfolio Candidate: Net-Return Optimized Candidate
  - Allocation (Bills / 10-Yr / IG / Eq): `0.0% / 20.0% / 20.0% / 60.0%`
  - Expected Gross Return: `6.66%`
  - Expected Net Return: `6.51%`
  - Portfolio Volatility: `10.07%`
  - Reserve Allocation: `20.0%`
  - Five-Day Liquidity: `100.0%`
  - Qualifying Allocations Count: `106 / 1,771`
  - Committee Decision Status: `[TO BE RECORDED]`

- **Actual Model Outputs (After Change):**
  - Allocation (Bills / 10-Yr / IG / Eq): `[TO BE RECORDED POST-RUN]`
  - Expected Gross Return: `[TO BE RECORDED POST-RUN]`
  - Expected Net Return: `[TO BE RECORDED POST-RUN]`
  - Portfolio Volatility: `[TO BE RECORDED POST-RUN]`
  - Reserve Allocation: `[TO BE RECORDED POST-RUN]`
  - Five-Day Liquidity: `[TO BE RECORDED POST-RUN]`
  - Qualifying Allocations Count: `[TO BE RECORDED POST-RUN]`
  - Committee Decision Status: `[TO BE RECORDED POST-RUN]`

---

### C. Explanation of Differences & Decision Impact Analysis

*To be authored by Elliot after model execution:*

- **Directional Accuracy:**  
  `[TO BE RECORDED POST-RUN — Did metrics move in the predicted direction? Note any unexpected shifts.]`

- **Magnitude & Numerical Differences:**  
  `[TO BE RECORDED POST-RUN — Contrast predicted numerical magnitudes with actual model outputs.]`

- **Fiduciary Decision Impact:**  
  `[TO BE RECORDED POST-RUN — Did the investment recommendation hold, require modification, or reverse completely? Why?]`

- **Model Limitation or Lesson Learned:**  
  `[TO BE RECORDED POST-RUN — What did this changed-input experiment reveal about model sensitivity or institutional constraints?]`

---

## 3. Named AI-Use Register

| Date / Phase | Assistant / Tool | Development Task | Suggestion / Output Considered | Independent Check by Elliot | Action Taken (Accept / Modify / Reject) | Effect on Model & Decision |
|---|---|---|---|---|---|---|
| **2026-11-18 (Step 1)** | Antigravity AI | Repository audit against Rubric.pdf and project requirements. | Identified file divergence between Project 1 IREN valuation and Project 2 portfolio app. | Verified file locations in workspace and past lab writeups. | **ACCEPTED**: Separated Project 2 into dedicated clean folder structure. | Prevented confusing single-company DCF with portfolio management. |
| **2026-11-18 (Step 2)** | Antigravity AI | Scaffolding `modules/` and automated test suite. | Proposed standard quadratic programming solver (`scipy.optimize`). | Checked against Lab 15 requirement for transparent, reproducible grid search. | **REJECTED**: Preserved exact 5-pp integer grid search across 1,771 allocations. | Preserves 100% reproducibility and matches professor's known answers. |
| **2026-11-18 (Step 2)** | Antigravity AI | Mandate rule evaluation in portfolio engine. | Suggested treating Statement S9 as a hard loss constraint. | Reviewed Lab 13 legal/mathematical analysis. | **MODIFIED**: Flagged S9 as "requires CIO clarification"; excluded from automated filtering. | Avoided mathematically unsound portfolio truncation. |
| **2026-11-18 (Step 4)** | Antigravity AI | Net vs. gross expected return investigation. | Investigated feasibility of $6.50\%$ net return under documented fee drag ($15\text{ bps}$). | Verified mathematical grid search with Python script. | **ACCEPTED**: Identified optimal net candidate `[0%, 20%, 20%, 60%]` ($6.51\%$ net, $10.07\%$ vol). | Resolved the core mandate hurdle contradiction for committee evaluation. |

---

## 4. Cold-Run Protocol & Environment Specifications

- **Python Version:** Python 3.13.15 (local executable: `Python-3.13.15\python.exe`)
- **Master Reproduction Command:**
  ```powershell
  python run_tests.py
  ```
  *(or on systems without global path: `& "..\Python-3.13.15\python.exe" run_tests.py`)*
- **Streamlit Launch Command:**
  ```powershell
  streamlit run app.py
  ```
