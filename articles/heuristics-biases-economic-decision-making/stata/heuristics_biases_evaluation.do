clear all
set more off

* Heuristics and Biases in Economic Decision-Making
* Stata judgment-error evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_heuristics_biases_panel.csv", clear varnames(1)

label variable medium_bias_treat "Medium-bias environment"
label variable high_bias_treat "High-bias low-context environment"
label variable estimated_value "Estimated target value"
label variable judgment_error "Estimate minus true value"
label variable absolute_error "Absolute judgment error"
label variable decision_quality "Synthetic decision-quality index"
label variable welfare_proxy "Synthetic welfare proxy"

local controls correction_capacity numeracy domain_knowledge cognitive_load confidence disclosure_quality debiasing_support availability_signal representativeness_signal anchor_signal framing_signal
local outcomes estimated_value judgment_error absolute_error decision_quality welfare_proxy

tempname handle
postfile `handle' str55 outcome str55 term double estimate double std_error double p_value double n using "$REG/stata_heuristics_biases_estimates.dta", replace

foreach y of local outcomes {
    regress `y' medium_bias_treat high_bias_treat `controls', vce(robust)

    foreach x in medium_bias_treat high_bias_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_heuristics_biases_estimates.dta", clear
export delimited using "$REG/stata_heuristics_biases_estimates.csv", replace

* Heterogeneity by correction-capacity quartile.
import delimited "$TABLES/synthetic_heuristics_biases_panel.csv", clear varnames(1)

xtile correction_quartile = correction_capacity, nq(4)

tempname h
postfile `h' str30 group str55 term double estimate double std_error double p_value double n using "$REG/stata_heuristics_biases_correction_heterogeneity.dta", replace

forvalues q = 1/4 {
    regress absolute_error medium_bias_treat high_bias_treat `controls' if correction_quartile == `q', vce(robust)

    foreach x in medium_bias_treat high_bias_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `h' ("correction_q`q'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `h'

use "$REG/stata_heuristics_biases_correction_heterogeneity.dta", clear
export delimited using "$REG/stata_heuristics_biases_correction_heterogeneity.csv", replace

display "Stata heuristics-and-biases evaluation workflow complete."
