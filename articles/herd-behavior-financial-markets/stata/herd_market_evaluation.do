clear all
set more off

* Herd Behavior in Financial Markets
* Stata market-regime evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_herd_market_experiment.csv", clear varnames(1)

label variable moderate_herding_treat "Moderate herding treatment"
label variable high_herding_treat "High herding crowded-trade treatment"
label variable price "Simulated market price"
label variable price_deviation "Price deviation from baseline"
label variable buy_rate "Aggregate buy rate"
label variable volatility_proxy "Absolute price-impact volatility proxy"
label variable systemic_herding_risk "Crowding leverage liquidity risk proxy"

local controls liquidity_depth leverage_pressure social_media_intensity post_shock
local outcomes price price_deviation buy_rate volatility_proxy drawdown_from_peak systemic_herding_risk

tempname handle
postfile `handle' str50 outcome str45 term double estimate double std_error double p_value double n using "$REG/stata_herd_market_estimates.dta", replace

foreach y of local outcomes {
    regress `y' moderate_herding_treat high_herding_treat `controls', vce(robust)

    foreach x in moderate_herding_treat high_herding_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_herd_market_estimates.dta", clear
export delimited using "$REG/stata_herd_market_estimates.csv", replace

* Shock-window diagnostics.
import delimited "$TABLES/synthetic_herd_market_experiment.csv", clear varnames(1)

collapse (mean) price buy_rate volatility_proxy drawdown_from_peak systemic_herding_risk, by(regime post_shock)
export delimited using "$REG/stata_herd_market_shock_window_summary.csv", replace

display "Stata herd behavior market-regime evaluation workflow complete."
