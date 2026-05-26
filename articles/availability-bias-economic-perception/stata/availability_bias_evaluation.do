clear all
set more off

* Availability Bias and Economic Perception
* Stata risk-perception evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_availability_bias_panel.csv", clear varnames(1)

label variable medium_availability_treat "Medium availability environment"
label variable high_availability_treat "High availability / low base-rate environment"
label variable subjective_probability "Subjective probability"
label variable calibration_error "Subjective minus true probability"
label variable insurance_demand "Insurance demand indicator"
label variable policy_support "Policy support indicator"
label variable welfare_proxy "Synthetic welfare proxy"

local controls availability_sensitivity numeracy trust_in_statistics risk_tolerance prior_experience availability_score base_rate_disclosure emotional_intensity
local outcomes subjective_probability calibration_error participate_in_risky_asset insurance_demand policy_support welfare_proxy

tempname handle
postfile `handle' str55 outcome str55 term double estimate double std_error double p_value double n using "$REG/stata_availability_bias_estimates.dta", replace

foreach y of local outcomes {
    regress `y' medium_availability_treat high_availability_treat `controls', vce(robust)

    foreach x in medium_availability_treat high_availability_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_availability_bias_estimates.dta", clear
export delimited using "$REG/stata_availability_bias_estimates.csv", replace

* Heterogeneity by availability-sensitivity quartile.
import delimited "$TABLES/synthetic_availability_bias_panel.csv", clear varnames(1)

xtile availability_sensitivity_quartile = availability_sensitivity, nq(4)

tempname h
postfile `h' str30 group str55 term double estimate double std_error double p_value double n using "$REG/stata_availability_bias_sensitivity_heterogeneity.dta", replace

forvalues q = 1/4 {
    regress subjective_probability medium_availability_treat high_availability_treat `controls' if availability_sensitivity_quartile == `q', vce(robust)

    foreach x in medium_availability_treat high_availability_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `h' ("availability_q`q'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `h'

use "$REG/stata_availability_bias_sensitivity_heterogeneity.dta", clear
export delimited using "$REG/stata_availability_bias_sensitivity_heterogeneity.csv", replace

display "Stata availability-bias evaluation workflow complete."
