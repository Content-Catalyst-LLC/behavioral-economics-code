# Data Dictionary

## synthetic_mental_accounting_household_panel.csv

- `household_id`: synthetic household identifier
- `regime`: segmented, integrated-prompt, or unified-money regime
- `monthly_income`: synthetic monthly household income
- `liquid_savings`: liquid savings balance
- `emergency_reserve`: separate emergency reserve
- `credit_card_debt`: high-interest consumer debt
- `windfall`: tax refund, bonus, rebate, or other unexpected income
- `savings_label_strength`: strength of psychological reluctance to spend labeled savings
- `emergency_need_risk`: probability/intensity proxy for needing liquidity
- `present_bias`: present-bias parameter
- `windfall_consumption`: amount of windfall spent
- `windfall_debt_payment`: amount of windfall allocated to debt
- `savings_available_for_debt`: liquid savings available after protected liquidity
- `savings_used_for_debt`: labeled savings used for debt repayment
- `total_debt_payment`: total debt repayment from windfall and savings
- `remaining_debt`: debt remaining after repayment
- `remaining_liquid_savings`: liquid savings remaining after repayment
- `inefficiency_gap`: remaining high-cost debt coexisting with available liquid savings
- `annual_interest_cost`: interest burden from remaining debt
- `resilience_index`: synthetic household financial resilience metric
- `integrated_prompt_treat`: treatment indicator for integrated balance-sheet prompt
- `unified_money_treat`: treatment indicator for unified fungible-money regime

## mental_accounting_regime_summary.csv

Regime-level comparison of household outcomes.

## windfall_spending_history.csv

Synthetic windfall-allocation experiment with spending, saving, and debt-repayment outcomes.
