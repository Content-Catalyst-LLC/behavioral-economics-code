clear all
set more off

* Overconfidence Bias in Financial Markets
* Stata investor-regime evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_overconfidence_experiment.csv", clear varnames(1)

label variable moderate_overconfidence_treat "Moderate overconfidence treatment"
label variable high_overconfidence_treat "High overconfidence low-friction treatment"
label variable mean_trade_intensity "Mean trading intensity"
label variable mean_trading_cost "Mean trading cost"
label variable mean_realized_return "Mean realized return"
label variable volatility_proxy "Return volatility proxy"

local controls trading_friction leverage_access
local outcomes mean_trade_intensity mean_trading_cost mean_gross_position_return mean_realized_return volatility_proxy mean_abs_perceived_signal portfolio_drag

tempname handle
postfile `handle' str55 outcome str55 term double estimate double std_error double p_value double n using "$REG/stata_overconfidence_estimates.dta", replace

foreach y of local outcomes {
    regress `y' moderate_overconfidence_treat high_overconfidence_treat `controls', vce(robust)

    foreach x in moderate_overconfidence_treat high_overconfidence_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_overconfidence_estimates.dta", clear
export delimited using "$REG/stata_overconfidence_estimates.csv", replace

* Regime summary.
import delimited "$TABLES/synthetic_overconfidence_experiment.csv", clear varnames(1)
collapse (mean) mean_trade_intensity mean_trading_cost mean_gross_position_return mean_realized_return volatility_proxy mean_abs_perceived_signal portfolio_drag, by(regime)
export delimited using "$REG/stata_overconfidence_regime_summary.csv", replace

display "Stata overconfidence investor-regime evaluation workflow complete."
