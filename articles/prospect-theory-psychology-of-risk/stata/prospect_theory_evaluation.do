clear all
set more off

* Prospect Theory: How Humans Evaluate Risk and Uncertainty
* Stata framing and risk-choice workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_prospect_theory_panel.csv", clear varnames(1)

label variable lambda_loss "Loss-aversion coefficient"
label variable gamma_weight "Probability-weighting curvature"
label variable rho_crra "CRRA risk-aversion parameter"
label variable choose_risky_pt "Risky choice under prospect theory"
label variable choose_risky_eu "Risky choice under expected utility"
label variable pt_eu_disagreement "Prospect theory and expected utility disagreement"
label variable loss_frame_treat "Loss-frame treatment"
label variable mixed_gamble_treat "Mixed-gamble treatment"

local controls loss_frame_treat mixed_gamble_treat lambda_loss alpha_gain beta_loss gamma_weight rho_crra wealth numeracy income_security trust prior_loss_exposure
local outcomes choose_risky_pt choose_risky_eu pt_eu_disagreement pt_risky_value

tempname handle
postfile `handle' str55 outcome str55 term double estimate double std_error double p_value double n using "$REG/stata_prospect_theory_estimates.dta", replace

foreach y of local outcomes {
    regress `y' `controls', vce(robust)

    foreach x in loss_frame_treat mixed_gamble_treat lambda_loss alpha_gain beta_loss gamma_weight rho_crra wealth numeracy income_security trust prior_loss_exposure {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_prospect_theory_estimates.dta", clear
export delimited using "$REG/stata_prospect_theory_estimates.csv", replace

* Heterogeneity by loss aversion and probability weighting.
import delimited "$TABLES/synthetic_prospect_theory_panel.csv", clear varnames(1)

xtile lambda_quartile = lambda_loss, nq(4)
xtile gamma_quartile = gamma_weight, nq(4)

tempname h
postfile `h' str30 group str30 frame double share_choose_risky_pt double share_choose_risky_eu double disagreement_rate double n using "$REG/stata_prospect_theory_heterogeneity.dta", replace

levelsof frame, local(frames)

forvalues q = 1/4 {
    foreach f of local frames {
        summarize choose_risky_pt if lambda_quartile == `q' & frame == "`f'"
        local pt_share = r(mean)
        local n = r(N)

        summarize choose_risky_eu if lambda_quartile == `q' & frame == "`f'"
        local eu_share = r(mean)

        summarize pt_eu_disagreement if lambda_quartile == `q' & frame == "`f'"
        local disagree = r(mean)

        post `h' ("lambda_q`q'") ("`f'") (`pt_share') (`eu_share') (`disagree') (`n')

        summarize choose_risky_pt if gamma_quartile == `q' & frame == "`f'"
        local pt_share_g = r(mean)
        local n_g = r(N)

        summarize choose_risky_eu if gamma_quartile == `q' & frame == "`f'"
        local eu_share_g = r(mean)

        summarize pt_eu_disagreement if gamma_quartile == `q' & frame == "`f'"
        local disagree_g = r(mean)

        post `h' ("gamma_q`q'") ("`f'") (`pt_share_g') (`eu_share_g') (`disagree_g') (`n_g')
    }
}

postclose `h'

use "$REG/stata_prospect_theory_heterogeneity.dta", clear
export delimited using "$REG/stata_prospect_theory_heterogeneity.csv", replace

display "Stata prospect-theory workflow complete."
