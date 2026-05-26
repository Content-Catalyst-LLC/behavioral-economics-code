clear all
set more off

* Time Discounting and Long-Term Decision-Making
* Stata intertemporal-choice evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_time_discounting_experiment.csv", clear varnames(1)

label variable present_bias_treat "Present-biased discounting treatment"
label variable commitment_support_treat "Present bias with commitment support treatment"
label variable choose_delayed "Delayed choice indicator"
label variable cumulative_delayed_choices "Cumulative delayed choices"
label variable cumulative_welfare "Synthetic cumulative welfare"

local controls beta delta sophistication liquidity_need immediate_reward_base future_goal_value commitment_support flexibility
local outcomes choose_delayed cumulative_delayed_choices cumulative_welfare

tempname handle
postfile `handle' str55 outcome str55 term double estimate double std_error double p_value double n using "$REG/stata_time_discounting_estimates.dta", replace

foreach y of local outcomes {
    regress `y' present_bias_treat commitment_support_treat `controls', vce(robust)

    foreach x in present_bias_treat commitment_support_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_time_discounting_estimates.dta", clear
export delimited using "$REG/stata_time_discounting_estimates.csv", replace

* Heterogeneity by present-bias quartile.
import delimited "$TABLES/synthetic_time_discounting_experiment.csv", clear varnames(1)

xtile beta_quartile = beta, nq(4)

tempname h
postfile `h' str30 group str55 term double estimate double std_error double p_value double n using "$REG/stata_time_discounting_beta_heterogeneity.dta", replace

forvalues q = 1/4 {
    regress cumulative_delayed_choices present_bias_treat commitment_support_treat `controls' if beta_quartile == `q', vce(robust)

    foreach x in present_bias_treat commitment_support_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `h' ("beta_q`q'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `h'

use "$REG/stata_time_discounting_beta_heterogeneity.dta", clear
export delimited using "$REG/stata_time_discounting_beta_heterogeneity.csv", replace

display "Stata time-discounting evaluation workflow complete."
