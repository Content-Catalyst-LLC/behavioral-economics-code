clear all
set more off

* Behavioral Design in Technology Systems
* Stata policy-evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_interface_experiment.csv", clear varnames(1)

gen supportive_design = (regime == "user_supportive_design")

label variable engagement_design "Engagement-maximizing interface"
label variable lockin_design "Friction-heavy lock-in interface"
label variable user_welfare "Synthetic user welfare"
label variable platform_value "Synthetic platform value"
label variable welfare_platform_gap "Platform value minus user welfare"

local controls baseline_value cognitive_overload privacy_sensitivity autonomy_preference digital_literacy
local outcomes joined retained consented user_welfare platform_value welfare_platform_gap

tempname handle
postfile `handle' str30 outcome str30 term double estimate double std_error double p_value double n using "$REG/stata_interface_policy_estimates.dta", replace

foreach y of local outcomes {
    regress `y' engagement_design lockin_design `controls', vce(robust)

    foreach x in engagement_design lockin_design {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_interface_policy_estimates.dta", clear
export delimited using "$REG/stata_interface_policy_estimates.csv", replace

* Heterogeneous welfare effect by cognitive overload quartile.
import delimited "$TABLES/synthetic_interface_experiment.csv", clear varnames(1)
xtile overload_quartile = cognitive_overload, nq(4)

tempname h
postfile `h' str30 group str30 term double estimate double std_error double p_value double n using "$REG/stata_heterogeneous_welfare_effects.dta", replace

forvalues q = 1/4 {
    regress user_welfare engagement_design lockin_design `controls' if overload_quartile == `q', vce(robust)

    foreach x in engagement_design lockin_design {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `h' ("overload_q`q'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `h'

use "$REG/stata_heterogeneous_welfare_effects.dta", clear
export delimited using "$REG/stata_heterogeneous_welfare_effects.csv", replace

display "Stata policy-evaluation workflow complete."
