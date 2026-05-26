# Identification Strategy

## Research setting

The synthetic data represent household-finance regimes with different levels of mental-account segmentation, integrated balance-sheet prompting, windfall framing, savings-label strength, emergency risk, liquidity need, present bias, and household debt.

Regimes include:

1. `segmented_mental_accounts`
2. `integrated_balance_sheet_prompt`
3. `unified_fungible_money`

## Core estimands

- Effect of integrated balance-sheet prompts on windfall consumption, total debt payment, remaining debt, annual interest cost, and financial resilience.
- Effect of a unified fungible-money view on debt-savings inefficiency and resilience.
- Effect of savings-label strength on the use of liquid savings for high-interest debt repayment.
- Heterogeneous effects by emergency-risk, income, debt burden, liquidity need, and present bias.

## Baseline household-regime specification

```text
Y_i = alpha
    + beta_1 IntegratedPrompt_i
    + beta_2 UnifiedMoney_i
    + X_i'gamma
    + epsilon_i
```

where `Y_i` may be windfall consumption, total debt payment, remaining debt, inefficiency gap, annual interest cost, remaining liquid savings, or financial resilience.

## Key identification cautions for real data

- Mental accounts are often latent and may not match formal bank-account categories.
- Preserving cash while holding debt can be rational when households face income volatility or limited credit access.
- Windfall spending may meet overdue needs, not merely discretionary desire.
- A narrow debt-minimization metric can miss welfare losses from reduced liquidity.
- Households that adopt labeled savings tools may differ from those that do not.
- Digital-finance platforms can both reveal and manipulate mental-account categories.
- Account labels may be user-endorsed, defaulted, institutionally imposed, or commercially exploited.

Because the data here are synthetic, estimates are not empirical claims about any actual household, bank, budgeting app, credit product, or public program. The value of the workflow is methodological.
