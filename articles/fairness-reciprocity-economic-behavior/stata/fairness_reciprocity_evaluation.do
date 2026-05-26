clear all
set more off

* Fairness and Reciprocity in Economic Behavior
* Stata policy-evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_fairness_reciprocity_experiment.csv", clear varnames(1)

label variable unequal_cooperative_treat "Unequal but cooperative treatment"
label variable unequal_noncooperative_treat "Unequal noncooperative treatment"
label variable exploitative_low_process_treat "Exploitative low process fairness treatment"
label variable fairness_reciprocity_utility "Fairness and reciprocity utility"

local controls fairness_sensitivity reciprocity_sensitivity trust punishment_willingness process_fairness_weight
local outcomes fairness_reciprocity_utility rejected punished cooperated process_fairness total_welfare

tempname handle
postfile `handle' str50 outcome str50 term double estimate double std_error double p_value double n using "$REG/stata_fairness_reciprocity_estimates.dta", replace

foreach y of local outcomes {
    regress `y' unequal_cooperative_treat unequal_noncooperative_treat exploitative_low_process_treat `controls', vce(robust)

    foreach x in unequal_cooperative_treat unequal_noncooperative_treat exploitative_low_process_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_fairness_reciprocity_estimates.dta", clear
export delimited using "$REG/stata_fairness_reciprocity_estimates.csv", replace

* Heterogeneous welfare effect by fairness-sensitivity quartile.
import delimited "$TABLES/synthetic_fairness_reciprocity_experiment.csv", clear varnames(1)
xtile fairness_quartile = fairness_sensitivity, nq(4)

tempname h
postfile `h' str30 group str50 term double estimate double std_error double p_value double n using "$REG/stata_fairness_reciprocity_heterogeneous_welfare_effects.dta", replace

forvalues q = 1/4 {
    regress total_welfare unequal_cooperative_treat unequal_noncooperative_treat exploitative_low_process_treat `controls' if fairness_quartile == `q', vce(robust)

    foreach x in unequal_cooperative_treat unequal_noncooperative_treat exploitative_low_process_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `h' ("fairness_q`q'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `h'

use "$REG/stata_fairness_reciprocity_heterogeneous_welfare_effects.dta", clear
export delimited using "$REG/stata_fairness_reciprocity_heterogeneous_welfare_effects.csv", replace

display "Stata fairness and reciprocity policy-evaluation workflow complete."
