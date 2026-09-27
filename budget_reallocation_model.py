import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('cleaned_ad_level_performance.csv')

def run_reallocation_analysis(order_value=100.0):
    total_spend = df['Spent'].sum()
    total_approved = df['Approved_Conversion'].sum()
    portfolio_cpa = total_spend / total_approved
    portfolio_roas = order_value / portfolio_cpa
    portfolio_roi = (order_value - portfolio_cpa) / portfolio_cpa * 100

    print("="*70)
    print(f"PORTFOLIO BENCHMARK (ASSUMED_ORDER_VALUE = ${order_value:.2f})")
    print(f"Total Spend: ${total_spend:,.2f} | Total Approved: {total_approved}")
    print(f"Portfolio CPA: ${portfolio_cpa:.2f} | Portfolio ROAS: {portfolio_roas:.2f}x | Portfolio ROI: {portfolio_roi:.1f}%")
    print(f"Breakeven CPA Threshold: ${order_value:.2f}")
    print("="*70)

    # 1. AGE X GENDER SEGMENT ANALYSIS
    ag = df.groupby(['age', 'gender'], observed=False).agg(
        Spend=('Spent', 'sum'),
        Approved=('Approved_Conversion', 'sum'),
        Clicks=('Clicks', 'sum'),
        Impressions=('Impressions', 'sum')
    ).reset_index()

    ag['Segment'] = ag['age'].astype(str) + " " + ag['gender'].astype(str)
    ag['CPA'] = ag['Spend'] / ag['Approved']
    ag['ROAS'] = order_value / ag['CPA']
    ag['ROI_pct'] = (order_value - ag['CPA']) / ag['CPA'] * 100
    ag['CTR_pct'] = ag['Clicks'] / ag['Impressions'] * 100
    ag['CVR_pct'] = ag['Approved'] / ag['Clicks'] * 100

    # Rule-based shift assignment:
    # Scale up if ROAS > 1.2 * portfolio_roas
    # Scale down if ROAS < 0.8 * portfolio_roas or ROAS < 1.0 (unprofitable)
    # Neutral if within [0.8, 1.2] * portfolio_roas
    shifts = []
    rationales = []
    
    for idx, row in ag.iterrows():
        roas = row['ROAS']
        cpa = row['CPA']
        if roas >= 1.5 * portfolio_roas: # Exceptionally high (> 2.76x)
            shift = +0.25 # +25%
            rat = f"Top-tier performer (ROAS {roas:.2f}x, CPA ${cpa:.2f}). Scale up aggressively within safe marginal bounds."
        elif roas >= 1.15 * portfolio_roas: # Moderately high (2.1x - 2.76x)
            shift = +0.15 # +15%
            rat = f"Strong performer (ROAS {roas:.2f}x, CPA ${cpa:.2f}). Scale up moderately."
        elif roas < 1.0: # Below breakeven
            shift = -0.30 # -30% (capped cut)
            rat = f"Unprofitable at Order Value ${order_value:.0f} (ROAS {roas:.2f}x < 1.0, CPA ${cpa:.2f}). Trim spend by maximum safe cap (-30%)."
        elif roas <= 0.75 * portfolio_roas: # Weak performer
            shift = -0.20 # -20%
            rat = f"Significantly below portfolio average (ROAS {roas:.2f}x, CPA ${cpa:.2f}). Reduce spend by -20%."
        elif roas < 0.90 * portfolio_roas: # Mildly lagging
            shift = -0.10 # -10%
            rat = f"Lagging portfolio average (ROAS {roas:.2f}x, CPA ${cpa:.2f}). Moderate trim (-10%)."
        else: # Neutral
            shift = 0.0
            rat = f"Performing near portfolio benchmark (ROAS {roas:.2f}x, CPA ${cpa:.2f}). Maintain current spend."
        
        shifts.append(shift)
        rationales.append(rat)

    ag['Recommended_Shift_pct'] = [s * 100 for s in shifts]
    ag['New_Spend'] = ag['Spend'] * (1 + np.array(shifts))
    ag['Spend_Change'] = ag['New_Spend'] - ag['Spend']
    ag['Rationale'] = rationales

    # Estimated Conversions & Revenue Impact:
    # Use conservative diminishing return assumption: marginal CPA = CPA * 1.15 for scaling up, and saving at average CPA for scaling down
    # Or linear conversion at segment CPA
    ag['Estimated_Approved_Change'] = np.where(
        ag['Spend_Change'] > 0,
        ag['Spend_Change'] / (ag['CPA'] * 1.15), # 15% marginal penalty on scale-up
        ag['Spend_Change'] / ag['CPA']           # savings at current CPA
    )
    ag['Estimated_Revenue_Change'] = ag['Estimated_Approved_Change'] * order_value
    ag['Estimated_Profit_Change'] = ag['Estimated_Revenue_Change'] - ag['Spend_Change']

    print("\n--- AGE X GENDER RECOMMENDED REALLOCATION ---")
    cols_display = ['Segment', 'Spend', 'ROAS', 'CPA', 'Recommended_Shift_pct', 'Spend_Change', 'Estimated_Revenue_Change', 'Estimated_Profit_Change']
    print(ag[cols_display].to_string(index=False))

    net_spend_change = ag['Spend_Change'].sum()
    net_rev_change = ag['Estimated_Revenue_Change'].sum()
    net_profit_change = ag['Estimated_Profit_Change'].sum()

    print(f"\nNet Budget Change: ${net_spend_change:,.2f}")
    print(f"Net Estimated Revenue Impact: ${net_rev_change:,.2f}")
    print(f"Net Estimated Profit Impact:  ${net_profit_change:,.2f}")

    # 2. INTEREST REALLOCATION
    spend_by_interest = df.groupby('interest')['Spent'].sum().sort_values(ascending=False)
    top_15 = spend_by_interest.head(15).index.tolist()
    df['interest_grouped'] = df['interest'].apply(lambda x: str(x) if x in top_15 else 'Other')

    ig = df.groupby('interest_grouped', observed=False).agg(
        Spend=('Spent', 'sum'),
        Approved=('Approved_Conversion', 'sum'),
        Clicks=('Clicks', 'sum')
    ).reset_index()

    ig['CPA'] = ig['Spend'] / ig['Approved']
    ig['ROAS'] = order_value / ig['CPA']
    ig['ROI_pct'] = (order_value - ig['CPA']) / ig['CPA'] * 100
    
    # Sort by spend descending
    ig = ig.sort_values(by='Spend', ascending=False).reset_index(drop=True)

    int_shifts = []
    int_rationales = []
    for idx, row in ig.iterrows():
        roas = row['ROAS']
        cpa = row['CPA']
        if roas >= 1.3 * portfolio_roas: # High efficiency (ROAS > 2.39x)
            shift = +0.20
            rat = f"High ROI interest (ROAS {roas:.2f}x, CPA ${cpa:.2f}). Scale up budget by +20%."
        elif roas >= 1.1 * portfolio_roas: # Moderately high
            shift = +0.10
            rat = f"Above average efficiency (ROAS {roas:.2f}x, CPA ${cpa:.2f}). Scale up budget by +10%."
        elif roas < 1.05: # Near or below breakeven
            shift = -0.25
            rat = f"Near breakeven / low efficiency (ROAS {roas:.2f}x, CPA ${cpa:.2f}). Reduce spend by -25%."
        elif roas < 0.8 * portfolio_roas: # Below average
            shift = -0.15
            rat = f"Sub-par efficiency (ROAS {roas:.2f}x, CPA ${cpa:.2f}). Trim spend by -15%."
        else:
            shift = 0.0
            rat = f"Average efficiency (ROAS {roas:.2f}x, CPA ${cpa:.2f}). Maintain spend."
        int_shifts.append(shift)
        int_rationales.append(rat)

    ig['Recommended_Shift_pct'] = [s * 100 for s in int_shifts]
    ig['New_Spend'] = ig['Spend'] * (1 + np.array(int_shifts))
    ig['Spend_Change'] = ig['New_Spend'] - ig['Spend']
    ig['Rationale'] = int_rationales

    ig['Estimated_Approved_Change'] = np.where(
        ig['Spend_Change'] > 0,
        ig['Spend_Change'] / (ig['CPA'] * 1.15),
        ig['Spend_Change'] / ig['CPA']
    )
    ig['Estimated_Revenue_Change'] = ig['Estimated_Approved_Change'] * order_value
    ig['Estimated_Profit_Change'] = ig['Estimated_Revenue_Change'] - ig['Spend_Change']

    print("\n--- TOP INTERESTS RECOMMENDED REALLOCATION ---")
    print(ig[['interest_grouped', 'Spend', 'ROAS', 'CPA', 'Recommended_Shift_pct', 'Spend_Change', 'Estimated_Revenue_Change', 'Estimated_Profit_Change']].to_string(index=False))

    return ag, ig

if __name__ == '__main__':
    run_reallocation_analysis(100.0)
