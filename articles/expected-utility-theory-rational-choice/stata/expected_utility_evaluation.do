clear all
set more off

* Expected Utility Theory and Rational Choice
* Stata risk-aversion and risky-choice workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_expected_utility_panel.csv", clear varnames(1)

label variable rho "CRRA risk-aversion parameter"
label variable wealth "Initial wealth"
label variable numeracy "Numeracy proxy"
label variable liquidity_constraint "Liquidity constraint proxy"
label variable trust "Trust proxy"
label variable choose_risky_eu "Risky choice under expected utility"
label variable observed_choose_risky "Observed risky choice with implementation frictions"
label variable certainty_equivalent_payoff "Certainty equivalent payoff"
label variable risk_premium "Risk premium"

local controls medium_risk_aversion_treat high_risk_aversion_treat wealth rho numeracy liquidity_constraint trust
local outcomes choose_risky_eu observed_choose_risky certainty_equivalent_payoff risk_premium

tempname handle
postfile `handle' str55 outcome str55 term double estimate double std_error double p_value double n using "$REG/stata_expected_utility_estimates.dta", replace

foreach y of local outcomes {
    regress `y' `controls', vce(robust)

    foreach x in medium_risk_aversion_treat high_risk_aversion_treat rho wealth numeracy liquidity_constraint trust {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_expected_utility_estimates.dta", clear
export delimited using "$REG/stata_expected_utility_estimates.csv", replace

* Heterogeneity by risk-aversion quartile.
import delimited "$TABLES/synthetic_expected_utility_panel.csv", clear varnames(1)

xtile rho_quartile = rho, nq(4)
xtile wealth_quartile = wealth, nq(4)

tempname h
postfile `h' str30 group str55 outcome double mean_value double n using "$REG/stata_expected_utility_heterogeneity.dta", replace

forvalues q = 1/4 {
    foreach y in choose_risky_eu observed_choose_risky certainty_equivalent_payoff risk_premium {
        summarize `y' if rho_quartile == `q'
        post `h' ("rho_q`q'") ("`y'") (r(mean)) (r(N))

        summarize `y' if wealth_quartile == `q'
        post `h' ("wealth_q`q'") ("`y'") (r(mean)) (r(N))
    }
}

postclose `h'

use "$REG/stata_expected_utility_heterogeneity.dta", clear
export delimited using "$REG/stata_expected_utility_heterogeneity.csv", replace

display "Stata expected-utility workflow complete."
