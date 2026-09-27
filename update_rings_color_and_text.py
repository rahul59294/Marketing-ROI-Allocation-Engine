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
  <title>Marketing Campaign ROI & Allocation Dashboard</title>

  <!-- Google Fonts: Sora (Headings) & Inter (Body/Data) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@500;600;700;800&display=swap" rel="stylesheet">

  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <style>
    :root {{
      --bg-page: #F6F5F3;
      --bg-card: #FFFFFF;
      --bg-subtle: #F9F8F6;
      --bg-muted: #EDE9E3;
      --border-subtle: rgba(25, 27, 31, 0.05);

      --text-primary: #181A1F;
      --text-secondary: #5F6675;
      --text-muted: #8D94A3;

      /* Distinct Tiering Colors */
      --tier-portfolio: #4C5FD5; /* Indigo / Slate Blue */
      --tier-top3: #F59E0B;      /* Warm Amber / Gold */
      --tier-hero: #FF6B4A;      /* Vibrant Signature Coral */

      --accent-coral: #FF6B4A;
      --accent-coral-hover: #F25734;
      --accent-coral-tint: rgba(255, 107, 74, 0.09);
      --accent-coral-light: #FFF2EE;

      --color-dark: #15181E;
      --color-dark-surface: #20242D;
      
      --color-emerald: #1F9D77;
      --color-emerald-tint: rgba(31, 157, 119, 0.10);

      --radius-card: 24px;
      --radius-md: 14px;
      --radius-pill: 9999px;

      --shadow-card: 0 10px 30px rgba(25, 27, 31, 0.035), 0 2px 6px rgba(25, 27, 31, 0.02);
      --shadow-hover: 0 16px 36px rgba(25, 27, 31, 0.06), 0 4px 10px rgba(25, 27, 31, 0.025);
      --shadow-coral: 0 12px 28px rgba(255, 107, 74, 0.28);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html, body {{
      width: 100%;
      overflow-x: hidden;
    }}

    body {{
      background-color: var(--bg-page);
      color: var(--text-primary);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      font-variant-numeric: tabular-nums;
      line-height: 1.45;
      padding: 28px 36px 60px;
      max-width: 1440px;
      margin: 0 auto;
      -webkit-font-smoothing: antialiased;
    }}

    /* Typography */
    h1, h2, h3, h4, .brand-title {{
      font-family: 'Sora', sans-serif;
      font-weight: 700;
      letter-spacing: -0.025em;
      color: var(--text-primary);
    }}

    /* Header Bar */
    .dashboard-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      flex-wrap: wrap;
      gap: 16px;
    }}

    .header-branding {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .brand-avatar {{
      width: 42px;
      height: 42px;
      background: var(--color-dark);
      color: #FFFFFF;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Sora', sans-serif;
      font-weight: 800;
      font-size: 18px;
      box-shadow: 0 4px 12px rgba(21, 24, 30, 0.15);
    }}

    .brand-text h1 {{
      font-size: 20px;
      line-height: 1.2;
    }}

    .brand-text p {{
      font-size: 12.5px;
      color: var(--text-secondary);
    }}

    /* Order Value Controller Pill */
    .order-controller-pill {{
      background: var(--bg-card);
      padding: 8px 12px 8px 18px;
      border-radius: var(--radius-pill);
      border: 1px solid var(--border-subtle);
      box-shadow: var(--shadow-card);
      display: flex;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
    }}

    .controller-labels {{
      display: flex;
      flex-direction: column;
    }}

    .controller-title {{
      font-size: 12px;
      font-weight: 600;
      color: var(--text-primary);
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .assumed-tag {{
      background: var(--accent-coral-light);
      color: var(--accent-coral);
      font-size: 10px;
      font-weight: 600;
      padding: 1px 7px;
      border-radius: var(--radius-pill);
    }}

    .controller-caption {{
      font-size: 11px;
      color: var(--text-muted);
    }}

    .slider-wrap {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .slider-wrap span {{
      font-size: 11.5px;
      font-weight: 500;
      color: var(--text-secondary);
    }}

    .range-input {{
      width: 140px;
      height: 6px;
      border-radius: var(--radius-pill);
      background: var(--bg-muted);
      outline: none;
      -webkit-appearance: none;
      cursor: pointer;
    }}

    .range-input::-webkit-slider-thumb {{
      -webkit-appearance: none;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: var(--accent-coral);
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(255, 107, 74, 0.45);
      transition: transform 0.15s ease;
    }}

    .range-input::-webkit-slider-thumb:hover {{
      transform: scale(1.15);
    }}

    .val-display-pill {{
      background: var(--color-dark);
      color: #FFFFFF;
      font-family: 'Sora', sans-serif;
      font-weight: 700;
      font-size: 13.5px;
      padding: 6px 14px;
      border-radius: var(--radius-pill);
      min-width: 62px;
      text-align: center;
    }}

    /* Global Bento Grid Alignment */
    .bento-row {{
      display: grid;
      gap: 20px;
      margin-bottom: 24px;
      width: 100%;
    }}

    /* Hero Row: 4 equal cards */
    .bento-hero-row {{
      grid-template-columns: repeat(4, 1fr);
    }}

    @media (max-width: 1180px) {{
      .bento-hero-row {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}

    @media (max-width: 680px) {{
      .bento-hero-row {{
        grid-template-columns: 1fr;
      }}
    }}

    /* Common Card Styling */
    .bento-card {{
      background: var(--bg-card);
      border-radius: var(--radius-card);
      border: 1px solid var(--border-subtle);
      padding: 24px;
      box-shadow: var(--shadow-card);
      position: relative;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
      min-width: 0;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .bento-card:hover {{
      box-shadow: var(--shadow-hover);
    }}

    .card-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
    }}

    .card-label {{
      font-size: 12.5px;
      font-weight: 500;
      color: var(--text-secondary);
    }}

    .icon-circle {{
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: var(--accent-coral-tint);
      color: var(--accent-coral);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
    }}

    .hero-num-huge {{
      font-family: 'Sora', sans-serif;
      font-size: 32px;
      font-weight: 700;
      color: var(--text-primary);
      letter-spacing: -0.03em;
      line-height: 1.1;
    }}

    .hero-sub {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 4px;
      line-height: 1.4;
    }}

    /* Hero Card 1 footer split */
    .card-foot-split {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      padding-top: 14px;
      margin-top: 14px;
      border-top: 1px solid var(--bg-muted);
    }}

    .foot-stat-num {{
      font-family: 'Sora', sans-serif;
      font-size: 15px;
      font-weight: 700;
      color: var(--text-primary);
    }}

    .foot-stat-lbl {{
      font-size: 11px;
      color: var(--text-secondary);
    }}

    /* Hero Card 2: Standout Coral */
    .bento-card-coral {{
      background: linear-gradient(135deg, #FF6B4A 0%, #FA532E 100%);
      color: #FFFFFF;
      box-shadow: var(--shadow-coral);
      border: none;
    }}

    .bento-card-coral .card-label {{
      color: rgba(255, 255, 255, 0.88);
    }}

    .bento-card-coral .hero-num-huge {{
      color: #FFFFFF;
    }}

    .bento-card-coral .hero-sub {{
      color: rgba(255, 255, 255, 0.9);
    }}

    .coral-save-tag {{
      display: inline-flex;
      align-items: center;
      background: rgba(255, 255, 255, 0.22);
      backdrop-filter: blur(8px);
      padding: 5px 12px;
      border-radius: var(--radius-pill);
      font-size: 11.5px;
      font-weight: 600;
      color: #FFFFFF;
      margin-top: 14px;
      width: fit-content;
    }}

    /* Hero Card 3: Dark Circular Gauge */
    .bento-card-dark {{
      background: var(--color-dark);
      color: #FFFFFF;
      align-items: center;
      text-align: center;
      justify-content: center;
      border: none;
    }}

    .gauge-box {{
      position: relative;
      width: 104px;
      height: 104px;
      margin-bottom: 10px;
    }}

    .gauge-svg {{
      width: 100%;
      height: 100%;
      transform: rotate(-90deg);
    }}

    .gauge-bg-ring {{
      fill: none;
      stroke: var(--color-dark-surface);
      stroke-width: 8;
    }}

    .gauge-val-ring {{
      fill: none;
      stroke: var(--accent-coral);
      stroke-width: 8;
      stroke-linecap: round;
      stroke-dasharray: 282.74;
      stroke-dashoffset: 70;
      transition: stroke-dashoffset 0.5s ease;
    }}

    .gauge-center-text {{
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-family: 'Sora', sans-serif;
      font-weight: 700;
      font-size: 20px;
      color: #FFFFFF;
    }}

    .gauge-title {{
      font-size: 12.5px;
      font-weight: 600;
      color: #FFFFFF;
    }}

    .gauge-caption {{
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 2px;
    }}

    /* Pill Badges */
    .status-badge {{
      display: inline-flex;
      align-items: center;
      padding: 3px 9px;
      border-radius: var(--radius-pill);
      font-size: 11px;
      font-weight: 600;
    }}

    .badge-cpc {{
      background: var(--accent-coral-tint);
      color: var(--accent-coral);
    }}

    /* Row 2: Reallocation & Demographic Tiering (2-col Bento) */
    .bento-middle-row {{
      grid-template-columns: 360px 1fr;
    }}

    @media (max-width: 1100px) {{
      .bento-middle-row {{
        grid-template-columns: 1fr;
      }}
    }}

    /* Concentric Radial Progress Rings Card */
    .radial-top-stat-block {{
      margin-bottom: 12px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--bg-muted);
    }}

    .radial-stat-lbl {{
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
    }}

    .radial-stat-val {{
      font-family: 'Sora', sans-serif;
      font-size: 26px;
      font-weight: 800;
      color: var(--text-primary);
      margin: 2px 0 1px;
      line-height: 1.15;
    }}

    .radial-stat-caption {{
      font-size: 11.5px;
      color: var(--text-secondary);
    }}

    .radial-rings-container {{
      width: 100%;
      height: 170px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 6px 0 12px;
      position: relative;
    }}

    .radial-svg {{
      width: 160px;
      height: 160px;
      transform: rotate(-90deg);
    }}

    .ring-track {{
      fill: none;
      stroke: #EDE8E2;
      stroke-linecap: round;
    }}

    .ring-progress {{
      fill: none;
      stroke-linecap: round;
      transition: stroke-dashoffset 0.5s ease;
    }}

    .concentric-item-list {{
      display: flex;
      flex-direction: column;
      gap: 9px;
      border-top: 1px solid var(--bg-muted);
      padding-top: 14px;
      margin-bottom: 12px;
    }}

    .concentric-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
    }}

    .concentric-row-left {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .dot-marker {{
      width: 9px;
      height: 9px;
      border-radius: 50%;
      display: inline-block;
    }}

    /* Separate CPA Callout below concentric rings */
    .hero-cpa-callout {{
      background: var(--bg-subtle);
      border-radius: var(--radius-md);
      padding: 12px 14px;
      border: 1px solid var(--border-subtle);
    }}

    /* Tabbed Reallocation Engine Card */
    .tabbed-engine-card {{
      background: var(--bg-card);
      border-radius: var(--radius-card);
      border: 1px solid var(--border-subtle);
      padding: 24px;
      box-shadow: var(--shadow-card);
      min-width: 0;
    }}

    .engine-head-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .nav-pills {{
      display: flex;
      background: var(--bg-subtle);
      padding: 4px;
      border-radius: var(--radius-pill);
      gap: 4px;
    }}

    .nav-pill-btn {{
      border: none;
      background: transparent;
      padding: 7px 16px;
      border-radius: var(--radius-pill);
      font-family: 'Inter', sans-serif;
      font-size: 12.5px;
      font-weight: 600;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .nav-pill-btn.active {{
      background: var(--color-dark);
      color: #FFFFFF;
      box-shadow: 0 2px 8px rgba(21, 24, 30, 0.15);
    }}

    .lens-info-pill {{
      font-size: 11.5px;
      color: var(--text-muted);
      background: var(--bg-subtle);
      padding: 5px 12px;
      border-radius: var(--radius-pill);
    }}

    /* 2-Column Split inside Reallocation Lens */
    .lens-inner-grid {{
      display: grid;
      grid-template-columns: 320px 1fr;
      gap: 20px;
      min-width: 0;
    }}

    @media (max-width: 980px) {{
      .lens-inner-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .bar-chart-container {{
      height: 380px;
      position: relative;
      min-width: 0;
    }}

    /* Styled Card-Rows for Table */
    .cards-table-scroll {{
      display: flex;
      flex-direction: column;
      gap: 8px;
      max-height: 400px;
      overflow-y: auto;
      padding-right: 4px;
      min-width: 0;
    }}

    .cards-table-scroll::-webkit-scrollbar {{
      width: 4px;
    }}
    .cards-table-scroll::-webkit-scrollbar-thumb {{
      background: var(--bg-muted);
      border-radius: 4px;
    }}

    .cohort-card-row {{
      background: var(--bg-subtle);
      border-radius: var(--radius-md);
      padding: 12px 16px;
      display: grid;
      grid-template-columns: 120px 1fr 75px 70px 75px;
      align-items: center;
      gap: 12px;
      transition: background 0.15s ease;
      min-width: 0;
    }}

    .cohort-card-row:hover {{
      background: #F1ECE6;
    }}

    .col-cohort strong {{
      font-size: 13px;
      color: var(--text-primary);
      display: block;
      white-space: nowrap;
    }}

    .col-cohort span {{
      font-size: 11px;
      color: var(--text-muted);
      white-space: nowrap;
    }}

    .col-metrics {{
      font-size: 11.5px;
      color: var(--text-secondary);
      line-height: 1.35;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .col-roas {{
      font-family: 'Sora', sans-serif;
      font-weight: 700;
      font-size: 15px;
      color: var(--text-primary);
      text-align: right;
      white-space: nowrap;
    }}

    .col-roas small {{
      display: block;
      font-size: 10px;
      font-weight: 500;
      color: var(--text-muted);
    }}

    .shift-tag {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 4px 9px;
      border-radius: var(--radius-pill);
      font-weight: 700;
      font-size: 11.5px;
      white-space: nowrap;
    }}

    .shift-pos {{
      background: var(--color-emerald-tint);
      color: var(--color-emerald);
    }}

    .shift-neg {{
      background: rgba(255, 107, 74, 0.12);
      color: var(--accent-coral);
    }}

    .shift-zero {{
      background: var(--bg-muted);
      color: var(--text-secondary);
    }}

    .col-new-spend {{
      text-align: right;
      font-size: 12.5px;
      font-weight: 600;
      color: var(--text-primary);
      white-space: nowrap;
    }}

    /* Row 3: Campaign Diminishing Returns (2-col Bento) */
    .bento-bottom-row {{
      grid-template-columns: 1fr 360px;
    }}

    @media (max-width: 1080px) {{
      .bento-bottom-row {{
        grid-template-columns: 1fr;
      }}
    }}

    .scatter-chart-wrap {{
      height: 340px;
      position: relative;
      margin-top: 10px;
      min-width: 0;
    }}

    .diminishing-stack {{
      display: flex;
      flex-direction: column;
      gap: 16px;
      min-width: 0;
    }}

    .side-stat-box {{
      background: var(--bg-card);
      border-radius: var(--radius-card);
      border: 1px solid var(--border-subtle);
      padding: 20px 22px;
      box-shadow: var(--shadow-card);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .box-stat-coral {{
      font-family: 'Sora', sans-serif;
      font-size: 24px;
      font-weight: 700;
      color: var(--accent-coral);
      margin-bottom: 2px;
    }}

    .guidance-banner {{
      background: var(--bg-subtle);
      border-left: 3px solid var(--accent-coral);
      padding: 12px 14px;
      border-radius: 0 var(--radius-md) var(--radius-md) 0;
      margin-top: 10px;
    }}

    .guidance-banner strong {{
      font-size: 12.5px;
      color: var(--text-primary);
      display: block;
      margin-bottom: 2px;
    }}

    .guidance-banner p {{
      font-size: 11.5px;
      color: var(--text-secondary);
      line-height: 1.4;
    }}

    /* Footer */
    footer {{
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid var(--bg-muted);
      display: flex;
      justify-content: space-between;
      font-size: 11.5px;
      color: var(--text-muted);
      flex-wrap: wrap;
      gap: 8px;
    }}
  </style>
</head>
<body>

  <!-- Top Header Bar -->
  <header class="dashboard-header">
    <div class="header-branding">
      <div class="brand-avatar">M</div>
      <div class="brand-text">
        <h1>Marketing Campaign ROI Dashboard</h1>
        <p>Capital Allocation &amp; Diminishing Returns Engine • Authentic Facebook Ads Dataset</p>
      </div>
    </div>

    <!-- Order Value Controller -->
    <div class="order-controller-pill">
      <div class="controller-labels">
        <div class="controller-title">
          <span>Assumed Order Value</span>
          <span class="assumed-tag">Assumed Parameter</span>
        </div>
        <span class="controller-caption">Not in raw source data • Live recalibration</span>
      </div>

      <div class="slider-wrap">
        <span>$30</span>
        <input type="range" id="orderValueSlider" class="range-input" min="30" max="200" step="5" value="100">
        <span>$200</span>
      </div>

      <div class="val-display-pill" id="orderValueDisplay">$100</div>
    </div>
  </header>

  <!-- Bento Grid Hero (4 Cards) -->
  <section class="bento-row bento-hero-row">
    
    <!-- Hero Card 1: Gross Revenue -->
    <div class="bento-card">
      <div>
        <div class="card-head">
          <span class="card-label">Portfolio Gross Revenue</span>
          <div class="icon-circle">📈</div>
        </div>
        <div class="hero-num-huge" id="kpiGrossRevenue">$107,900</div>
        <div class="hero-sub">1,079 closed sales @ <span id="subOrderVal">$100</span> assumed order value</div>
      </div>

      <div class="card-foot-split">
        <div>
          <div class="foot-stat-num">$58,705</div>
          <div class="foot-stat-lbl">Total Spend (1,143 ads)</div>
        </div>
        <div>
          <div class="foot-stat-num" id="kpiNetProfit">$49,195</div>
          <div class="foot-stat-lbl">Baseline Profit</div>
        </div>
      </div>
    </div>

    <!-- Hero Card 2: Standout Coral Card (Profit Lift) -->
    <div class="bento-card bento-card-coral">
      <div>
        <div class="card-head">
          <span class="card-label">Recommended Reallocation</span>
          <span style="font-size: 18px;">⚡</span>
        </div>
        <div class="hero-num-huge" id="kpiProfitLift">+$6,184</div>
        <div class="hero-sub" id="kpiProfitLiftSub">+12.6% net profit increase</div>
      </div>
      <div>
        <div class="coral-save-tag">
          <span>Saves $3,769 in ad budget</span>
        </div>
      </div>
    </div>

    <!-- Hero Card 3: Dark Circular Gauge (Blended ROAS) -->
    <div class="bento-card bento-card-dark">
      <div class="gauge-box">
        <svg class="gauge-svg" viewBox="0 0 100 100">
          <circle class="gauge-bg-ring" cx="50" cy="50" r="45"></circle>
          <circle id="roasGaugeCircle" class="gauge-val-ring" cx="50" cy="50" r="45"></circle>
        </svg>
        <div class="gauge-center-text" id="kpiRoasGaugeVal">1.84x</div>
      </div>
      <div class="gauge-title">Blended Portfolio ROAS</div>
      <div class="gauge-caption" id="kpiBreakevenNotice">Breakeven CPA: $100.00</div>
    </div>

    <!-- Hero Card 4: View-Through Attribution (Strictly Delineated Inquiries vs Purchases) -->
    <div class="bento-card">
      <div>
        <div class="card-head">
          <span class="card-label">View-Through Attribution</span>
          <div class="icon-circle">🎯</div>
        </div>
        <div class="hero-num-huge">76 Purchases</div>
        <div class="hero-sub">
          Across 207 zero-click ads: <strong>212 inquiries (204 ads)</strong> resulted in <strong>76 approved purchases (71 ads)</strong> with $0 spend.
        </div>
      </div>

      <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--bg-muted); display: flex; justify-content: space-between; align-items: center;">
        <div>
          <div style="font-size: 11px; color: var(--text-secondary);">Zero-Click Inquiries</div>
          <div style="font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 700; color: var(--text-primary);">212 Leads</div>
        </div>
        <div class="status-badge badge-cpc">488k Impressions</div>
      </div>
    </div>

  </section>

  <!-- Bento Grid Row 2: Concentric Demographic Card + Tabbed Reallocation Engine -->
  <section class="bento-row bento-middle-row">
    
    <!-- Left Card: Concentric Radial Progress Rings with Distinct Tri-Color Palette & External Text -->
    <div class="bento-card">
      <div>
        <div class="card-head" style="margin-bottom: 10px;">
          <div>
            <h3 style="font-size: 15px;">Demographic Tiering</h3>
            <span style="font-size: 11.5px; color: var(--text-muted);">Revenue concentration by cohort tier</span>
          </div>
          <span class="status-badge" style="background: var(--bg-subtle); color: var(--text-secondary);">3-Tier Rings</span>
        </div>

        <!-- External Stat Block (Cleanly outside the circles) -->
        <div class="radial-top-stat-block">
          <div class="radial-stat-lbl">Portfolio Gross Revenue</div>
          <div class="radial-stat-val" id="concOuterRevenue">$107,900</div>
          <div class="radial-stat-caption">Across 1,079 orders @ $<span class="concOrderValDisplay">100</span> assumed value</div>
        </div>

        <!-- Pure Concentric Rings (Clean inside, completely free of text!) -->
        <div class="radial-rings-container">
          <svg class="radial-svg" viewBox="0 0 160 160">
            <!-- Ring 1 (Outer): Portfolio Total -> Indigo (#4C5FD5, r = 66, C = 414.69) -->
            <circle class="ring-track" cx="80" cy="80" r="66" stroke-width="8.5"></circle>
            <circle id="ringProgressL1" class="ring-progress" cx="80" cy="80" r="66" stroke-width="8.5" stroke="#4C5FD5" stroke-dasharray="414.69" stroke-dashoffset="0"></circle>

            <!-- Ring 2 (Middle): Top 3 Cohorts -> Warm Amber (#F59E0B, r = 48, C = 301.59, 56.2% -> offset 132.10) -->
            <circle class="ring-track" cx="80" cy="80" r="48" stroke-width="8.5"></circle>
            <circle id="ringProgressL2" class="ring-progress" cx="80" cy="80" r="48" stroke-width="8.5" stroke="#F59E0B" stroke-dasharray="301.59" stroke-dashoffset="132.10"></circle>

            <!-- Ring 3 (Inner): Men 30-34 Hero Cohort -> Vibrant Coral (#FF6B4A, r = 30, C = 188.50, 27.7% -> offset 136.29) -->
            <circle class="ring-track" cx="80" cy="80" r="30" stroke-width="8.5"></circle>
            <circle id="ringProgressL3" class="ring-progress" cx="80" cy="80" r="30" stroke-width="8.5" stroke="#FF6B4A" stroke-dasharray="188.50" stroke-dashoffset="136.29"></circle>
          </svg>
        </div>
      </div>

      <div>
        <!-- Legend with 3 Totally Distinct Colors -->
        <div class="concentric-item-list">
          <div class="concentric-row">
            <div class="concentric-row-left">
              <span class="dot-marker" style="background: #4C5FD5;"></span>
              <span style="font-weight: 500;">Total Portfolio Gross</span>
            </div>
            <div>
              <strong id="concLegL1" style="color: #4C5FD5;">$107,900</strong>
              <span style="color: var(--text-muted); font-size: 11px; margin-left: 4px;">(100%)</span>
            </div>
          </div>

          <div class="concentric-row">
            <div class="concentric-row-left">
              <span class="dot-marker" style="background: #F59E0B;"></span>
              <span style="font-weight: 500;">Top 3 Cohorts (30–39)</span>
            </div>
            <div>
              <strong id="concLegL2" style="color: #D97706;">$60,600</strong>
              <span style="color: var(--text-muted); font-size: 11px; margin-left: 4px;">(56%)</span>
            </div>
          </div>

          <div class="concentric-row">
            <div class="concentric-row-left">
              <span class="dot-marker" style="background: #FF6B4A;"></span>
              <span style="font-weight: 500;">Men 30–34 (Hero Cohort)</span>
            </div>
            <div>
              <strong id="concLegL3" style="color: #FF6B4A;">$29,900</strong>
              <span style="color: var(--accent-coral); font-weight: 700; font-size: 11px; margin-left: 4px;">(28%)</span>
            </div>
          </div>
        </div>

        <!-- Separate Unit-Cost Metric Callout (CPA distinct from Revenue rings) -->
        <div class="hero-cpa-callout">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
              <span style="font-size: 10.5px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Top Cohort Unit Cost</span>
              <div style="font-family: 'Sora', sans-serif; font-size: 16px; font-weight: 700; color: var(--accent-coral);">Men 30-34 CPA: $25.55</div>
            </div>
            <span class="status-badge" style="background: var(--color-emerald-tint); color: var(--color-emerald); font-weight: 700;">-53% vs Avg CPA</span>
          </div>
          <div style="font-size: 11px; color: var(--text-secondary); margin-top: 3px;">
            Generates 6.82% conversion rate at lowest CPA in the portfolio ($25.55 vs $54.41 portfolio average).
          </div>
        </div>
      </div>
    </div>

    <!-- Right Card: Tabbed Reallocation Engine -->
    <div class="tabbed-engine-card">
      <div class="engine-head-bar">
        <div class="nav-pills">
          <button class="nav-pill-btn active" onclick="switchLensTab('age_gender')">Lens A: Age × Gender</button>
          <button class="nav-pill-btn" onclick="switchLensTab('interest')">Lens B: Interest Segments</button>
        </div>
        <span class="lens-info-pill">Independent lenses on same $58.7k budget (not additive)</span>
      </div>

      <div class="lens-inner-grid">
        <!-- Chart -->
        <div>
          <div style="font-size: 12px; font-weight: 600; color: var(--text-secondary); margin-bottom: 6px;">
            Segment ROAS vs Portfolio Benchmark (<span id="chartBenchmarkVal">1.84x</span>)
          </div>
          <div class="bar-chart-container">
            <canvas id="lensChart"></canvas>
          </div>
        </div>

        <!-- Cards List -->
        <div>
          <div style="font-size: 12px; font-weight: 600; color: var(--text-secondary); margin-bottom: 6px;">
            Recommended Reallocation Directives (Capped within ±30%)
          </div>
          <div class="cards-table-scroll" id="tableCardsContainer">
            <!-- Dynamically populated -->
          </div>
        </div>
      </div>
    </div>

  </section>

  <!-- Bento Grid Row 3: Diminishing Returns & Marginal Economics (2-col Bento) -->
  <section class="bento-row bento-bottom-row">
    
    <!-- Scatter Plot Card -->
    <div class="bento-card">
      <div class="card-head" style="margin-bottom: 4px;">
        <div>
          <h3 style="font-size: 15px;">Campaign 1178 Ad-Level Response Curve</h3>
          <span style="font-size: 11.5px; color: var(--text-muted);">Spend vs. Approved Conversions across 625 ads with OLS Regression</span>
        </div>
        <span class="status-badge" style="background: var(--bg-subtle); color: var(--text-secondary);">R² = 0.315 • p = 3.25e-53</span>
      </div>

      <div class="scatter-chart-wrap">
        <canvas id="scatterChart"></canvas>
      </div>
    </div>

    <!-- Side Analysis Stack (Two balanced cards) -->
    <div class="diminishing-stack">
      
      <!-- Card A: Marginal Economics -->
      <div class="side-stat-box">
        <div>
          <div class="card-head" style="margin-bottom: 6px;">
            <span style="font-size: 12.5px; font-weight: 600;">Marginal Acquisition Cost</span>
            <span class="status-badge" style="background: var(--accent-coral-tint); color: var(--accent-coral);">1.30x of Avg CPA</span>
          </div>
          <div class="box-stat-coral">$82.89</div>
          <p style="font-size: 12px; color: var(--text-secondary); line-height: 1.4;">
            Slope &beta;₁ = +0.01206. Incremental orders cost <strong>$82.89</strong> each vs. Campaign 1178's average CPA of <strong>$63.83</strong>.
          </p>
        </div>

        <div class="guidance-banner">
          <strong id="marginalRoasTitle">1.21x Marginal ROAS</strong>
          <p>
            Because marginal CPA ($82.89) is below assumed order value ($<span class="inlineOrderVal">100</span>), returns are <strong>diminishing but still profitable</strong>. Strategic rule: <em>Moderate growth, do not cut.</em>
          </p>
        </div>
      </div>

      <!-- Card B: Testing Sandboxes -->
      <div class="side-stat-box">
        <div class="card-head" style="margin-bottom: 6px;">
          <span style="font-size: 12.5px; font-weight: 600;">Pilot Campaigns 916 &amp; 936 Note</span>
          <span class="status-badge" style="background: var(--bg-subtle); color: var(--text-secondary);">Flat Slopes</span>
        </div>
        <p style="font-size: 12px; color: var(--text-secondary); line-height: 1.45;">
          Campaign 916 ($150 spend, p = 0.548) and Campaign 936 ($2.89k spend, p = 0.714) have statistically insignificant regression slopes. Ad spend was too low ($0-$20/ad) to support spend-scaling curves. Maintain as discovery sandboxes.
        </p>
      </div>

    </div>

  </section>

  <!-- Footer -->
  <footer>
    <div>Marketing Campaign ROI Dashboard • Light Bento Grid Theme (QClay Reference)</div>
    <div>Strictly Non-Synthetic Ad Tracking Dataset • Kaggle loveall/clicks-conversion-tracking</div>
  </footer>

  <!-- Script Logic -->
  <script>
    const DATA = {json.dumps(data)};
    const SCATTER_POINTS = {json.dumps(points_1178)};

    let currentOrderValue = 100.0;
    let activeLens = 'age_gender';
    let lensChartInstance = null;
    let scatterChartInstance = null;

    // Elements
    const orderSlider = document.getElementById('orderValueSlider');
    const orderDisplay = document.getElementById('orderValueDisplay');
    const kpiGrossRevenue = document.getElementById('kpiGrossRevenue');
    const kpiNetProfit = document.getElementById('kpiNetProfit');
    const subOrderVal = document.getElementById('subOrderVal');
    const kpiProfitLift = document.getElementById('kpiProfitLift');
    const kpiProfitLiftSub = document.getElementById('kpiProfitLiftSub');
    const kpiRoasGaugeVal = document.getElementById('kpiRoasGaugeVal');
    const roasGaugeCircle = document.getElementById('roasGaugeCircle');
    const kpiBreakevenNotice = document.getElementById('kpiBreakevenNotice');
    const chartBenchmarkVal = document.getElementById('chartBenchmarkVal');
    const marginalRoasTitle = document.getElementById('marginalRoasTitle');
    const inlineOrderVals = document.querySelectorAll('.inlineOrderVal');

    // Concentric elements
    const concOuterRevenue = document.getElementById('concOuterRevenue');
    const concOrderValDisplays = document.querySelectorAll('.concOrderValDisplay');
    const concLegL1 = document.getElementById('concLegL1');
    const concLegL2 = document.getElementById('concLegL2');
    const concLegL3 = document.getElementById('concLegL3');
    const ringProgressL2 = document.getElementById('ringProgressL2');
    const ringProgressL3 = document.getElementById('ringProgressL3');

    // Tab Switcher
    function switchLensTab(lens) {{
      activeLens = lens;
      const btns = document.querySelectorAll('.nav-pill-btn');
      if (lens === 'age_gender') {{
        btns[0].classList.add('active');
        btns[1].classList.remove('active');
      }} else {{
        btns[0].classList.remove('active');
        btns[1].classList.add('active');
      }}
      renderLensContent();
    }}

    // Recalculate Dashboard on Slider Move
    function updateDashboard() {{
      const V = currentOrderValue;
      const portfolioCpa = DATA.portfolio.portfolio_cpa; // 54.41
      const portfolioRoas = V / portfolioCpa;
      const totalRev = DATA.portfolio.total_approved * V; // 1079 * V
      const baselineProfit = totalRev - DATA.portfolio.total_spend;

      // Net impact
      const deltaApproved = DATA.portfolio.delta_approved; // 24.14
      const spendSavings = Math.abs(DATA.portfolio.net_spend_change); // 3769.29
      const profitLift = (deltaApproved * V) + spendSavings;
      const profitLiftPct = (profitLift / baselineProfit * 100);

      // Marginal ROAS
      const marginalCpa = DATA.regression_1178.marginal_cpa; // 82.89
      const marginalRoas = V / marginalCpa;

      // Update Texts
      orderDisplay.textContent = `$${{V}}`;
      subOrderVal.textContent = `$${{V}}`;
      inlineOrderVals.forEach(el => el.textContent = V);
      concOrderValDisplays.forEach(el => el.textContent = V);

      kpiGrossRevenue.textContent = `$${{Math.round(totalRev).toLocaleString()}}`;
      kpiNetProfit.textContent = `$${{Math.round(baselineProfit).toLocaleString()}}`;
      kpiProfitLift.textContent = `+$${{Math.round(profitLift).toLocaleString()}}`;
      kpiProfitLiftSub.textContent = `+${{profitLiftPct.toFixed(1)}}% net profit increase`;

      kpiRoasGaugeVal.textContent = `${{portfolioRoas.toFixed(2)}}x`;
      chartBenchmarkVal.textContent = `${{portfolioRoas.toFixed(2)}}x`;
      kpiBreakevenNotice.textContent = `Breakeven CPA: $${{V.toFixed(2)}}`;
      marginalRoasTitle.textContent = `${{marginalRoas.toFixed(2)}}x Marginal ROAS`;

      // Update Circular Progress Ring (Circumference = 2 * PI * 45 = 282.74)
      const circumference = 282.74;
      const fillPct = Math.min(Math.max(portfolioRoas / 3.0, 0.05), 1.0);
      const dashOffset = circumference * (1 - fillPct);
      roasGaugeCircle.style.strokeDashoffset = dashOffset;

      // Update Concentric External Readout & Legend
      concOuterRevenue.textContent = `$${{Math.round(totalRev).toLocaleString()}}`;
      concLegL1.textContent = `$${{Math.round(totalRev).toLocaleString()}}`;
      concLegL2.textContent = `$${{Math.round(totalRev * 0.562).toLocaleString()}}`;
      concLegL3.textContent = `$${{Math.round(299 * V).toLocaleString()}}`;

      // Render Active Tab Content
      renderLensContent();
    }}

    // Render Tab Content (Chart + Cards)
    function renderLensContent() {{
      const V = currentOrderValue;
      const portfolioRoas = V / DATA.portfolio.portfolio_cpa;
      const isAgeGender = activeLens === 'age_gender';
      const items = isAgeGender ? DATA.age_gender : DATA.interest;

      // 1. Update Chart
      const labels = items.map(d => isAgeGender ? d.segment : 'ID ' + d.interest_grouped);
      const roasValues = items.map(d => V / d.cpa);
      const bgColors = roasValues.map(r => r >= portfolioRoas ? '#FF6B4A' : '#D1CBC2');

      if (!lensChartInstance) {{
        const ctx = document.getElementById('lensChart').getContext('2d');
        lensChartInstance = new Chart(ctx, {{
          type: 'bar',
          data: {{
            labels: labels,
            datasets: [{{
              data: roasValues,
              backgroundColor: bgColors,
              borderRadius: 6,
              barThickness: 14
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
                  label: ctx => `ROAS: ${{ctx.raw.toFixed(2)}}x (CPA: $${{items[ctx.dataIndex].cpa.toFixed(2)}})`
                }}
              }}
            }},
            scales: {{
              x: {{
                grid: {{ color: '#EFECE6' }},
                ticks: {{ color: '#8E95A5', callback: v => v + 'x' }}
              }},
              y: {{
                grid: {{ display: false }},
                ticks: {{ color: '#181A1F', font: {{ weight: 600, size: 10.5 }} }}
              }}
            }}
          }}
        }});
      }} else {{
        lensChartInstance.data.labels = labels;
        lensChartInstance.data.datasets[0].data = roasValues;
        lensChartInstance.data.datasets[0].backgroundColor = bgColors;
        lensChartInstance.update();
      }}

      // 2. Render Card-Based Rows
      const container = document.getElementById('tableCardsContainer');
      let html = '';

      items.forEach(d => {{
        const roas = V / d.cpa;
        const newSpend = d.spend * (1 + d.shift_pct / 100);
        const shiftClass = d.shift_pct > 0 ? 'shift-pos' : (d.shift_pct < 0 ? 'shift-neg' : 'shift-zero');
        const shiftLabel = d.shift_pct > 0 ? `+${{d.shift_pct}}%` : (d.shift_pct < 0 ? `${{d.shift_pct}}%` : '0%');
        const title = isAgeGender ? d.segment : `Interest ${{d.interest_grouped}}`;

        html += `
          <div class="cohort-card-row">
            <div class="col-cohort">
              <strong>${{title}}</strong>
              <span>$${{Math.round(d.spend).toLocaleString()}}</span>
            </div>
            
            <div class="col-metrics">
              <div>CPA: <strong>$${{d.cpa.toFixed(2)}}</strong></div>
              <div style="font-size: 10.5px; color: var(--text-muted);">${{d.rationale}}</div>
            </div>

            <div class="col-roas">
              ${{roas.toFixed(2)}}x
              <small>${{roas >= 1.0 ? 'Profitable' : 'Loss'}}</small>
            </div>

            <div style="text-align: center;">
              <span class="shift-tag ${{shiftClass}}">${{shiftLabel}}</span>
            </div>

            <div class="col-new-spend">
              $${{Math.round(newSpend).toLocaleString()}}
            </div>
          </div>
        `;
      }});

      container.innerHTML = html;
    }}

    // Scatter Plot Init
    function initScatterPlot() {{
      const ctx = document.getElementById('scatterChart').getContext('2d');
      const maxSpend = Math.max(...SCATTER_POINTS.map(p => p.x));
      const b0 = DATA.regression_1178.intercept;
      const b1 = DATA.regression_1178.slope;
      
      const regressionLine = [
        {{ x: 0, y: b0 }},
        {{ x: maxSpend, y: b0 + b1 * maxSpend }}
      ];

      scatterChartInstance = new Chart(ctx, {{
        type: 'scatter',
        data: {{
          datasets: [
            {{
              label: 'Ads (n = 625)',
              data: SCATTER_POINTS,
              backgroundColor: 'rgba(21, 24, 30, 0.25)',
              borderColor: 'transparent',
              pointRadius: 3.5,
              pointHoverRadius: 6
            }},
            {{
              label: 'OLS Regression Line',
              data: regressionLine,
              type: 'line',
              borderColor: '#FF6B4A',
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
              position: 'top',
              labels: {{ color: '#5F6675', font: {{ size: 11.5 }} }}
            }},
            tooltip: {{
              callbacks: {{
                label: ctx => `Spend: $${{ctx.parsed.x.toFixed(2)}} | Approved: ${{ctx.parsed.y}} orders`
              }}
            }}
          }},
          scales: {{
            x: {{
              title: {{ display: true, text: 'Ad Spend ($USD)', color: '#8D94A3', font: {{ size: 11 }} }},
              grid: {{ color: '#EDE9E3' }},
              ticks: {{ color: '#8D94A3' }}
            }},
            y: {{
              title: {{ display: true, text: 'Approved Conversions (Orders)', color: '#8D94A3', font: {{ size: 11 }} }},
              grid: {{ color: '#EDE9E3' }},
              ticks: {{ color: '#8D94A3' }}
            }}
          }}
        }}
      }});
    }}

    // Listener
    orderSlider.addEventListener('input', e => {{
      currentOrderValue = parseFloat(e.target.value);
      updateDashboard();
    }});

    // Boot
    window.addEventListener('DOMContentLoaded', () => {{
      updateDashboard();
      initScatterPlot();
    }});
  </script>
</body>
</html>
'''

with open('index.html', 'w') as f:
    f.write(html_content)

print("Updated index.html: text moved outside circles, and distinct tri-color palette applied.")
