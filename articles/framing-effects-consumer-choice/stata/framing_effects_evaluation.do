clear all
set more off

* Framing Effects in Consumer Choice
* Stata framing-effects evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_framing_effects_panel.csv", clear varnames(1)

label variable loss_frame_treat "Loss frame treatment"
label variable balanced_frame_treat "Balanced absolute-risk frame treatment"
label variable choose_risky "Risky choice indicator"
label variable welfare_proxy "Synthetic welfare proxy"
label variable comprehension "Comprehension proxy"
label variable loss_aversion "Loss-aversion parameter"
label variable numeracy "Numeracy proxy"

local controls loss_aversion curvature numeracy trust decision_fatigue frame_strength disclosure_quality salience
local outcomes choose_risky welfare_proxy comprehension adjusted_risky_value

tempname handle
postfile `handle' str55 outcome str55 term double estimate double std_error double p_value double n using "$REG/stata_framing_effects_estimates.dta", replace

foreach y of local outcomes {
    regress `y' loss_frame_treat balanced_frame_treat `controls', vce(robust)

    foreach x in loss_frame_treat balanced_frame_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_framing_effects_estimates.dta", clear
export delimited using "$REG/stata_framing_effects_estimates.csv", replace

* Heterogeneity by loss-aversion quartile.
import delimited "$TABLES/synthetic_framing_effects_panel.csv", clear varnames(1)

xtile loss_aversion_quartile = loss_aversion, nq(4)

tempname h
postfile `h' str30 group str55 term double estimate double std_error double p_value double n using "$REG/stata_framing_effects_loss_aversion_heterogeneity.dta", replace

forvalues q = 1/4 {
    regress choose_risky loss_frame_treat balanced_frame_treat `controls' if loss_aversion_quartile == `q', vce(robust)

    foreach x in loss_frame_treat balanced_frame_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `h' ("loss_q`q'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `h'

use "$REG/stata_framing_effects_loss_aversion_heterogeneity.dta", clear
export delimited using "$REG/stata_framing_effects_loss_aversion_heterogeneity.csv", replace

display "Stata framing-effects evaluation workflow complete."
