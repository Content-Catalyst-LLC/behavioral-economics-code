clear all
set more off

* Nudge Theory and Behavioral Public Policy
* Stata policy-evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_nudge_policy_experiment.csv", clear varnames(1)

label variable reminder_norm_treat "Reminder plus social norm treatment"
label variable default_reminder_treat "Default plus reminder treatment"
label variable adopted "Simulated adoption outcome"
label variable total_welfare "Synthetic total welfare"
label variable user_benefit "Synthetic user benefit"
label variable social_benefit "Synthetic social benefit"

local controls default_sensitivity reminder_sensitivity norm_sensitivity friction_sensitivity present_bias administrative_burden_sensitivity trust
local outcomes adopted total_welfare user_benefit social_benefit friction_cost admin_cost implementation_cost

tempname handle
postfile `handle' str40 outcome str40 term double estimate double std_error double p_value double n using "$REG/stata_nudge_policy_estimates.dta", replace

foreach y of local outcomes {
    regress `y' reminder_norm_treat default_reminder_treat `controls', vce(robust)

    foreach x in reminder_norm_treat default_reminder_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_nudge_policy_estimates.dta", clear
export delimited using "$REG/stata_nudge_policy_estimates.csv", replace

* Heterogeneous welfare effect by present-bias quartile.
import delimited "$TABLES/synthetic_nudge_policy_experiment.csv", clear varnames(1)
xtile present_bias_quartile = present_bias, nq(4)

tempname h
postfile `h' str30 group str40 term double estimate double std_error double p_value double n using "$REG/stata_nudge_policy_heterogeneous_welfare_effects.dta", replace

forvalues q = 1/4 {
    regress total_welfare reminder_norm_treat default_reminder_treat `controls' if present_bias_quartile == `q', vce(robust)

    foreach x in reminder_norm_treat default_reminder_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `h' ("present_bias_q`q'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `h'

use "$REG/stata_nudge_policy_heterogeneous_welfare_effects.dta", clear
export delimited using "$REG/stata_nudge_policy_heterogeneous_welfare_effects.csv", replace

display "Stata nudge policy-evaluation workflow complete."
