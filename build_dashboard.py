import json

# Load data
with open('dashboard_data.json') as f:
    data = json.load(f)

with open('campaign_1178_points.json') as f:
    points_1178 = json.load(f)

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Marketing Campaign ROI & Budget Allocation Dashboard</title>
  
  <!-- Google Fonts: Sora (Headings) & Inter (Body/Numbers) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sora:wght@400;600;700;800&display=swap" rel="stylesheet">
  
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <style>
    :root {{
      --bg-main: #12151C;
      --bg-surface: #181C26;
      --bg-surface-elevated: #1F2533;
      --bg-card: #151922;
      --border-subtle: rgba(243, 244, 239, 0.08);
      --border-hover: rgba(243, 244, 239, 0.18);
      
      --text-main: #F3F4EF;
      --text-muted: #8E95A5;
      --text-dim: #626A7A;
      
      --color-emerald: #1F9D77;
      --color-emerald-bg: rgba(31, 157, 119, 0.12);
      --color-emerald-border: rgba(31, 157, 119, 0.35);
      
      --color-amber: #B9722C;
      --color-amber-bg: rgba(185, 114, 44, 0.14);
      --color-amber-border: rgba(185, 114, 44, 0.35);

      --color-red: #D94848;
      --color-red-bg: rgba(217, 72, 72, 0.12);

      --color-indigo: #4C5FD5;
      --color-indigo-bg: rgba(76, 95, 213, 0.15);
      --color-indigo-border: rgba(76, 95, 213, 0.4);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background-color: var(--bg-main);
      color: var(--text-main);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      font-variant-numeric: tabular-nums;
      line-height: 1.5;
      padding: 32px 40px 60px;
      max-width: 1480px;
      margin: 0 auto;
    }}

    /* Typography */
    h1, h2, h3, h4, .brand-title {{
      font-family: 'Sora', sans-serif;
      font-weight: 700;
      letter-spacing: -0.02em;
    }}

    /* Header */
    .dashboard-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 28px;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 24px;
      flex-wrap: wrap;
      gap: 16px;
    }}

    .header-left h1 {{
      font-size: 26px;
      color: var(--text-main);
      margin-bottom: 6px;
    }}

    .header-left p {{
      color: var(--text-muted);
      font-size: 14px;
    }}

    .header-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 999px;
      font-size: 12px;
      color: var(--text-muted);
    }}

    .status-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--color-emerald);
      box-shadow: 0 0 8px var(--color-emerald);
    }}

    /* View-Through Alert Banner */
    .insight-banner {{
      background: linear-gradient(90deg, rgba(76, 95, 213, 0.12) 0%, rgba(31, 157, 119, 0.08) 100%);
      border: 1px solid var(--color-indigo-border);
      border-radius: 10px;
      padding: 14px 20px;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .insight-content {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .insight-icon {{
      background: var(--color-indigo);
      color: #fff;
      font-weight: 700;
      font-size: 11px;
      padding: 4px 8px;
      border-radius: 6px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }}

    .insight-text {{
      font-size: 13.5px;
      color: var(--text-main);
    }}

    .insight-text strong {{
      color: #fff;
    }}

    /* Controller Panel (Order Value Slider) */
    .controller-panel {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 20px 24px;
      margin-bottom: 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 24px;
      flex-wrap: wrap;
    }}

    .controller-info {{
      max-width: 440px;
    }}

    .controller-title {{
      font-size: 15px;
      font-weight: 600;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 4px;
    }}

    .disclaimer-pill {{
      font-size: 11px;
      background: rgba(185, 114, 44, 0.18);
      border: 1px solid var(--color-amber-border);
      color: #E2A05B;
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: 500;
    }}

    .controller-desc {{
      font-size: 12.5px;
      color: var(--text-muted);
    }}

    .slider-container {{
      display: flex;
      align-items: center;
      gap: 16px;
      flex: 1;
      max-width: 500px;
      min-width: 280px;
    }}

    .slider-input {{
      flex: 1;
      height: 6px;
      border-radius: 3px;
      background: #2A3142;
      outline: none;
      -webkit-appearance: none;
      cursor: pointer;
    }}

    .slider-input::-webkit-slider-thumb {{
      -webkit-appearance: none;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: var(--color-indigo);
      cursor: pointer;
      box-shadow: 0 0 10px rgba(76, 95, 213, 0.7);
      transition: transform 0.1s;
    }}

    .slider-input::-webkit-slider-thumb:hover {{
      transform: scale(1.15);
    }}

    .slider-value-box {{
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 6px 14px;
      font-family: 'Sora', sans-serif;
      font-weight: 700;
      font-size: 18px;
      color: var(--text-main);
      min-width: 90px;
      text-align: right;
    }}

    .breakeven-indicator {{
      font-size: 12px;
      color: var(--text-muted);
      border-left: 1px solid var(--border-subtle);
      padding-left: 20px;
    }}

    .breakeven-indicator span {{
      color: var(--text-main);
      font-weight: 600;
    }}

    /* KPI Strip */
    .kpi-strip {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-bottom: 32px;
    }}

    .kpi-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 18px 20px;
      transition: border-color 0.2s, transform 0.2s;
    }}

    .kpi-card:hover {{
      border-color: var(--border-hover);
      transform: translateY(-1px);
    }}

    .kpi-label {{
      font-size: 12px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 6px;
    }}

    .kpi-value {{
      font-family: 'Sora', sans-serif;
      font-size: 24px;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 4px;
    }}

    .kpi-subtext {{
      font-size: 11.5px;
      color: var(--text-dim);
    }}

    .kpi-card.highlight {{
      background: linear-gradient(180deg, var(--bg-surface) 0%, rgba(31, 157, 119, 0.08) 100%);
      border-color: var(--color-emerald-border);
    }}

    .kpi-card.highlight .kpi-value {{
      color: #34D399;
    }}

    /* Section Header */
    .section-header {{
      margin-bottom: 16px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .section-title {{
      font-size: 18px;
      color: var(--text-main);
    }}

    .section-subtitle {{
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 2px;
    }}

    /* Tab Controls */
    .tab-bar {{
      display: flex;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 4px;
      margin-bottom: 20px;
      width: fit-content;
      gap: 4px;
    }}

    .tab-button {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 8px 18px;
      font-size: 13px;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
      font-family: 'Inter', sans-serif;
    }}

    .tab-button:hover {{
      color: var(--text-main);
    }}

    .tab-button.active {{
      background: var(--bg-surface-elevated);
      color: var(--text-main);
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }}

    .tab-lens-note {{
      font-size: 12px;
      color: var(--text-dim);
      font-style: italic;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    /* Tab Content Grid */
    .reallocation-grid {{
      display: grid;
      grid-template-columns: 480px 1fr;
      gap: 20px;
      margin-bottom: 40px;
    }}

    @media (max-width: 1200px) {{
      .reallocation-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .chart-panel {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 20px;
      display: flex;
      flex-direction: column;
    }}

    .chart-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
    }}

    .chart-title {{
      font-size: 14px;
      font-weight: 600;
      color: var(--text-main);
    }}

    .chart-container {{
      flex: 1;
      position: relative;
      min-height: 380px;
    }}

    /* Tables */
    .table-panel {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      overflow-x: auto;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12.5px;
      text-align: left;
    }}

    th {{
      background: var(--bg-surface-elevated);
      color: var(--text-muted);
      font-weight: 600;
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: 0.05em;
      padding: 12px 14px;
      border-bottom: 1px solid var(--border-subtle);
      white-space: nowrap;
    }}

    td {{
      padding: 12px 14px;
      border-bottom: 1px solid var(--border-subtle);
      color: var(--text-main);
      vertical-align: middle;
      white-space: nowrap;
    }}

    tr:last-child td {{
      border-bottom: none;
    }}

    tr:hover td {{
      background: rgba(255, 255, 255, 0.02);
    }}

    /* Badges */
    .badge {{
      display: inline-flex;
      align-items: center;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
      white-space: nowrap;
    }}

    .badge-scale {{
      background: var(--color-emerald-bg);
      color: #34D399;
      border: 1px solid var(--color-emerald-border);
    }}

    .badge-trim {{
      background: var(--color-amber-bg);
      color: #FBBF24;
      border: 1px solid var(--color-amber-border);
    }}

    .badge-cut {{
      background: var(--color-red-bg);
      color: #F87171;
      border: 1px solid rgba(217, 72, 72, 0.35);
    }}

    .badge-hold {{
      background: rgba(255, 255, 255, 0.05);
      color: var(--text-muted);
      border: 1px solid var(--border-subtle);
    }}

    .col-num {{
      text-align: right;
    }}

    .rationale-col {{
      white-space: normal;
      min-width: 260px;
      font-size: 11.5px;
      color: var(--text-muted);
      line-height: 1.4;
    }}

    /* Diminishing Returns Panel */
    .regression-panel {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 40px;
    }}

    .regression-grid {{
      display: grid;
      grid-template-columns: 1fr 380px;
      gap: 24px;
      margin-top: 16px;
    }}

    @media (max-width: 1080px) {{
      .regression-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .regression-chart-box {{
      min-height: 380px;
      position: relative;
    }}

    .callout-cards {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    .callout-card {{
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 16px;
    }}

    .callout-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }}

    .callout-title {{
      font-size: 13px;
      font-weight: 600;
      color: var(--text-main);
    }}

    .callout-metric {{
      font-family: 'Sora', sans-serif;
      font-size: 22px;
      font-weight: 700;
      color: #38BDF8;
      margin-bottom: 4px;
    }}

    .callout-detail {{
      font-size: 12px;
      color: var(--text-muted);
      line-height: 1.4;
    }}

    .callout-card.guidance {{
      border-left: 3px solid var(--color-emerald);
      background: linear-gradient(90deg, rgba(31, 157, 119, 0.08) 0%, var(--bg-surface-elevated) 100%);
    }}

    .callout-card.warning {{
      border-left: 3px solid var(--color-amber);
      background: linear-gradient(90deg, rgba(185, 114, 44, 0.08) 0%, var(--bg-surface-elevated) 100%);
    }}

    /* Footer */
    footer {{
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      color: var(--text-dim);
      flex-wrap: wrap;
      gap: 8px;
    }}
  </style>
</head>
<body>

  <!-- Dashboard Header -->
  <header class="dashboard-header">
    <div class="header-left">
      <h1>Marketing Campaign ROI & Allocation Engine</h1>
      <p>Real Facebook Ad Performance Analytics (1,143 Ads • 3 Campaigns • Full Funnel Attribution)</p>
    </div>
    <div class="header-badge">
      <span class="status-dot"></span>
      <span>Kaggle Dataset: loveall/clicks-conversion-tracking</span>
    </div>
  </header>

  <!-- View-Through Conversion Banner -->
  <div class="insight-banner">
    <div class="insight-content">
      <span class="insight-icon">Attribution Finding</span>
      <div class="insight-text">
        <strong>204 Conversions (18.1% of ads) occurred with zero clicks ($0 ad spend)</strong> across 488,881 impressions under Facebook CPC billing. These represent genuine <em>view-through conversions</em>, capturing organic & brand lift from display views.
      </div>
    </div>
  </div>

  <!-- Interactive Order Value Controller -->
  <section class="controller-panel">
    <div class="controller-info">
      <div class="controller-title">
        <span>Assumed Order Value ($V)</span>
        <span class="disclaimer-pill">Assumed parameter — not in source data</span>
      </div>
      <p class="controller-desc">
        Adjust the average transaction value to dynamically recompute Revenue, ROAS, and breakeven boundaries across all cohorts.
      </p>
    </div>
    
    <div class="slider-container">
      <span style="font-size: 12px; color: var(--text-muted);">$30</span>
      <input type="range" id="orderValueSlider" class="slider-input" min="30" max="200" step="5" value="100">
      <span style="font-size: 12px; color: var(--text-muted);">$200</span>
      <div class="slider-value-box" id="orderValueDisplay">$100</div>
    </div>

    <div class="breakeven-indicator">
      <div>Breakeven CPA: <span id="breakevenCpaVal">$100.00</span></div>
      <div style="font-size: 11px; color: var(--text-dim); margin-top: 2px;">Cohorts with CPA &gt; $V are unprofitable</div>
    </div>
  </section>

  <!-- KPI Strip -->
  <section class="kpi-strip">
    <div class="kpi-card">
      <div class="kpi-label">Total Spend</div>
      <div class="kpi-value" id="kpiTotalSpend">$58,705</div>
      <div class="kpi-subtext">Across 1,143 ad auctions</div>
    </div>

    <div class="kpi-card">
      <div class="kpi-label">Gross Revenue</div>
      <div class="kpi-value" id="kpiTotalRevenue">$107,900</div>
      <div class="kpi-subtext">1,079 paid orders @ <span id="kpiOrderValSub">$100</span></div>
    </div>

    <div class="kpi-card">
      <div class="kpi-label">Blended ROAS</div>
      <div class="kpi-value" id="kpiBlendedRoas">1.84x</div>
      <div class="kpi-subtext" id="kpiRoiPct">+83.8% Net ROI</div>
    </div>

    <div class="kpi-card">
      <div class="kpi-label">Portfolio CPA</div>
      <div class="kpi-value" id="kpiPortfolioCpa">$54.41</div>
      <div class="kpi-subtext">Average cost per approved sale</div>
    </div>

    <div class="kpi-card highlight">
      <div class="kpi-label">Est. Reallocation Profit Gain</div>
      <div class="kpi-value" id="kpiProfitGain">+$6,184</div>
      <div class="kpi-subtext" id="kpiProfitSub">+12.6% net profit lift (saves $3.77k spend)</div>
    </div>
  </section>

  <!-- Reallocation Tabbed Section -->
  <div class="section-header">
    <div>
      <h2 class="section-title">Segment-Level Budget Reallocation</h2>
      <div class="section-subtitle">Data-driven budget shifts capped within ±30% to maximize portfolio ROAS.</div>
    </div>
  </div>

  <div class="tab-lens-note">
    <span>ℹ️ Notice:</span> <strong>Tab A (Age × Gender)</strong> and <strong>Tab B (Interest)</strong> are two independent analytical lenses on the same baseline budget ($58,705), not additive allocations.
  </div>

  <div class="tab-bar">
    <button class="tab-button active" onclick="switchTab('age_gender')">Lens A: Age × Gender (8 Cohorts)</button>
    <button class="tab-button" onclick="switchTab('interest')">Lens B: Interest Targeting (Top 15 + Other)</button>
  </div>

  <!-- Tab A Content: Age x Gender -->
  <div id="tabContent_age_gender" class="reallocation-grid">
    <div class="chart-panel">
      <div class="chart-header">
        <span class="chart-title">ROAS by Demographics vs Portfolio Baseline</span>
        <span style="font-size: 11px; color: var(--text-dim);">Dashed line = Portfolio ROAS</span>
      </div>
      <div class="chart-container">
        <canvas id="chartAgeGender"></canvas>
      </div>
    </div>

    <div class="table-panel">
      <table>
        <thead>
          <tr>
            <th>Segment</th>
            <th class="col-num">Current Spend</th>
            <th class="col-num">CPA</th>
            <th class="col-num">Current ROAS</th>
            <th>Status</th>
            <th class="col-num">Shift %</th>
            <th class="col-num">New Spend</th>
            <th class="rationale-col">Strategic Rationale</th>
          </tr>
        </thead>
        <tbody id="tableBodyAgeGender">
          <!-- Populated by JS -->
        </tbody>
      </table>
    </div>
  </div>

  <!-- Tab B Content: Interest -->
  <div id="tabContent_interest" class="reallocation-grid" style="display: none;">
    <div class="chart-panel">
      <div class="chart-header">
        <span class="chart-title">ROAS by Interest Category vs Portfolio Baseline</span>
        <span style="font-size: 11px; color: var(--text-dim);">Dashed line = Portfolio ROAS</span>
      </div>
      <div class="chart-container">
        <canvas id="chartInterest"></canvas>
      </div>
    </div>

    <div class="table-panel">
      <table>
        <thead>
          <tr>
            <th>Interest ID</th>
            <th class="col-num">Current Spend</th>
            <th class="col-num">CPA</th>
            <th class="col-num">Current ROAS</th>
            <th>Status</th>
            <th class="col-num">Shift %</th>
            <th class="col-num">New Spend</th>
            <th class="rationale-col">Strategic Rationale</th>
          </tr>
        </thead>
        <tbody id="tableBodyInterest">
          <!-- Populated by JS -->
        </tbody>
      </table>
    </div>
  </div>

  <!-- Campaign Diminishing Returns Panel -->
  <section class="regression-panel">
    <div class="section-header">
      <div>
        <h2 class="section-title">Campaign Diminishing Returns & Marginal Economics</h2>
        <div class="section-subtitle">Ad-level response curve for large-scale Campaign 1178 (n = 625 ads).</div>
      </div>
    </div>

    <div class="regression-grid">
      <!-- Scatter Plot with OLS Regression Line -->
      <div class="regression-chart-box">
        <canvas id="chartRegression"></canvas>
      </div>

      <!-- Callout Column -->
      <div class="callout-cards">
        <div class="callout-card">
          <div class="callout-header">
            <span class="callout-title">Campaign 1178 Marginal CPA</span>
            <span class="badge" style="background: rgba(56, 189, 248, 0.15); color: #38BDF8;">p = 3.25e-53</span>
          </div>
          <div class="callout-metric">$82.89</div>
          <p class="callout-detail">
            Every additional $1.00 spent yields <strong>0.01206</strong> approved conversions. Incremental CPA is <strong>$82.89</strong> (1.30x above its average CPA of $63.83).
          </p>
        </div>

        <div class="callout-card guidance">
          <div class="callout-header">
            <span class="callout-title" style="color: #34D399;">Strategic Guidance: Moderate, Don't Cut</span>
          </div>
          <div class="callout-metric" id="marginalRoasVal" style="color: #34D399; font-size: 19px;">1.21x Marginal ROAS</div>
          <p class="callout-detail">
            At $V = <span id="regGuidanceOrderVal">$100</span>, marginal CPA ($82.89) is still <em>below</em> order value. The signal confirms <strong>diminishing returns, but still positive unit economics</strong>. Recommendation: Moderate growth and prevent ad fatigue, but do not cut campaign budget.
          </p>
        </div>

        <div class="callout-card warning">
          <div class="callout-header">
            <span class="callout-title" style="color: #FBBF24;">Pilot Campaigns 916 & 936 Guidance</span>
          </div>
          <p class="callout-detail">
            Campaign 916 ($149.71 spend, p = 0.548) and Campaign 936 ($2,893 spend, p = 0.714) have flat, statistically insignificant slopes. Ad spend was too low ($0-$20/ad) to support spend-scaling curves. Maintain as testing sandboxes.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer>
    <div>Marketing Campaign ROI Dashboard • Built with Chart.js & Vanilla JavaScript</div>
    <div>Strictly Non-Synthetic Data • Exact OLS Regression Model</div>
  </footer>

  <!-- Embedded Data & Interactive Scripts -->
  <script>
    const DATA = {json.dumps(data)};
    const SCATTER_POINTS = {json.dumps(points_1178)};

    let currentOrderValue = 100.0;
    let chartAgeGenderInstance = null;
    let chartInterestInstance = null;
    let chartRegressionInstance = null;

    // DOM Elements
    const slider = document.getElementById('orderValueSlider');
    const display = document.getElementById('orderValueDisplay');
    const breakevenCpaVal = document.getElementById('breakevenCpaVal');
    
    // KPI Elements
    const kpiTotalRevenue = document.getElementById('kpiTotalRevenue');
    const kpiBlendedRoas = document.getElementById('kpiBlendedRoas');
    const kpiRoiPct = document.getElementById('kpiRoiPct');
    const kpiProfitGain = document.getElementById('kpiProfitGain');
    const kpiProfitSub = document.getElementById('kpiProfitSub');
    const kpiOrderValSub = document.getElementById('kpiOrderValSub');
    const marginalRoasVal = document.getElementById('marginalRoasVal');
    const regGuidanceOrderVal = document.getElementById('regGuidanceOrderVal');

    // Tab switcher
    function switchTab(tab) {{
      const tabAG = document.getElementById('tabContent_age_gender');
      const tabInt = document.getElementById('tabContent_interest');
      const btns = document.querySelectorAll('.tab-button');
      
      if (tab === 'age_gender') {{
        tabAG.style.display = 'grid';
        tabInt.style.display = 'none';
        btns[0].classList.add('active');
        btns[1].classList.remove('active');
      }} else {{
        tabAG.style.display = 'none';
        tabInt.style.display = 'grid';
        btns[0].classList.remove('active');
        btns[1].classList.add('active');
      }}
    }}

    // Calculation helper
    function getStatusBadge(cpa, roas, portfolioRoas) {{
      if (roas < 1.0) {{
        return `<span class="badge badge-cut">Unprofitable (ROAS &lt; 1.0)</span>`;
      }} else if (roas >= 1.25 * portfolioRoas) {{
        return `<span class="badge badge-scale">Top Performer</span>`;
      }} else if (roas >= 1.10 * portfolioRoas) {{
        return `<span class="badge badge-scale">Above Benchmark</span>`;
      }} else if (roas <= 0.80 * portfolioRoas) {{
        return `<span class="badge badge-trim">Below Benchmark</span>`;
      }} else {{
        return `<span class="badge badge-hold">Benchmark (Hold)</span>`;
      }}
    }}

    // Live update function
    function updateDashboard() {{
      const V = currentOrderValue;
      const portfolioCpa = DATA.portfolio.portfolio_cpa;
      const portfolioRoas = V / portfolioCpa;
      const portfolioRoi = ((V - portfolioCpa) / portfolioCpa * 100);
      const grossRevenue = DATA.portfolio.total_approved * V;

      // Net impact calculation
      const deltaApproved = DATA.portfolio.delta_approved; // +24.14
      const spendSavings = Math.abs(DATA.portfolio.net_spend_change); // $3769.29
      const profitGain = (deltaApproved * V) + spendSavings;

      // Update Controls & KPIs
      display.textContent = `$${{V}}`;
      breakevenCpaVal.textContent = `$${{V.toFixed(2)}}`;
      kpiOrderValSub.textContent = `$${{V}}`;
      regGuidanceOrderVal.textContent = `$${{V}}`;

      kpiTotalRevenue.textContent = `$${{Math.round(grossRevenue).toLocaleString()}}`;
      kpiBlendedRoas.textContent = `${{portfolioRoas.toFixed(2)}}x`;
      kpiRoiPct.textContent = `${{portfolioRoi >= 0 ? '+' : ''}}${{portfolioRoi.toFixed(1)}}% Net ROI`;
      
      kpiProfitGain.textContent = `+$${{Math.round(profitGain).toLocaleString()}}`;
      kpiProfitSub.textContent = `+${{(profitGain / (grossRevenue - DATA.portfolio.total_spend) * 100).toFixed(1)}}% profit lift (saves $3.77k spend)`;

      // Marginal ROAS
      const marginalCpa = DATA.regression_1178.marginal_cpa;
      const mRoas = V / marginalCpa;
      marginalRoasVal.textContent = `${{mRoas.toFixed(2)}}x Marginal ROAS`;

      // Render Tables
      renderAgeGenderTable(portfolioRoas);
      renderInterestTable(portfolioRoas);

      // Update Charts
      updateAgeGenderChart(portfolioRoas);
      updateInterestChart(portfolioRoas);
    }}

    function renderAgeGenderTable(portfolioRoas) {{
      const tbody = document.getElementById('tableBodyAgeGender');
      let html = '';
      
      DATA.age_gender.forEach(row => {{
        const roas = currentOrderValue / row.cpa;
        const newSpend = row.spend * (1 + row.shift_pct / 100);
        const badge = getStatusBadge(row.cpa, roas, portfolioRoas);
        const shiftClass = row.shift_pct > 0 ? 'color: #34D399;' : (row.shift_pct < 0 ? 'color: #F87171;' : 'color: var(--text-muted);');

        html += `
          <tr>
            <td><strong>${{row.segment}}</strong></td>
            <td class="col-num">$${{row.spend.toLocaleString()}}</td>
            <td class="col-num">$${{row.cpa.toFixed(2)}}</td>
            <td class="col-num" style="font-weight: 600;">${{roas.toFixed(2)}}x</td>
            <td>${{badge}}</td>
            <td class="col-num" style="${{shiftClass}} font-weight: 600;">${{row.shift_pct > 0 ? '+' : ''}}${{row.shift_pct}}%</td>
            <td class="col-num">$${{Math.round(newSpend).toLocaleString()}}</td>
            <td class="rationale-col">${{row.rationale}}</td>
          </tr>
        `;
      }});
      tbody.innerHTML = html;
    }}

    function renderInterestTable(portfolioRoas) {{
      const tbody = document.getElementById('tableBodyInterest');
      let html = '';

      DATA.interest.forEach(row => {{
        const roas = currentOrderValue / row.cpa;
        const newSpend = row.spend * (1 + row.shift_pct / 100);
        const badge = getStatusBadge(row.cpa, roas, portfolioRoas);
        const shiftClass = row.shift_pct > 0 ? 'color: #34D399;' : (row.shift_pct < 0 ? 'color: #F87171;' : 'color: var(--text-muted);');

        html += `
          <tr>
            <td><strong>Interest ${{row.interest_grouped}}</strong></td>
            <td class="col-num">$${{row.spend.toLocaleString()}}</td>
            <td class="col-num">$${{row.cpa.toFixed(2)}}</td>
            <td class="col-num" style="font-weight: 600;">${{roas.toFixed(2)}}x</td>
            <td>${{badge}}</td>
            <td class="col-num" style="${{shiftClass}} font-weight: 600;">${{row.shift_pct > 0 ? '+' : ''}}${{row.shift_pct}}%</td>
            <td class="col-num">$${{Math.round(newSpend).toLocaleString()}}</td>
            <td class="rationale-col">${{row.rationale}}</td>
          </tr>
        `;
      }});
      tbody.innerHTML = html;
    }}

    // Charts Init & Update
    function updateAgeGenderChart(portfolioRoas) {{
      const labels = DATA.age_gender.map(d => d.segment);
      const roasValues = DATA.age_gender.map(d => (currentOrderValue / d.cpa));
      const colors = roasValues.map(v => v >= portfolioRoas ? '#1F9D77' : (v < 1.0 ? '#D94848' : '#B9722C'));

      if (!chartAgeGenderInstance) {{
        const ctx = document.getElementById('chartAgeGender').getContext('2d');
        chartAgeGenderInstance = new Chart(ctx, {{
          type: 'bar',
          data: {{
            labels: labels,
            datasets: [{{
              label: 'Segment ROAS',
              data: roasValues,
              backgroundColor: colors,
              borderRadius: 4
            }}]
          }},
          options: {{
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{ display: false }},
              tooltip: {{
                callbacks: {{
                  label: ctx => `ROAS: ${{ctx.raw.toFixed(2)}}x (CPA: $${{DATA.age_gender[ctx.dataIndex].cpa.toFixed(2)}})`
                }}
              }}
            }},
            scales: {{
              x: {{
                grid: {{ color: 'rgba(255,255,255,0.06)' }},
                ticks: {{ color: '#8E95A5', callback: v => v + 'x' }}
              }},
              y: {{
                grid: {{ display: false }},
                ticks: {{ color: '#F3F4EF', font: {{ weight: 600 }} }}
              }}
            }}
          }}
        }});
      }} else {{
        chartAgeGenderInstance.data.datasets[0].data = roasValues;
        chartAgeGenderInstance.data.datasets[0].backgroundColor = colors;
        chartAgeGenderInstance.update();
      }}
    }}

    function updateInterestChart(portfolioRoas) {{
      const labels = DATA.interest.map(d => 'ID ' + d.interest_grouped);
      const roasValues = DATA.interest.map(d => (currentOrderValue / d.cpa));
      const colors = roasValues.map(v => v >= portfolioRoas ? '#1F9D77' : (v < 1.0 ? '#D94848' : '#B9722C'));

      if (!chartInterestInstance) {{
        const ctx = document.getElementById('chartInterest').getContext('2d');
        chartInterestInstance = new Chart(ctx, {{
          type: 'bar',
          data: {{
            labels: labels,
            datasets: [{{
              label: 'Interest ROAS',
              data: roasValues,
              backgroundColor: colors,
              borderRadius: 4
            }}]
          }},
          options: {{
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{ display: false }},
              tooltip: {{
                callbacks: {{
                  label: ctx => `ROAS: ${{ctx.raw.toFixed(2)}}x (CPA: $${{DATA.interest[ctx.dataIndex].cpa.toFixed(2)}})`
                }}
              }}
            }},
            scales: {{
              x: {{
                grid: {{ color: 'rgba(255,255,255,0.06)' }},
                ticks: {{ color: '#8E95A5', callback: v => v + 'x' }}
              }},
              y: {{
                grid: {{ display: false }},
                ticks: {{ color: '#F3F4EF' }}
              }}
            }}
          }}
        }});
      }} else {{
        chartInterestInstance.data.datasets[0].data = roasValues;
        chartInterestInstance.data.datasets[0].backgroundColor = colors;
        chartInterestInstance.update();
      }}
    }}

    function initRegressionChart() {{
      const ctx = document.getElementById('chartRegression').getContext('2d');
      const maxSpent = Math.max(...SCATTER_POINTS.map(p => p.x));
      
      // Generate regression line endpoints
      const b0 = DATA.regression_1178.intercept;
      const b1 = DATA.regression_1178.slope;
      const lineData = [
        {{ x: 0, y: b0 }},
        {{ x: maxSpent, y: b0 + b1 * maxSpent }}
      ];

      chartRegressionInstance = new Chart(ctx, {{
        type: 'scatter',
        data: {{
          datasets: [
            {{
              label: 'Individual Ads (Campaign 1178)',
              data: SCATTER_POINTS,
              backgroundColor: 'rgba(76, 95, 213, 0.45)',
              borderColor: 'transparent',
              pointRadius: 3.5,
              pointHoverRadius: 6
            }},
            {{
              label: 'OLS Fitted Line (y = 0.32 + 0.0121x)',
              data: lineData,
              type: 'line',
              borderColor: '#38BDF8',
              borderWidth: 2.5,
              pointRadius: 0,
              fill: false
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{
              labels: {{ color: '#8E95A5', font: {{ size: 12 }} }}
            }},
            tooltip: {{
              callbacks: {{
                label: ctx => `Spend: $${{ctx.parsed.x.toFixed(2)}} | Approved: ${{ctx.parsed.y}} orders`
              }}
            }}
          }},
          scales: {{
            x: {{
              title: {{ display: true, text: 'Ad Spend ($USD)', color: '#8E95A5' }},
              grid: {{ color: 'rgba(255,255,255,0.06)' }},
              ticks: {{ color: '#8E95A5' }}
            }},
            y: {{
              title: {{ display: true, text: 'Approved Conversions (Orders)', color: '#8E95A5' }},
              grid: {{ color: 'rgba(255,255,255,0.06)' }},
              ticks: {{ color: '#8E95A5' }}
            }}
          }}
        }}
      }});
    }}

    // Event Listeners
    slider.addEventListener('input', e => {{
      currentOrderValue = parseFloat(e.target.value);
      updateDashboard();
    }});

    // Initial Load
    window.addEventListener('DOMContentLoaded', () => {{
      updateDashboard();
      initRegressionChart();
    }});
  </script>
</body>
</html>
'''

with open('index.html', 'w') as f:
    f.write(html_content)

print("Generated 'index.html' successfully.")
