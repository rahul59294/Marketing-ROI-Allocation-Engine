import pandas as pd
import numpy as np
from scipy import stats

# 1. Load Data
df = pd.read_csv('KAG_conversion_data.csv')

# 2. Correct Dtypes
age_order = ['30-34', '35-39', '40-44', '45-49']
df['age'] = pd.Categorical(df['age'], categories=age_order, ordered=True)
df['gender'] = pd.Categorical(df['gender'], categories=['M', 'F'])
df['interest'] = df['interest'].astype(int)
df['xyz_campaign_id'] = df['xyz_campaign_id'].astype(int)

# 3. Engineer Fields (Guarding against division by zero)
df['CTR'] = np.where(df['Impressions'] > 0, df['Clicks'] / df['Impressions'], 0.0)
df['CPC'] = np.where(df['Clicks'] > 0, df['Spent'] / df['Clicks'], np.nan)
df['CPA'] = np.where(df['Approved_Conversion'] > 0, df['Spent'] / df['Approved_Conversion'], np.nan)
df['Click_to_Conversion_Rate'] = np.where(df['Clicks'] > 0, df['Total_Conversion'] / df['Clicks'], np.nan)
df['Conversion_to_Approval_Rate'] = np.where(df['Total_Conversion'] > 0, df['Approved_Conversion'] / df['Total_Conversion'], np.nan)
df['attribution_type'] = np.where(df['Clicks'] > 0, 'click_through', 'view_through')

# 4. Revenue & ROAS (Explicit Assumed Order_Value = $100 per Approved_Conversion)
ORDER_VALUE = 100.0  # Labeled assumption
df['Order_Value_Assumption'] = ORDER_VALUE
df['Revenue'] = df['Approved_Conversion'] * ORDER_VALUE
df['ROAS'] = np.where(df['Spent'] > 0, df['Revenue'] / df['Spent'], np.nan)
df['ROI_pct'] = np.where(df['Spent'] > 0, (df['Revenue'] - df['Spent']) / df['Spent'] * 100.0, np.nan)

# Save cleaned ad-level dataset
df.to_csv('cleaned_ad_level_performance.csv', index=False)
print("Saved 'cleaned_ad_level_performance.csv' successfully.")

# 5. Helper Function for Aggregated Tables
def build_aggregate_table(group_cols):
    agg = df.groupby(group_cols, observed=False).agg(
        Ad_Count=('ad_id', 'count'),
        Total_Spend=('Spent', 'sum'),
        Total_Revenue=('Revenue', 'sum'),
        Total_Impressions=('Impressions', 'sum'),
        Total_Clicks=('Clicks', 'sum'),
        Total_Inquiries=('Total_Conversion', 'sum'),
        Total_Approved=('Approved_Conversion', 'sum')
    ).reset_index()
    
    # Portfolio level ratios (sum / sum)
    agg['ROAS'] = np.where(agg['Total_Spend'] > 0, agg['Total_Revenue'] / agg['Total_Spend'], np.nan)
    agg['ROI_pct'] = np.where(agg['Total_Spend'] > 0, (agg['Total_Revenue'] - agg['Total_Spend']) / agg['Total_Spend'] * 100.0, np.nan)
    agg['CPA'] = np.where(agg['Total_Approved'] > 0, agg['Total_Spend'] / agg['Total_Approved'], np.nan)
    agg['CTR_pct'] = np.where(agg['Total_Impressions'] > 0, (agg['Total_Clicks'] / agg['Total_Impressions']) * 100.0, 0.0)
    agg['CPC'] = np.where(agg['Total_Clicks'] > 0, agg['Total_Spend'] / agg['Total_Clicks'], np.nan)
    agg['Inquiry_Conversion_Rate_pct'] = np.where(agg['Total_Clicks'] > 0, (agg['Total_Inquiries'] / agg['Total_Clicks']) * 100.0, np.nan)
    agg['Approved_Conversion_Rate_pct'] = np.where(agg['Total_Clicks'] > 0, (agg['Total_Approved'] / agg['Total_Clicks']) * 100.0, np.nan)
    agg['Approval_Rate_pct'] = np.where(agg['Total_Inquiries'] > 0, (agg['Total_Approved'] / agg['Total_Inquiries']) * 100.0, np.nan)
    return agg

# Table 1: By xyz_campaign_id
t1 = build_aggregate_table(['xyz_campaign_id'])
print('\n' + '='*50)
print('TABLE 1: PERFORMANCE BY XYZ_CAMPAIGN_ID')
print('='*50)
print(t1.to_string(index=False))

# Table 2: By age
t2 = build_aggregate_table(['age'])
print('\n' + '='*50)
print('TABLE 2: PERFORMANCE BY AGE')
print('='*50)
print(t2.to_string(index=False))

# Table 3: By gender
t3 = build_aggregate_table(['gender'])
print('\n' + '='*50)
print('TABLE 3: PERFORMANCE BY GENDER')
print('='*50)
print(t3.to_string(index=False))

# Table 4: By interest (Top 15 by spend + 'Other')
spend_by_interest = df.groupby('interest')['Spent'].sum().sort_values(ascending=False)
top_15_interests = spend_by_interest.head(15).index.tolist()
df['interest_grouped'] = df['interest'].apply(lambda x: str(x) if x in top_15_interests else 'Other')
interest_order = [str(x) for x in top_15_interests] + ['Other']
df['interest_grouped'] = pd.Categorical(df['interest_grouped'], categories=interest_order, ordered=True)

t4 = build_aggregate_table(['interest_grouped'])
print('\n' + '='*50)
print('TABLE 4: PERFORMANCE BY INTEREST (TOP 15 BY SPEND + OTHER)')
print('='*50)
print(t4.to_string(index=False))

# Table 5: By age x gender combined
t5 = build_aggregate_table(['age', 'gender'])
print('\n' + '='*50)
print('TABLE 5: PERFORMANCE BY AGE X GENDER COMBINED')
print('='*50)
print(t5.to_string(index=False))

# 6. Within-Campaign Linear Regressions
print('\n' + '='*50)
print('WITHIN-CAMPAIGN LINEAR REGRESSIONS (Approved_Conversion ~ Spent)')
print('='*50)
for camp in [916, 936, 1178]:
    sub = df[df['xyz_campaign_id'] == camp]
    reg = stats.linregress(sub['Spent'], sub['Approved_Conversion'])
    marginal_cost = 1.0 / reg.slope if reg.slope > 0 else np.nan
    avg_cpa = sub['Spent'].sum() / sub['Approved_Conversion'].sum()
    
    # Also evaluate Spent-normalized conversion rate regression or residual stats
    print(f"\n--- Campaign {camp} (n = {len(sub)} ads) ---")
    print(f"Total Spend: ${sub['Spent'].sum():,.2f} | Total Approved: {sub['Approved_Conversion'].sum()} | Average CPA: ${avg_cpa:.2f}")
    print(f"Regression Equation: Approved_Conversion = {reg.intercept:.4f} + {reg.slope:.5f} * Spent")
    print(f"  Slope (beta_1):                {reg.slope:.5f} conversions per $1.00 spent")
    print(f"  Intercept (beta_0):            {reg.intercept:.4f} (baseline conversions at $0 spend)")
    print(f"  Standard Error of Slope:       {reg.stderr:.5f}")
    print(f"  R-squared (R^2):               {reg.rvalue**2:.4f} (Correlation r = {reg.rvalue:.4f})")
    print(f"  p-value:                       {reg.pvalue:.4e}")
    print(f"  Within-Campaign Marginal Cost: ${marginal_cost:.2f} per incremental approved conversion")
    print(f"  Marginal vs Average CPA Ratio: {marginal_cost / avg_cpa:.2f}x")
