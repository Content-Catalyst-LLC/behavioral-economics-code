clear all
set more off

* Status Quo Bias and Institutional Inertia
* Stata default-retention evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_status_quo_bias_panel.csv", clear varnames(1)

label variable active_choice_treat "Active choice with disclosure treatment"
label variable pro_switching_treat "Pro-switching default with support treatment"
label variable choose_alternative "Alternative adoption indicator"
label variable welfare "Synthetic welfare"
label variable switch_cost "Switching cost"
label variable loss_aversion "Loss aversion"
label variable status_quo_premium "Status quo premium"

local controls objective_gain switch_cost loss_aversion status_quo_premium uncertainty_sensitivity decision_fatigue sophistication default_shift switching_support disclosure_quality
local outcomes choose_alternative welfare effective_switch_cost effective_status_quo_premium effective_perceived_loss

tempname handle
postfile `handle' str55 outcome str55 term double estimate double std_error double p_value double n using "$REG/stata_status_quo_bias_estimates.dta", replace

foreach y of local outcomes {
    regress `y' active_choice_treat pro_switching_treat `controls', vce(robust)

    foreach x in active_choice_treat pro_switching_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_status_quo_bias_estimates.dta", clear
export delimited using "$REG/stata_status_quo_bias_estimates.csv", replace

* Heterogeneity by switching-cost quartile.
import delimited "$TABLES/synthetic_status_quo_bias_panel.csv", clear varnames(1)

xtile switch_cost_quartile = switch_cost, nq(4)

tempname h
postfile `h' str30 group str55 term double estimate double std_error double p_value double n using "$REG/stata_status_quo_bias_switching_heterogeneity.dta", replace

forvalues q = 1/4 {
    regress choose_alternative active_choice_treat pro_switching_treat `controls' if switch_cost_quartile == `q', vce(robust)

    foreach x in active_choice_treat pro_switching_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `h' ("switch_q`q'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `h'

use "$REG/stata_status_quo_bias_switching_heterogeneity.dta", clear
export delimited using "$REG/stata_status_quo_bias_switching_heterogeneity.csv", replace

display "Stata status quo bias evaluation workflow complete."
