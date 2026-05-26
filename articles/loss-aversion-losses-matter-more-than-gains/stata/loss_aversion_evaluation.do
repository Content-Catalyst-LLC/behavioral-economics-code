clear all
set more off

* Loss Aversion: Why Losses Matter More Than Gains
* Stata reference-dependent risk-choice workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_loss_aversion_panel.csv", clear varnames(1)

label variable lambda_loss "Loss-aversion coefficient"
label variable alpha_gain "Gain-domain curvature"
label variable beta_loss "Loss-domain curvature"
label variable choose_risky "Risky choice indicator"
label variable risky_value "Prospect-style value of risky option"
label variable loss_frame_treat "Loss-frame treatment"
label variable mixed_gamble_treat "Mixed-gamble treatment"
label variable income_security "Income-security proxy"
label variable prior_loss_exposure "Prior loss exposure"

local controls loss_frame_treat mixed_gamble_treat lambda_loss alpha_gain beta_loss numeracy income_security prior_loss_exposure trust
local outcomes choose_risky risky_value

tempname handle
postfile `handle' str55 outcome str55 term double estimate double std_error double p_value double n using "$REG/stata_loss_aversion_estimates.dta", replace

foreach y of local outcomes {
    regress `y' `controls', vce(robust)

    foreach x in loss_frame_treat mixed_gamble_treat lambda_loss alpha_gain beta_loss numeracy income_security prior_loss_exposure trust {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_loss_aversion_estimates.dta", clear
export delimited using "$REG/stata_loss_aversion_estimates.csv", replace

* Heterogeneity by loss-aversion quartile.
import delimited "$TABLES/synthetic_loss_aversion_panel.csv", clear varnames(1)

xtile lambda_quartile = lambda_loss, nq(4)

tempname h
postfile `h' str30 group str30 frame double share_choose_risky double mean_risky_value double n using "$REG/stata_loss_aversion_lambda_heterogeneity.dta", replace

levelsof frame, local(frames)

forvalues q = 1/4 {
    foreach f of local frames {
        summarize choose_risky if lambda_quartile == `q' & frame == "`f'"
        local share = r(mean)
        local n = r(N)

        summarize risky_value if lambda_quartile == `q' & frame == "`f'"
        local value = r(mean)

        post `h' ("lambda_q`q'") ("`f'") (`share') (`value') (`n')
    }
}

postclose `h'

use "$REG/stata_loss_aversion_lambda_heterogeneity.dta", clear
export delimited using "$REG/stata_loss_aversion_lambda_heterogeneity.csv", replace

display "Stata loss-aversion workflow complete."
