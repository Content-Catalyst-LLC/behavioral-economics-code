clear all
set more off

* Present Bias and the Psychology of Immediate Reward
* Stata intertemporal-choice evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_present_bias_experiment.csv", clear varnames(1)

label variable medium_commitment_treat "Medium commitment treatment"
label variable strong_commitment_treat "Strong commitment treatment"
label variable choose_delayed "Delayed choice indicator"
label variable cumulative_delayed_choices "Cumulative delayed choices"
label variable cumulative_welfare "Synthetic cumulative welfare"

local controls beta delta sophistication liquidity_need temptation_strength future_goal_value commitment_cost reminder_strength flexibility
local outcomes choose_delayed cumulative_delayed_choices cumulative_welfare

tempname handle
postfile `handle' str55 outcome str55 term double estimate double std_error double p_value double n using "$REG/stata_present_bias_estimates.dta", replace

foreach y of local outcomes {
    regress `y' medium_commitment_treat strong_commitment_treat `controls', vce(robust)

    foreach x in medium_commitment_treat strong_commitment_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_present_bias_estimates.dta", clear
export delimited using "$REG/stata_present_bias_estimates.csv", replace

* Heterogeneity by present-bias quartile.
import delimited "$TABLES/synthetic_present_bias_experiment.csv", clear varnames(1)

xtile beta_quartile = beta, nq(4)

tempname h
postfile `h' str30 group str55 term double estimate double std_error double p_value double n using "$REG/stata_present_bias_beta_heterogeneity.dta", replace

forvalues q = 1/4 {
    regress cumulative_delayed_choices medium_commitment_treat strong_commitment_treat `controls' if beta_quartile == `q', vce(robust)

    foreach x in medium_commitment_treat strong_commitment_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `h' ("beta_q`q'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `h'

use "$REG/stata_present_bias_beta_heterogeneity.dta", clear
export delimited using "$REG/stata_present_bias_beta_heterogeneity.csv", replace

display "Stata present-bias evaluation workflow complete."
