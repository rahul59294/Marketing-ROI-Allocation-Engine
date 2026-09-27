# Marketing ROI & Capital Allocation Engine

An interactive, statistically rigorous marketing performance analytics platform and capital reallocation engine built on real-world Facebook advertising campaign auction data.

Featuring parametric financial sensitivity modeling, ordinary least squares (OLS) regression for within-campaign diminishing returns, and an interactive light fintech dashboard inspired by Dribbble's Bogdan Falin / QClay aesthetic.

---

## 🌟 Key Features

1. **Statistical Verification & Audit:**
   - Evaluated synthetic vs. authentic advertising data.
   - Audited 1,143 real Facebook ads across 3 campaigns (`xyz_campaign_id`: 916, 936, 1178) from Kaggle's `loveall/clicks-conversion-tracking`.
   - Confirmed authentic advertising market dynamics: Clicks vs. Spend ($r = 0.993$), Impressions vs. Clicks ($r = 0.949$), and Spend vs. Approved Conversions ($r = 0.593$).

2. **Full-Funnel Attribution & View-Through Discovery:**
   - Delineates between direct click-through conversions and view-through conversions.
   - Identified that **204 ads generated 212 inquiries** resulting in **76 approved purchases with $0 ad spend** across 488,881 impressions under Facebook CPC bidding.

3. **Parametric Financial Modeling & Order Value Sensitivity:**
   - Labeled assumed parameter: $\text{ASSUMED\_ORDER\_VALUE} = V$ (default $V = \$100.00$, adjustable from $\$30$ to $\$200$).
   - Dynamic parameterization of:
     $$\text{ROAS}(V) = \frac{V}{\text{CPA}}, \quad \text{ROI\%}(V) = \left(\frac{V}{\text{CPA}} - 1\right) \times 100\%$$
   - Dynamic breakeven threshold identification ($\text{CPA} > V \implies \text{Unprofitable}$).

4. **Rule-Based Capital Reallocation Policy:**
   - Independent analytical lenses: **Lens A (Age × Gender)** and **Lens B (Interest Targeting)**.
   - Capped shifts within a safe operational band ($\pm 30\%$).
   - Reallocates capital from unprofitable/lagging segments (e.g., Women 45–49 at $\$119.94$ CPA) to top-performing cohorts (Men 30–34 at $\$25.55$ CPA).
   - Generates a **+$6,184 net profit lift (+12.6%)** while reducing media spend by **$3,769 (-6.4%)**.

5. **Within-Campaign Marginal Economics & Diminishing Returns:**
   - Avoids conflating disparate campaigns by estimating within-campaign response curves:
     $$\text{Approved\_Conversion}_i = 0.3208 + 0.01206 \cdot \text{Spent}_i \quad (R^2 = 0.315, p = 3.25 \times 10^{-53})$$
   - Computes **Marginal CPA = $82.89** (vs. Average CPA = $63.83, a 1.30× premium).
   - Actionable strategic guidance: Marginal CPA is below $100 order value (1.21x marginal ROAS), confirming diminishing returns but positive unit economics (**"Moderate growth, do not cut"**).
   - Notes why low-spend pilot campaigns (916 and 936) cannot support spend-scaling curves due to statistical insignificance ($p > 0.50$).

6. **Interactive Bento-Grid Fintech Dashboard:**
   - Built with pure HTML5, vanilla JavaScript, and Chart.js.
   - Light warm gray aesthetic (`#F6F5F3`) with white soft-shadow cards, pill controls, and signature coral accents (`#FF6B4A`).
   - Dynamic 3-tier concentric rings visual for demographic revenue concentration (Indigo `#4C5FD5` $\to$ Amber `#F59E0B` $\to$ Coral `#FF6B4A`).
   - Ad-level scatter plot with overlaid OLS regression line.

---

## 📊 Summary Performance Metrics ($V = \$100$)

| Cohort / Segment | Current Spend ($) | Portfolio CPA ($) | Current ROAS | Recommended Shift | New Spend ($) | Performance Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Men 30–34** | $7,640.92 | **$25.55** | **3.91x** | **+25.0%** | $9,551.15 | 🏆 Top Performer (6.82% CVR) |
| **Women 30–34** | $7,611.48 | **$39.03** | **2.56x** | **+15.0%** | $8,753.20 | 🟢 Above Benchmark |
| **Men 35–39** | $5,051.08 | **$45.10** | **2.22x** | **+15.0%** | $5,808.74 | 🟢 Above Benchmark |
| **Men 40–44** | $4,193.15 | **$54.46** | **1.84x** | **0.0%** | $4,193.15 | ⚪ Portfolio Benchmark (Hold) |
| **Women 35–39** | $6,061.35 | **$63.80** | **1.57x** | **-10.0%** | $5,455.21 | 🟡 Mildly Lagging |
| **Men 45–49** | $7,317.46 | **$76.22** | **1.31x** | **-20.0%** | $5,853.97 | 🟡 Below Benchmark |
| **Women 40–44** | $7,396.58 | **$79.53** | **1.26x** | **-20.0%** | $5,917.26 | 🟡 Below Benchmark |
| **Women 45–49** | $13,433.21 | **$119.94** | **0.83x** | **-30.0%** | $9,403.25 | 🔴 Unprofitable (CPA > $100) |
| **Portfolio Total** | **$58,705.23** | **$54.41** | **1.84x** | **-6.4%** | **$54,935.94** | **Saves $3.77k, +$6.18k Profit Lift** |

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
