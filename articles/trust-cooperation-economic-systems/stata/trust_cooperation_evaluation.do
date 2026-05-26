clear all
set more off

* Trust and Cooperation in Economic Systems
* Stata policy-evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_trust_cooperation_experiment.csv", clear varnames(1)

local controls trust_propensity reciprocity punishment_willingness institutional_trust betrayal_sensitivity monitoring_cost_sensitivity
local outcomes trusted reciprocated punished transaction_cost_reduction monitoring_cost total_welfare

tempname handle
postfile `handle' str45 outcome str45 term double estimate double std_error double p_value double n using "$REG/stata_trust_cooperation_estimates.dta", replace

foreach y of local outcomes {
    regress `y' reciprocal_market_treat institutional_support_treat `controls', vce(robust)

    foreach x in reciprocal_market_treat institutional_support_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_trust_cooperation_estimates.dta", clear
export delimited using "$REG/stata_trust_cooperation_estimates.csv", replace

display "Stata trust and cooperation policy-evaluation workflow complete."
