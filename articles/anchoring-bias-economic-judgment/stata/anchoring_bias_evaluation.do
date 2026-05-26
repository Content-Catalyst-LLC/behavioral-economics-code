clear all
set more off

* Anchoring Bias in Economic Judgment
* Stata anchoring-bias evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_anchoring_bias_panel.csv", clear varnames(1)

label variable low_anchor_treat "Low anchor treatment"
label variable high_anchor_treat "High anchor treatment"
label variable counter_context_treat "High anchor with counter-context treatment"
label variable estimate "Final estimate"
label variable bias "Estimate minus true value"
label variable absolute_error "Absolute estimation error"
label variable welfare_proxy "Synthetic welfare proxy"

local controls anchor_value adjustment_rate effective_adjustment numeracy confidence cognitive_load domain_knowledge disclosure_quality counter_anchor_support
local outcomes estimate bias absolute_error decision_quality welfare_proxy

tempname handle
postfile `handle' str55 outcome str55 term double estimate double std_error double p_value double n using "$REG/stata_anchoring_bias_estimates.dta", replace

foreach y of local outcomes {
    regress `y' low_anchor_treat high_anchor_treat counter_context_treat `controls', vce(robust)

    foreach x in low_anchor_treat high_anchor_treat counter_context_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_anchoring_bias_estimates.dta", clear
export delimited using "$REG/stata_anchoring_bias_estimates.csv", replace

* Heterogeneity by effective-adjustment quartile.
import delimited "$TABLES/synthetic_anchoring_bias_panel.csv", clear varnames(1)

xtile adjustment_quartile = effective_adjustment, nq(4)

tempname h
postfile `h' str30 group str55 term double estimate double std_error double p_value double n using "$REG/stata_anchoring_bias_adjustment_heterogeneity.dta", replace

forvalues q = 1/4 {
    regress absolute_error low_anchor_treat high_anchor_treat counter_context_treat `controls' if adjustment_quartile == `q', vce(robust)

    foreach x in low_anchor_treat high_anchor_treat counter_context_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `h' ("adjustment_q`q'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `h'

use "$REG/stata_anchoring_bias_adjustment_heterogeneity.dta", clear
export delimited using "$REG/stata_anchoring_bias_adjustment_heterogeneity.csv", replace

display "Stata anchoring-bias evaluation workflow complete."
