clear all
set more off

* Behavioral Insights in Environmental Policy
* Stata policy-evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_environmental_policy_experiment.csv", clear varnames(1)

gen price_signal_only = (regime == "price_signal_only")

label variable norm_default_treat "Norm plus default treatment"
label variable integrated_treat "Integrated environmental policy design treatment"
label variable adopted "Simulated adoption outcome"
label variable total_welfare "Synthetic total welfare"
label variable environmental_benefit "Synthetic environmental benefit"
label variable fiscal_cost "Synthetic fiscal cost"
label variable admin_cost "Synthetic administrative cost"

local controls income energy_burden env_concern present_bias norm_sensitivity friction_sensitivity loss_aversion trust
local outcomes adopted total_welfare private_benefit environmental_benefit fiscal_cost admin_cost

tempname handle
postfile `handle' str35 outcome str35 term double estimate double std_error double p_value double n using "$REG/stata_environmental_policy_estimates.dta", replace

foreach y of local outcomes {
    regress `y' norm_default_treat integrated_treat `controls', vce(robust)

    foreach x in norm_default_treat integrated_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_environmental_policy_estimates.dta", clear
export delimited using "$REG/stata_environmental_policy_estimates.csv", replace

* Heterogeneous welfare effect by energy-burden quartile.
import delimited "$TABLES/synthetic_environmental_policy_experiment.csv", clear varnames(1)
xtile burden_quartile = energy_burden, nq(4)

tempname h
postfile `h' str30 group str35 term double estimate double std_error double p_value double n using "$REG/stata_environmental_policy_heterogeneous_welfare_effects.dta", replace

forvalues q = 1/4 {
    regress total_welfare norm_default_treat integrated_treat `controls' if burden_quartile == `q', vce(robust)

    foreach x in norm_default_treat integrated_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `h' ("burden_q`q'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `h'

use "$REG/stata_environmental_policy_heterogeneous_welfare_effects.dta", clear
export delimited using "$REG/stata_environmental_policy_heterogeneous_welfare_effects.csv", replace

display "Stata environmental policy-evaluation workflow complete."
