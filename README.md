# Marketing ROI & Capital Allocation Engine

An interactive, statistically rigorous marketing performance analytics platform and capital reallocation engine built on real-world Facebook advertising campaign auction data.

Featuring parametric financial sensitivity modeling, ordinary least squares (OLS) regression for within-campaign diminishing returns, hypothesis testing with Wilson Score confidence intervals, and an interactive light fintech dashboard inspired by Dribbble's Bogdan Falin / QClay aesthetic.

---

## 🌟 Key Features

1. **Statistical Verification & Significance Testing:**
   - Evaluated synthetic vs. authentic advertising data.
   - Audited 1,143 real Facebook ads across 3 campaigns (`xyz_campaign_id`: 916, 936, 1178) from Kaggle's `loveall/clicks-conversion-tracking`.
   - **Pearson's Chi-Square Test of Independence ($\chi^2 = 331.97, \text{df} = 7, p < 0.001$):** Formally rejects independence between demographic segments and purchase conversion across 38,165 clicks and 1,003 approved purchases. Conversion rate differences across segments are statistically confirmed, not random sampling noise.
   - **95% Wilson Score Confidence Intervals:** Computed for click-through conversion rates across all segments, providing robust coverage for conversion rates near zero.
   - **Hypothesis Testing for Tied Segments:** Pairwise two-proportion $z$-tests revealed that Women 30–34 and Men 35–39 are statistically indistinguishable ($z = -0.43, p = 0.67$), as are Women 35–39 and Men 45–49 ($z = 0.33, p = 0.74$). The engine groups them into shared reallocation parity tiers rather than arbitrarily ranking one over the other.

2. **Full-Funnel Attribution & View-Through Discovery:**
   - Delineates between direct click-through conversions and view-through conversions.
   - Identified that **204 zero-click ads generated 212 inquiries** resulting in **76 approved purchases across 71 ads with $0 ad spend** across 488,881 impressions under Facebook CPC bidding.

3. **Parametric Financial Modeling & Order Value Sensitivity:**
   - Labeled assumed parameter: $\text{ASSUMED\_ORDER\_VALUE} = V$ (default $V = \$100.00$, adjustable from $\$30$ to $\$200$).
   - Dynamic parameterization of:
     $$\text{ROAS}(V) = \frac{V}{\text{CPA}}, \quad \text{ROI\%}(V) = \left(\frac{V}{\text{CPA}} - 1\right) \times 100\%$$
   - Dynamic breakeven threshold identification ($\text{CPA} > V \implies \text{Below Breakeven}$).

4. **Statistically Grounded Capital Reallocation Policy:**
   - Independent analytical lenses: **Lens A (Age × Gender)** and **Lens B (Interest Targeting)**.
   - Capped shifts within a safe operational band ($\pm 30\%$).
   - **Shared Parity Tiers:** Statistically tied cohorts receive identical shift percentages (+15% for Tier 2; -15% for Tier 4) and shared rationale text.
   - **Softened & Dynamic Cohort Labeling:** Recognizes Women 45–49 as having the lowest conversion rate in the portfolio (1.14%, 95% CI [0.95%, 1.38%])—unprofitable under the default $\$100$ order value, but dynamically profitable at higher order values ($\ge \$119.94$).
   - Generates a **+$6,127 net profit lift (+12.5%)** while reducing media spend by **$3,706 (-6.3%)**.

5. **Within-Campaign Marginal Economics & Diminishing Returns:**
   - Avoids conflating disparate campaigns by estimating within-campaign response curves:
     $$\text{Approved\_Conversion}_i = 0.3208 + 0.01206 \cdot \text{Spent}_i \quad (R^2 = 0.315, p = 3.25 \times 10^{-53})$$
   - Computes **Marginal CPA = $82.89** (vs. Campaign 1178's Average CPA = $63.83, a 1.30× premium).
   - Actionable strategic guidance: Marginal CPA is below $100 order value (1.21x marginal ROAS), confirming diminishing returns but positive unit economics (**"Moderate growth, do not cut"**).
   - Explains why low-spend pilot campaigns (916 and 936) cannot support spend-scaling curves due to statistical insignificance ($p > 0.50$).

6. **Interactive Bento-Grid Fintech Dashboard:**
   - Built with pure HTML5, vanilla JavaScript, and Chart.js.
   - Light warm gray aesthetic (`#F6F5F3`) with white soft-shadow cards, pill controls, and signature coral accents (`#FF6B4A`).
   - Dynamic 3-tier concentric rings visual for demographic revenue concentration (Indigo `#4C5FD5` $\to$ Amber `#F59E0B` $\to$ Coral `#FF6B4A`).
   - Live statistical significance callout card and confidence interval pills.
   - Ad-level scatter plot with overlaid OLS regression line.

---

## 📊 Summary Performance Metrics ($V = \$100$)

| Cohort / Segment | Current Spend ($) | Portfolio CPA ($) | CVR Point Estimate (95% Wilson CI) | Current ROAS | Recommended Shift | New Spend ($) | Performance Tier & Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Men 30–34** | $7,640.92 | **$25.55** | **6.00%** [5.33%, 6.74%] | **3.91x** | **+25.0%** | $9,551.15 | 🏆 Tier 1 Leader (Highest CVR) |
| **Men 35–39** | $5,051.08 | **$45.10** | **3.72%** [3.09%, 4.46%] | **2.22x** | **+15.0%** | $5,808.74 | 🔗 Tier 2 Parity (Tied, $p=0.67$) |
| **Women 30–34** | $7,611.48 | **$39.03** | **3.53%** [3.06%, 4.07%] | **2.56x** | **+15.0%** | $8,753.20 | 🔗 Tier 2 Parity (Tied, $p=0.67$) |
| **Men 40–44** | $4,193.15 | **$54.46** | **2.85%** [2.27%, 3.57%] | **1.84x** | **0.0%** | $4,193.15 | ⚪ Tier 3 Portfolio Benchmark (Hold) |
| **Women 35–39** | $6,061.35 | **$63.80** | **2.16%** [1.76%, 2.65%] | **1.57x** | **-15.0%** | $5,152.15 | 🔗 Tier 4 Parity (Tied, $p=0.74$) |
| **Men 45–49** | $7,317.46 | **$76.22** | **2.06%** [1.68%, 2.53%] | **1.31x** | **-15.0%** | $6,219.84 | 🔗 Tier 4 Parity (Tied, $p=0.74$) |
| **Women 40–44** | $7,396.58 | **$79.53** | **1.72%** [1.40%, 2.11%] | **1.26x** | **-20.0%** | $5,917.26 | 🟡 Tier 5 Lagging Efficiency |
| **Women 45–49** | $13,433.21 | **$119.94** | **1.14%** [0.95%, 1.38%] | **0.83x** | **-30.0%** | $9,403.25 | ⚠️ Tier 6 Floor (Lowest CVR; Breakeven $119.94) |
| **Portfolio Total** | **$58,705.23** | **$54.41** | **2.63%** [2.47%, 2.79%] | **1.84x** | **-6.3%** | **$54,998.74** | **Saves $3.71k, +$6.13k Profit Lift (+12.5%)** |

---

## 🚀 Getting Started

### 1. View Dashboard Locally
The dashboard is completely self-contained in a single file with zero dependencies required:
```bash
open index.html
# Or simply double-click index.html in your file explorer
```

### 2. Run Data Processing & Analysis Pipeline
To regenerate the dataset, compute OLS regressions, and run the optimization model:
```bash
# Clone repository
git clone https://github.com/rahul59294/Marketing-ROI-Allocation-Engine.git
cd Marketing-ROI-Allocation-Engine

# Setup Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy scipy

# Execute processing pipeline
python process_and_analyze.py
python budget_reallocation_model.py
```

---

## 📁 Repository Structure

```
├── index.html                       # Standalone interactive Chart.js dashboard
├── KAG_conversion_data.csv          # Real Facebook ads dataset (loveall/clicks-conversion-tracking)
├── cleaned_ad_level_performance.csv # Cleaned & feature-engineered ad dataset
├── dashboard_data.json              # Processed aggregation & regression stats
├── campaign_1178_points.json        # 625 ad-level scatter plot data points
├── process_and_analyze.py           # Data audit, cleaning & OLS regression script
├── budget_reallocation_model.py     # Rule-based budget reallocation engine
├── build_optimized_dashboard.py     # HTML dashboard build script
└── README.md                        # Documentation
```

---

## 📄 License
MIT License. Created for marketing analytics and capital allocation modeling.
