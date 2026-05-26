clear all
set more off

* Behavioral Finance: Why Investors Deviate from Rational Models
* Stata market-regime evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_behavioral_finance_experiment.csv", clear varnames(1)

label variable medium_behavioral_treat "Medium behavioral distortion treatment"
label variable high_behavioral_treat "High behavioral distortion low-friction treatment"
label variable absolute_mispricing "Absolute mispricing"
label variable mean_trade_intensity "Mean trade intensity"
label variable mean_buy_rate "Mean buy rate"
label variable trading_cost_drag "Trading-cost drag"

local controls trading_friction platform_salience
local outcomes absolute_mispricing mean_trade_intensity mean_buy_rate trading_cost_drag mispricing drawdown_from_peak

tempname handle
postfile `handle' str55 outcome str55 term double estimate double std_error double p_value double n using "$REG/stata_behavioral_finance_estimates.dta", replace

foreach y of local outcomes {
    regress `y' medium_behavioral_treat high_behavioral_treat `controls', vce(robust)

    foreach x in medium_behavioral_treat high_behavioral_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_behavioral_finance_estimates.dta", clear
export delimited using "$REG/stata_behavioral_finance_estimates.csv", replace

* Regime summary.
import delimited "$TABLES/synthetic_behavioral_finance_experiment.csv", clear varnames(1)
collapse (mean) absolute_mispricing mean_trade_intensity mean_buy_rate trading_cost_drag mispricing drawdown_from_peak, by(regime)
export delimited using "$REG/stata_behavioral_finance_regime_summary.csv", replace

display "Stata behavioral-finance market-regime evaluation workflow complete."
