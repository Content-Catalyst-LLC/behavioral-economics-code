clear all
set more off

* Inequality Aversion in Economic Decision-Making
* Stata policy-evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_inequality_aversion_experiment.csv", clear varnames(1)

label variable advantageous_treat "Advantageous inequality treatment"
label variable disadvantageous_treat "Disadvantageous inequality treatment"
label variable social_preference_utility "Fehr-Schmidt social preference utility"
label variable alpha "Disadvantageous inequality aversion"
label variable beta "Advantageous inequality aversion"

local controls alpha beta redistribution_norm merit_belief institutional_trust process_fairness_sensitivity
local outcomes social_preference_utility rejected support_redistribution process_legitimacy total_welfare

tempname handle
postfile `handle' str50 outcome str45 term double estimate double std_error double p_value double n using "$REG/stata_inequality_aversion_estimates.dta", replace

foreach y of local outcomes {
    regress `y' advantageous_treat disadvantageous_treat `controls', vce(robust)

    foreach x in advantageous_treat disadvantageous_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_inequality_aversion_estimates.dta", clear
export delimited using "$REG/stata_inequality_aversion_estimates.csv", replace

* Heterogeneous welfare effect by alpha quartile.
import delimited "$TABLES/synthetic_inequality_aversion_experiment.csv", clear varnames(1)
xtile alpha_quartile = alpha, nq(4)

tempname h
postfile `h' str30 group str45 term double estimate double std_error double p_value double n using "$REG/stata_inequality_aversion_heterogeneous_welfare_effects.dta", replace

forvalues q = 1/4 {
    regress total_welfare advantageous_treat disadvantageous_treat `controls' if alpha_quartile == `q', vce(robust)

    foreach x in advantageous_treat disadvantageous_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `h' ("alpha_q`q'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `h'

use "$REG/stata_inequality_aversion_heterogeneous_welfare_effects.dta", clear
export delimited using "$REG/stata_inequality_aversion_heterogeneous_welfare_effects.csv", replace

display "Stata inequality aversion policy-evaluation workflow complete."
