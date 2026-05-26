clear all
set more off

* Mental Accounting in Personal Finance
* Stata household-finance evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_mental_accounting_household_panel.csv", clear varnames(1)

label variable integrated_prompt_treat "Integrated balance-sheet prompt treatment"
label variable unified_money_treat "Unified fungible-money treatment"
label variable windfall_consumption "Windfall consumption"
label variable total_debt_payment "Total debt payment"
label variable remaining_debt "Remaining credit-card debt"
label variable inefficiency_gap "Debt-savings inefficiency gap"
label variable annual_interest_cost "Annual interest cost"
label variable resilience_index "Financial resilience index"

local controls monthly_income liquid_savings credit_card_debt windfall savings_label_strength emergency_need_risk present_bias
local outcomes windfall_consumption total_debt_payment remaining_debt remaining_liquid_savings inefficiency_gap annual_interest_cost resilience_index

tempname handle
postfile `handle' str55 outcome str55 term double estimate double std_error double p_value double n using "$REG/stata_mental_accounting_estimates.dta", replace

foreach y of local outcomes {
    regress `y' integrated_prompt_treat unified_money_treat `controls', vce(robust)

    foreach x in integrated_prompt_treat unified_money_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_mental_accounting_estimates.dta", clear
export delimited using "$REG/stata_mental_accounting_estimates.csv", replace

* Heterogeneity by savings-label strength.
import delimited "$TABLES/synthetic_mental_accounting_household_panel.csv", clear varnames(1)

xtile label_quartile = savings_label_strength, nq(4)

tempname h
postfile `h' str30 group str55 term double estimate double std_error double p_value double n using "$REG/stata_mental_accounting_label_heterogeneity.dta", replace

forvalues q = 1/4 {
    regress inefficiency_gap integrated_prompt_treat unified_money_treat `controls' if label_quartile == `q', vce(robust)

    foreach x in integrated_prompt_treat unified_money_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `h' ("label_q`q'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `h'

use "$REG/stata_mental_accounting_label_heterogeneity.dta", clear
export delimited using "$REG/stata_mental_accounting_label_heterogeneity.csv", replace

display "Stata mental-accounting household-finance workflow complete."
