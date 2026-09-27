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
  <title>Marketing Performance & Capital Allocation Dashboard</title>

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
      --bg-muted: #EFECE6;
      
      --text-primary: #191B1F;
      --text-secondary: #636A79;
      --text-muted: #8E95A5;
      --text-light: #A5ABB8;

      --accent-coral: #FF6B4A;
      --accent-coral-hover: #FA5834;
      --accent-coral-tint: rgba(255, 107, 74, 0.08);
      --accent-coral-tint-deep: rgba(255, 107, 74, 0.16);
      
      --color-dark: #16181E;
      --color-dark-surface: #20232B;
      
      --color-emerald: #1F9D77;
      --color-emerald-tint: rgba(31, 157, 119, 0.10);

      --radius-xl: 26px;
      --radius-lg: 20px;
      --radius-md: 14px;
      --radius-pill: 9999px;

      --shadow-card: 0 10px 30px rgba(25, 27, 31, 0.035), 0 2px 8px rgba(25, 27, 31, 0.02);
      --shadow-hover: 0 18px 40px rgba(25, 27, 31, 0.06), 0 4px 12px rgba(25, 27, 31, 0.03);
      --shadow-coral: 0 12px 28px rgba(255, 107, 74, 0.28);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background-color: var(--bg-page);
      color: var(--text-primary);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      font-variant-numeric: tabular-nums;
      line-height: 1.45;
      padding: 36px 48px 80px;
      max-width: 1560px;
      margin: 0 auto;
      -webkit-font-smoothing: antialiased;
    }}

    /* Headings */
    h1, h2, h3, h4, .brand-title {{
      font-family: 'Sora', sans-serif;
      font-weight: 700;
      letter-spacing: -0.025em;
      color: var(--text-primary);
    }}

    /* Top Navigation Header */
    .top-nav {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 32px;
      flex-wrap: wrap;
      gap: 20px;
    }}

    .nav-left {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .brand-mark {{
      width: 44px;
      height: 44px;
      background: var(--color-dark);
      color: #FFFFFF;
      border-radius: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Sora', sans-serif;
      font-weight: 800;
      font-size: 18px;
      box-shadow: 0 4px 12px rgba(22, 24, 30, 0.15);
    }}

    .brand-meta h1 {{
      font-size: 20px;
      line-height: 1.2;
    }}

    .brand-meta p {{
      font-size: 13px;
      color: var(--text-secondary);
      font-weight: 400;
    }}

    /* Order Value Controller Pill in Header */
    .controller-pill {{
      background: var(--bg-card);
      padding: 8px 12px 8px 20px;
      border-radius: var(--radius-pill);
      box-shadow: var(--shadow-card);
      display: flex;
      align-items: center;
      gap: 20px;
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

    .assumed-badge {{
      background: #FFF1EE;
      color: var(--accent-coral);
      font-size: 10px;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: var(--radius-pill);
    }}

    .controller-sub {{
      font-size: 11px;
      color: var(--text-muted);
    }}

    .slider-track-wrap {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .slider-track-wrap span {{
      font-size: 12px;
      font-weight: 500;
      color: var(--text-secondary);
    }}

    .order-slider {{
      width: 160px;
      height: 6px;
      border-radius: var(--radius-pill);
      background: var(--bg-muted);
      outline: none;
      -webkit-appearance: none;
      cursor: pointer;
    }}

    .order-slider::-webkit-slider-thumb {{
      -webkit-appearance: none;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: var(--accent-coral);
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(255, 107, 74, 0.4);
      transition: transform 0.15s ease;
    }}

    .order-slider::-webkit-slider-thumb:hover {{
      transform: scale(1.18);
    }}

    .slider-val-badge {{
      background: var(--color-dark);
      color: #FFFFFF;
      font-family: 'Sora', sans-serif;
      font-weight: 700;
      font-size: 14px;
      padding: 7px 16px;
      border-radius: var(--radius-pill);
      min-width: 68px;
      text-align: center;
    }}

    /* Bento Grid System */
    .bento-grid-hero {{
      display: grid;
      grid-template-columns: 1.4fr 1.15fr 0.9fr 1.05fr;
      gap: 24px;
      margin-bottom: 28px;
    }}

    @media (max-width: 1280px) {{
      .bento-grid-hero {{
        grid-template-columns: 1fr 1fr;
      }}
    }}

    @media (max-width: 768px) {{
      .bento-grid-hero {{
        grid-template-columns: 1fr;
      }}
    }}

    /* Card Base */
    .card {{
      background: var(--bg-card);
      border-radius: var(--radius-xl);
      padding: 28px;
      box-shadow: var(--shadow-card);
      position: relative;
      transition: transform 0.25s ease, box-shadow 0.25s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .card:hover {{
      transform: translateY(-2px);
      box-shadow: var(--shadow-hover);
    }}

    .card-top {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 20px;
    }}

    .icon-badge {{
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: var(--accent-coral-tint);
      color: var(--accent-coral);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
    }}

    .card-label {{
      font-size: 13px;
      font-weight: 500;
      color: var(--text-secondary);
      margin-bottom: 4px;
    }}

    .hero-stat-large {{
      font-family: 'Sora', sans-serif;
      font-size: 34px;
      font-weight: 700;
      color: var(--text-primary);
      letter-spacing: -0.03em;
      line-height: 1.1;
    }}

    .hero-stat-desc {{
      font-size: 12.5px;
      color: var(--text-muted);
      margin-top: 6px;
    }}

    /* Hero Card 1: Revenue & Spend Split */
    .spend-revenue-split {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      padding-top: 18px;
      border-top: 1px solid var(--bg-muted);
      margin-top: 16px;
    }}

    .sub-stat-num {{
      font-family: 'Sora', sans-serif;
      font-size: 18px;
      font-weight: 700;
      color: var(--text-primary);
    }}

    .sub-stat-label {{
      font-size: 11.5px;
      color: var(--text-secondary);
    }}

    /* Hero Card 2: Standout Coral Card (Profit Lift) */
    .card-coral-hero {{
      background: linear-gradient(135deg, #FF6B4A 0%, #FA5530 100%);
      color: #FFFFFF;
      box-shadow: var(--shadow-coral);
    }}

    .card-coral-hero .card-label {{
      color: rgba(255, 255, 255, 0.85);
    }}

    .card-coral-hero .hero-stat-large {{
      color: #FFFFFF;
      font-size: 38px;
    }}

    .card-coral-hero .hero-stat-desc {{
      color: rgba(255, 255, 255, 0.9);
      font-size: 13px;
    }}

    .coral-pill-tag {{
      display: inline-flex;
      align-items: center;
      background: rgba(255, 255, 255, 0.22);
      backdrop-filter: blur(8px);
      padding: 6px 14px;
      border-radius: var(--radius-pill);
      font-size: 12px;
      font-weight: 600;
      color: #FFFFFF;
      margin-top: 12px;
      width: fit-content;
    }}

    /* Hero Card 3: Dark Circular Gauge Card */
    .card-dark-gauge {{
      background: var(--color-dark);
      color: #FFFFFF;
      align-items: center;
      text-align: center;
      justify-content: center;
      padding: 24px;
    }}

    .gauge-wrapper {{
      position: relative;
      width: 124px;
      height: 124px;
      margin-bottom: 12px;
    }}

    .gauge-svg {{
      width: 100%;
      height: 100%;
      transform: rotate(-90deg);
    }}

    .gauge-bg {{
      fill: none;
      stroke: var(--color-dark-surface);
      stroke-width: 9;
    }}

    .gauge-progress {{
      fill: none;
      stroke: var(--accent-coral);
      stroke-width: 9;
      stroke-linecap: round;
      stroke-dasharray: 339.29;
      stroke-dashoffset: 80;
      transition: stroke-dashoffset 0.5s ease;
    }}

    .gauge-inner-text {{
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-family: 'Sora', sans-serif;
      font-weight: 700;
      font-size: 22px;
      color: #FFFFFF;
    }}

    .gauge-label {{
      font-size: 13px;
      font-weight: 600;
      color: #FFFFFF;
    }}

    .gauge-sub {{
      font-size: 11.5px;
      color: #8E95A5;
      margin-top: 2px;
    }}

    /* Hero Card 4: View-Through Attribution */
    .pill-indicator {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11.5px;
      font-weight: 600;
      background: var(--accent-coral-tint);
      color: var(--accent-coral);
      padding: 4px 10px;
      border-radius: var(--radius-pill);
    }}

    /* Bento Row 2: Concentric Layer + Reallocation Lens */
    .bento-grid-reallocation {{
      display: grid;
      grid-template-columns: 420px 1fr;
      gap: 24px;
      margin-bottom: 28px;
    }}

    @media (max-width: 1200px) {{
      .bento-grid-reallocation {{
        grid-template-columns: 1fr;
      }}
    }}

    /* Concentric Rings Card */
    .concentric-card {{
      background: var(--bg-card);
      border-radius: var(--radius-xl);
      padding: 28px;
      box-shadow: var(--shadow-card);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .concentric-art-wrap {{
      position: relative;
      width: 100%;
      height: 290px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 16px 0;
    }}

    .concentric-legend {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      border-top: 1px solid var(--bg-muted);
      padding-top: 16px;
    }}

    .legend-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12.5px;
    }}

    .legend-dot {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
      display: inline-block;
      margin-right: 8px;
    }}

    /* Reallocation Lens Tabs & Cards */
    .lens-card {{
      background: var(--bg-card);
      border-radius: var(--radius-xl);
      padding: 28px;
      box-shadow: var(--shadow-card);
    }}

    .lens-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      flex-wrap: wrap;
      gap: 14px;
    }}

    .pill-tabs {{
      display: flex;
      background: var(--bg-subtle);
      padding: 4px;
      border-radius: var(--radius-pill);
      gap: 4px;
    }}

    .pill-tab-btn {{
      border: none;
      background: transparent;
      padding: 8px 18px;
      border-radius: var(--radius-pill);
      font-family: 'Inter', sans-serif;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .pill-tab-btn.active {{
      background: var(--color-dark);
      color: #FFFFFF;
      box-shadow: 0 4px 12px rgba(22, 24, 30, 0.15);
    }}

    .lens-notice {{
      font-size: 12px;
      color: var(--text-muted);
      background: var(--bg-subtle);
      padding: 6px 14px;
      border-radius: var(--radius-pill);
    }}

    .lens-layout-grid {{
      display: grid;
      grid-template-columns: 360px 1fr;
      gap: 24px;
    }}

    @media (max-width: 1080px) {{
      .lens-layout-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .chart-box {{
      height: 380px;
      position: relative;
    }}

    /* Card-Based Table List */
    .table-cards-list {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      max-height: 480px;
      overflow-y: auto;
      padding-right: 6px;
    }}

    .table-cards-list::-webkit-scrollbar {{
      width: 5px;
    }}
    .table-cards-list::-webkit-scrollbar-thumb {{
      background: var(--bg-muted);
      border-radius: 4px;
    }}

    .segment-row-card {{
      background: var(--bg-subtle);
      border-radius: var(--radius-md);
      padding: 14px 18px;
      display: grid;
      grid-template-columns: 140px 1fr 100px 90px 80px;
      align-items: center;
      gap: 14px;
      transition: background 0.15s ease, transform 0.15s ease;
    }}

    .segment-row-card:hover {{
      background: #F1EFEA;
      transform: translateX(2px);
    }}

    .segment-name-col strong {{
      font-size: 13.5px;
      color: var(--text-primary);
      display: block;
    }}

    .segment-name-col span {{
      font-size: 11.5px;
      color: var(--text-muted);
    }}

    .segment-metrics-col {{
      font-size: 12px;
      color: var(--text-secondary);
      line-height: 1.35;
    }}

    .roas-col {{
      font-family: 'Sora', sans-serif;
      font-weight: 700;
      font-size: 16px;
      color: var(--text-primary);
      text-align: right;
    }}

    .roas-col small {{
      display: block;
      font-size: 10.5px;
      font-weight: 500;
      color: var(--text-muted);
    }}

    .shift-pill {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 5px 12px;
      border-radius: var(--radius-pill);
      font-weight: 700;
      font-size: 12px;
      white-space: nowrap;
    }}

    .shift-up {{
      background: var(--color-emerald-tint);
      color: var(--color-emerald);
    }}

    .shift-down {{
      background: rgba(255, 107, 74, 0.12);
      color: var(--accent-coral);
    }}

    .shift-neutral {{
      background: var(--bg-muted);
      color: var(--text-secondary);
    }}

    .new-spend-col {{
      text-align: right;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-primary);
    }}

    /* Bento Row 3: Diminishing Returns & Marginal Economics */
    .bento-grid-diminishing {{
      display: grid;
      grid-template-columns: 1fr 380px;
      gap: 24px;
    }}

    @media (max-width: 1080px) {{
      .bento-grid-diminishing {{
        grid-template-columns: 1fr;
      }}
    }}

    .scatter-card {{
      background: var(--bg-card);
      border-radius: var(--radius-xl);
      padding: 28px;
      box-shadow: var(--shadow-card);
    }}

    .scatter-chart-box {{
      height: 380px;
      position: relative;
      margin-top: 14px;
    }}

    .diminishing-side-col {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    .stat-box-card {{
      background: var(--bg-card);
      border-radius: var(--radius-lg);
      padding: 20px 24px;
      box-shadow: var(--shadow-card);
    }}

    .stat-box-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }}

    .tag-badge {{
      font-size: 11px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: var(--radius-pill);
      background: var(--bg-subtle);
      color: var(--text-secondary);
    }}

    .stat-val-coral {{
      font-family: 'Sora', sans-serif;
      font-size: 26px;
      font-weight: 700;
      color: var(--accent-coral);
      margin-bottom: 4px;
    }}

    .stat-desc-text {{
      font-size: 12.5px;
      color: var(--text-secondary);
      line-height: 1.45;
    }}

    .guidance-box {{
      background: var(--bg-subtle);
      border-left: 4px solid var(--accent-coral);
      padding: 16px;
      border-radius: 0 var(--radius-md) var(--radius-md) 0;
      margin-top: 8px;
    }}

    .guidance-box strong {{
      color: var(--text-primary);
      font-size: 13px;
      display: block;
      margin-bottom: 4px;
    }}

    .guidance-box p {{
      font-size: 12px;
      color: var(--text-secondary);
      line-height: 1.4;
    }}

    /* Footer */
    footer {{
      margin-top: 48px;
      padding-top: 24px;
      border-top: 1px solid var(--bg-muted);
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      color: var(--text-muted);
      flex-wrap: wrap;
      gap: 12px;
    }}
  </style>
</head>
<body>

  <!-- Top Navigation Header -->
  <header class="top-nav">
    <div class="nav-left">
      <div class="brand-mark">M</div>
      <div class="brand-meta">
        <h1>Marketing Campaign ROI Dashboard</h1>
        <p>Capital Allocation & Diminishing Returns Engine • Authentic Facebook Ads Dataset</p>
      </div>
    </div>

    <!-- Order Value Controller -->
    <div class="controller-pill">
      <div class="controller-labels">
        <div class="controller-title">
          <span>Assumed Order Value</span>
          <span class="assumed-badge">Assumed Parameter</span>
        </div>
        <span class="controller-sub">Not in raw source data • Live recalibration</span>
      </div>

      <div class="slider-track-wrap">
        <span>$30</span>
        <input type="range" id="orderValueSlider" class="order-slider" min="30" max="200" step="5" value="100">
        <span>$200</span>
      </div>

      <div class="slider-val-badge" id="orderValueDisplay">$100</div>
    </div>
  </header>

  <!-- Bento Grid Hero: 4 Varied Cards -->
  <section class="bento-grid-hero">
    
    <!-- Hero Card 1: Gross Revenue & Spend Split -->
    <div class="card">
      <div>
        <div class="card-top">
          <span class="card-label">Portfolio Revenue</span>
          <div class="icon-badge">📈</div>
        </div>
        <div class="hero-stat-large" id="kpiGrossRevenue">$107,900</div>
        <div class="hero-stat-desc">1,079 closed sales @ <span id="subOrderVal">$100</span> assumed value</div>
      </div>

      <div class="spend-revenue-split">
        <div>
          <div class="sub-stat-num">$58,705</div>
          <div class="sub-stat-label">Total Spend (1,143 ads)</div>
        </div>
        <div>
          <div class="sub-stat-num" id="kpiNetProfit">$49,195</div>
          <div class="sub-stat-label">Baseline Profit</div>
        </div>
      </div>
    </div>

    <!-- Hero Card 2: Standout Coral Card (Profit Lift) -->
    <div class="card card-coral-hero">
      <div>
        <div class="card-top">
          <span class="card-label">Recommended Reallocation</span>
          <span style="font-size: 20px;">⚡</span>
        </div>
        <div class="hero-stat-large" id="kpiProfitLift">+$6,184</div>
        <div class="hero-stat-desc" id="kpiProfitLiftSub">+12.6% net profit increase</div>
      </div>
      <div>
        <div class="coral-pill-tag">
          <span>Saves $3,769 in ad budget</span>
        </div>
      </div>
    </div>

    <!-- Hero Card 3: Dark Circular Gauge (Blended ROAS) -->
    <div class="card card-dark-gauge">
      <div class="gauge-wrapper">
        <svg class="gauge-svg" viewBox="0 0 120 120">
          <circle class="gauge-bg" cx="60" cy="60" r="54"></circle>
          <circle id="roasGaugeCircle" class="gauge-progress" cx="60" cy="60" r="54"></circle>
        </svg>
        <div class="gauge-inner-text" id="kpiRoasGaugeVal">1.84x</div>
      </div>
      <div class="gauge-label">Blended Portfolio ROAS</div>
      <div class="gauge-sub" id="kpiBreakevenNotice">Breakeven CPA: $100.00</div>
    </div>

    <!-- Hero Card 4: View-Through & CPA -->
    <div class="card">
      <div>
        <div class="card-top">
          <span class="card-label">View-Through Attribution</span>
          <div class="icon-badge">🎯</div>
        </div>
        <div class="hero-stat-large">204 Orders</div>
        <div class="hero-stat-desc">
          18.1% of ads converted with <strong>$0 spend & zero clicks</strong> across 488k impressions.
        </div>
      </div>

      <div style="margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--bg-muted); display: flex; justify-content: space-between; align-items: center;">
        <div>
          <div style="font-size: 11.5px; color: var(--text-secondary);">Portfolio CPA</div>
          <div style="font-family: 'Sora', sans-serif; font-size: 17px; font-weight: 700;">$54.41</div>
        </div>
        <div class="pill-indicator">CPC Billed</div>
      </div>
    </div>

  </section>

  <!-- Bento Grid Row 2: Concentric Visual + Tabbed Reallocation -->
  <section class="bento-grid-reallocation">
    
    <!-- Left Card: Nested Concentric Donut / Arch Breakdown -->
    <div class="concentric-card">
      <div>
        <div class="card-top">
          <div>
            <h3 style="font-size: 16px;">Demographic Tiering</h3>
            <span style="font-size: 12px; color: var(--text-muted);">Nested revenue concentration</span>
          </div>
          <span class="tag-badge">QClay Bento Style</span>
        </div>

        <!-- Concentric SVG Visual (Teardrop / Arch Layers) -->
        <div class="concentric-art-wrap">
          <svg viewBox="0 0 320 280" width="100%" height="100%" style="overflow: visible;">
            <defs>
              <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="0" dy="6" stdDeviation="8" flood-opacity="0.04" />
              </filter>
            </defs>

            <!-- Layer 1: Portfolio Outer Arch (Lightest Peach) -->
            <ellipse cx="160" cy="180" rx="145" ry="95" fill="#FDF3EF" filter="url(#softGlow)" />
            <text x="160" y="105" text-anchor="middle" font-family="Sora" font-size="12" font-weight="700" fill="#B48275" id="concTextL1">Portfolio: $107.9K</text>

            <!-- Layer 2: Top 3 Cohorts (Peach) -->
            <ellipse cx="160" cy="192" rx="112" ry="74" fill="#FBDED5" filter="url(#softGlow)" />
            <text x="160" y="136" text-anchor="middle" font-family="Sora" font-size="11.5" font-weight="700" fill="#A86252" id="concTextL2">Top 3 Cohorts: $60.6K</text>

            <!-- Layer 3: Top Demographic Men 30-34 (Warm Coral Tint) -->
            <ellipse cx="160" cy="204" rx="80" ry="54" fill="#F8BCAC" filter="url(#softGlow)" />
            <text x="160" y="166" text-anchor="middle" font-family="Sora" font-size="11" font-weight="700" fill="#8E4334" id="concTextL3">Men 30-34: $29.9K</text>

            <!-- Layer 4: Highest Efficiency Core (Solid Coral) -->
            <ellipse cx="160" cy="216" rx="48" ry="34" fill="#FF6B4A" filter="url(#softGlow)" />
            <text x="160" y="221" text-anchor="middle" font-family="Sora" font-size="11" font-weight="800" fill="#FFFFFF" id="concTextL4">CPA: $25.55</text>
          </svg>
        </div>
      </div>

      <div class="concentric-legend">
        <div class="legend-row">
          <span><span class="legend-dot" style="background: #FDF3EF; border: 1px solid #E8CFC7;"></span>Total Portfolio Gross</span>
          <strong id="concLegL1">$107,900</strong>
        </div>
        <div class="legend-row">
          <span><span class="legend-dot" style="background: #FBDED5;"></span>Top 3 Cohorts (30-39)</span>
          <strong id="concLegL2">$60,600</strong>
        </div>
        <div class="legend-row">
          <span><span class="legend-dot" style="background: #FF6B4A;"></span>Men 30-34 (Hero Segment)</span>
          <strong id="concLegL3">$29,900 (ROAS: 3.91x)</strong>
        </div>
      </div>
    </div>

    <!-- Right Card: Tab-Switchable Reallocation Engine -->
    <div class="lens-card">
      <div class="lens-header">
        <div class="pill-tabs">
          <button class="pill-tab-btn active" onclick="switchLensTab('age_gender')">Lens A: Age × Gender</button>
          <button class="pill-tab-btn" onclick="switchLensTab('interest')">Lens B: Interest Segments</button>
        </div>
        <span class="lens-notice">Independent lenses on same $58.7k budget (not additive)</span>
      </div>

      <!-- Tab Content Grid -->
      <div class="lens-layout-grid">
        <!-- Left: ROAS Bar Chart -->
        <div>
          <div style="font-size: 13px; font-weight: 600; color: var(--text-secondary); margin-bottom: 8px;">
            Segment ROAS vs Portfolio Benchmark (<span id="chartBenchmarkVal">1.84x</span>)
          </div>
          <div class="chart-box">
            <canvas id="lensChart"></canvas>
          </div>
        </div>

        <!-- Right: Card-based Table Rows -->
        <div>
          <div style="font-size: 13px; font-weight: 600; color: var(--text-secondary); margin-bottom: 8px;">
            Segment Reallocation Directives (Capped within ±30%)
          </div>
          <div class="table-cards-list" id="tableCardsContainer">
            <!-- Dynamically populated -->
          </div>
        </div>
      </div>
    </div>

  </section>

  <!-- Bento Grid Row 3: Diminishing Returns & Marginal Economics -->
  <section class="bento-grid-diminishing">
    
    <!-- Scatter Plot Card -->
    <div class="scatter-card">
      <div class="card-top" style="margin-bottom: 8px;">
        <div>
          <h3 style="font-size: 16px;">Campaign 1178 Ad-Level Response Curve</h3>
          <span style="font-size: 12px; color: var(--text-muted);">Spend vs. Approved Conversions across 625 ads with OLS Regression</span>
        </div>
        <span class="tag-badge">R² = 0.315 • p = 3.25e-53</span>
      </div>

      <div class="scatter-chart-box">
        <canvas id="scatterChart"></canvas>
      </div>
    </div>

    <!-- Side Analysis Column -->
    <div class="diminishing-side-col">
      
      <!-- Stat Box: Marginal vs Average CPA -->
      <div class="stat-box-card">
        <div class="stat-box-header">
          <span style="font-size: 13px; font-weight: 600;">Marginal Acquisition Cost</span>
          <span class="tag-badge">1.30x of Avg CPA</span>
        </div>
        <div class="stat-val-coral">$82.89</div>
        <p class="stat-desc-text">
          Slope &beta;₁ = +0.01206. Incremental orders cost <strong>$82.89</strong> each vs. Campaign 1178's average CPA of <strong>$63.83</strong>.
        </p>

        <div class="guidance-box">
          <strong id="marginalRoasTitle">1.21x Marginal ROAS</strong>
          <p>
            Because marginal CPA ($82.89) is still below our assumed order value ($<span class="inlineOrderVal">100</span>), returns are <strong>diminishing but still profitable</strong>. Strategic rule: <em>Moderate growth, do not cut.</em>
          </p>
        </div>
      </div>

      <!-- Stat Box: Pilot Campaigns 916 & 936 -->
      <div class="stat-box-card">
        <div class="stat-box-header">
          <span style="font-size: 13px; font-weight: 600;">Campaigns 916 & 936 Note</span>
          <span class="tag-badge">Flat Slopes</span>
        </div>
        <p class="stat-desc-text">
          Campaign 916 ($150 spend, p = 0.548) and Campaign 936 ($2.89k spend, p = 0.714) have statistically insignificant regression slopes. Ad spend was too low ($0-$20/ad) to support scaling curves. Maintain as discovery sandboxes.
        </p>
      </div>

    </div>

  </section>

  <!-- Footer -->
  <footer>
    <div>Marketing Campaign ROI Dashboard • Inspired by Bogdan Falin / QClay Dribbble Aesthetic</div>
    <div>Strictly Non-Synthetic Ad Tracking Dataset • Kaggle loveall/clicks-conversion-tracking</div>
  </footer>

  <!-- Dashboard Logic -->
  <script>
    const DATA = {json.dumps(data)};
    const SCATTER_POINTS = {json.dumps(points_1178)};

    let currentOrderValue = 100.0;
    let activeLens = 'age_gender';
    let lensChartInstance = null;
    let scatterChartInstance = null;

    // DOM Elements
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
    const concTextL1 = document.getElementById('concTextL1');
    const concTextL2 = document.getElementById('concTextL2');
    const concTextL3 = document.getElementById('concTextL3');
    const concLegL1 = document.getElementById('concLegL1');
    const concLegL2 = document.getElementById('concLegL2');
    const concLegL3 = document.getElementById('concLegL3');

    // Tab Switcher
    function switchLensTab(lens) {{
      activeLens = lens;
      const btns = document.querySelectorAll('.pill-tab-btn');
      if (lens === 'age_gender') {{
        btns[0].classList.add('active');
        btns[1].classList.remove('active');
      }} else {{
        btns[0].classList.remove('active');
        btns[1].classList.add('active');
      }}
      renderLensContent();
    }}

    // Recalculation Engine
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

      kpiGrossRevenue.textContent = `$${{Math.round(totalRev).toLocaleString()}}`;
      kpiNetProfit.textContent = `$${{Math.round(baselineProfit).toLocaleString()}}`;
      kpiProfitLift.textContent = `+$${{Math.round(profitLift).toLocaleString()}}`;
      kpiProfitLiftSub.textContent = `+${{profitLiftPct.toFixed(1)}}% net profit lift`;

      kpiRoasGaugeVal.textContent = `${{portfolioRoas.toFixed(2)}}x`;
      chartBenchmarkVal.textContent = `${{portfolioRoas.toFixed(2)}}x`;
      kpiBreakevenNotice.textContent = `Breakeven CPA: $${{V.toFixed(2)}}`;
      marginalRoasTitle.textContent = `${{marginalRoas.toFixed(2)}}x Marginal ROAS`;

      // Update SVG Circular Gauge (Circumference = 2 * PI * 54 = 339.29)
      const circumference = 339.29;
      // Scale 0x to 3x ROAS
      const fillPct = Math.min(Math.max(portfolioRoas / 3.0, 0.05), 1.0);
      const dashOffset = circumference * (1 - fillPct);
      roasGaugeCircle.style.strokeDashoffset = dashOffset;

      // Update Concentric Rings
      const revL1 = totalRev / 1000;
      const revL2 = (totalRev * 0.562) / 1000;
      const revL3 = (299 * V) / 1000;
      concTextL1.textContent = `Portfolio: $${{revL1.toFixed(1)}}K`;
      concTextL2.textContent = `Top 3 Cohorts: $${{revL2.toFixed(1)}}K`;
      concTextL3.textContent = `Men 30-34: $${{revL3.toFixed(1)}}K`;

      concLegL1.textContent = `$${{Math.round(totalRev).toLocaleString()}}`;
      concLegL2.textContent = `$${{Math.round(totalRev * 0.562).toLocaleString()}}`;
      concLegL3.textContent = `$${{Math.round(299 * V).toLocaleString()}} (ROAS: ${{(V / 25.55).toFixed(2)}}x)`;

      // Render Active Tab
      renderLensContent();
    }}

    // Render Tab Content (Chart + Card Rows)
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
              barThickness: 16
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
                ticks: {{ color: '#191B1F', font: {{ weight: 600, size: 11 }} }}
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
        const shiftClass = d.shift_pct > 0 ? 'shift-up' : (d.shift_pct < 0 ? 'shift-down' : 'shift-neutral');
        const shiftLabel = d.shift_pct > 0 ? `+${{d.shift_pct}}%` : (d.shift_pct < 0 ? `${{d.shift_pct}}%` : 'Hold (0%)');
        const title = isAgeGender ? d.segment : `Interest ${{d.interest_grouped}}`;

        html += `
          <div class="segment-row-card">
            <div class="segment-name-col">
              <strong>${{title}}</strong>
              <span>$${{Math.round(d.spend).toLocaleString()}} spend</span>
            </div>
            
            <div class="segment-metrics-col">
              <span>CPA: <strong>$${{d.cpa.toFixed(2)}}</strong></span> • 
              <span style="font-size: 11px; color: var(--text-muted);">${{d.rationale}}</span>
            </div>

            <div class="roas-col">
              ${{roas.toFixed(2)}}x
              <small>${{roas >= 1.0 ? 'Profitable' : 'Unprofitable'}}</small>
            </div>

            <div style="text-align: center;">
              <span class="shift-pill ${{shiftClass}}">${{shiftLabel}}</span>
            </div>

            <div class="new-spend-col">
              $${{Math.round(newSpend).toLocaleString()}}
            </div>
          </div>
        `;
      }});

      container.innerHTML = html;
    }}

    // Initialize Scatter Plot for Campaign 1178
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
              backgroundColor: 'rgba(25, 27, 31, 0.28)',
              borderColor: 'transparent',
              pointRadius: 3.5,
              pointHoverRadius: 6
            }},
            {{
              label: 'OLS Fitted Line (y = 0.32 + 0.0121x)',
              data: regressionLine,
              type: 'line',
              borderColor: '#FF6B4A',
              borderWidth: 3,
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
              labels: {{ color: '#636A79', font: {{ size: 12 }} }}
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
              grid: {{ color: '#EFECE6' }},
              ticks: {{ color: '#8E95A5' }}
            }},
            y: {{
              title: {{ display: true, text: 'Approved Conversions (Orders)', color: '#8E95A5' }},
              grid: {{ color: '#EFECE6' }},
              ticks: {{ color: '#8E95A5' }}
            }}
          }}
        }}
      }});
    }}

    // Event Listener
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

print("Generated light fintech dashboard 'index.html' successfully.")
