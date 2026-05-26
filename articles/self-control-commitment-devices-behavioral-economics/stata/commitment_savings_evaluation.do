clear all
set more off

* Self-Control and Commitment Devices in Behavioral Economics
* Stata policy-evaluation scaffold using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_commitment_savings_experiment.csv", clear varnames(1)

label variable medium_commitment_treat "Medium commitment treatment"
label variable high_commitment_treat "High commitment treatment"
label variable accumulated_savings "Accumulated savings"
label variable actual_savings "Period savings"
label variable withdrawal "Emergency withdrawal"
label variable welfare "Synthetic welfare index"

local controls beta sophistication liquidity_need emergency_risk automation_strength flexibility
local outcomes accumulated_savings actual_savings withdrawal welfare

tempname handle
postfile `handle' str50 outcome str50 term double estimate double std_error double p_value double n using "$REG/stata_commitment_savings_estimates.dta", replace

foreach y of local outcomes {
    regress `y' medium_commitment_treat high_commitment_treat `controls', vce(robust)

    foreach x in medium_commitment_treat high_commitment_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_commitment_savings_estimates.dta", clear
export delimited using "$REG/stata_commitment_savings_estimates.csv", replace

* Heterogeneity by present-bias quartile.
import delimited "$TABLES/synthetic_commitment_savings_experiment.csv", clear varnames(1)

xtile beta_quartile = beta, nq(4)

tempname h
postfile `h' str30 group str50 term double estimate double std_error double p_value double n using "$REG/stata_commitment_beta_heterogeneity.dta", replace

forvalues q = 1/4 {
    regress accumulated_savings medium_commitment_treat high_commitment_treat `controls' if beta_quartile == `q', vce(robust)

    foreach x in medium_commitment_treat high_commitment_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `h' ("beta_q`q'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `h'

use "$REG/stata_commitment_beta_heterogeneity.dta", clear
export delimited using "$REG/stata_commitment_beta_heterogeneity.csv", replace

display "Stata commitment-device evaluation workflow complete."
