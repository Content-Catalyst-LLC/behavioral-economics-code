clear all
set more off

* Behavioral Regulation and Institutional Design
* Stata policy-evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_regulatory_policy_experiment.csv", clear varnames(1)

gen sanction_heavy_deterrence = (regime == "sanction_heavy_deterrence")

label variable simplification_treat "Simplification plus trust treatment"
label variable integrated_treat "Integrated behavioral regulation treatment"
label variable complied "Simulated compliance outcome"
label variable total_welfare "Synthetic total welfare"
label variable social_benefit "Synthetic social benefit"
label variable enforcement_cost "Synthetic enforcement cost"
label variable administrative_cost "Synthetic administrative cost"

local controls trust norm_sensitivity burden_sensitivity loss_aversion private_gain_noncompliance compliance_capacity
local outcomes complied total_welfare social_benefit compliance_cost enforcement_cost administrative_cost

tempname handle
postfile `handle' str35 outcome str35 term double estimate double std_error double p_value double n using "$REG/stata_regulatory_policy_estimates.dta", replace

foreach y of local outcomes {
    regress `y' simplification_treat integrated_treat `controls', vce(robust)

    foreach x in simplification_treat integrated_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_regulatory_policy_estimates.dta", clear
export delimited using "$REG/stata_regulatory_policy_estimates.csv", replace

* Heterogeneous welfare effect by trust quartile.
import delimited "$TABLES/synthetic_regulatory_policy_experiment.csv", clear varnames(1)
xtile trust_quartile = trust, nq(4)

tempname h
postfile `h' str30 group str35 term double estimate double std_error double p_value double n using "$REG/stata_regulatory_policy_heterogeneous_welfare_effects.dta", replace

forvalues q = 1/4 {
    regress total_welfare simplification_treat integrated_treat `controls' if trust_quartile == `q', vce(robust)

    foreach x in simplification_treat integrated_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `h' ("trust_q`q'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `h'

use "$REG/stata_regulatory_policy_heterogeneous_welfare_effects.dta", clear
export delimited using "$REG/stata_regulatory_policy_heterogeneous_welfare_effects.csv", replace

display "Stata regulatory policy-evaluation workflow complete."
