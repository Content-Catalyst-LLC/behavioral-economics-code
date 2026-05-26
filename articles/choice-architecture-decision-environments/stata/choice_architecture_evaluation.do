clear all
set more off

* Choice Architecture and Decision Environments
* Stata policy-evaluation workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_choice_architecture_experiment.csv", clear varnames(1)

label variable default_heavy_treat "Default-heavy architecture treatment"
label variable guided_design_treat "Low-complexity guided design treatment"
label variable realized_welfare "Synthetic realized welfare"
label variable chosen_utility "Architecture-adjusted chosen utility"
label variable selected_default "Selected default option"
label variable selected_high_value_option "Selected highest long-run value option"

local controls default_sensitivity salience_sensitivity framing_sensitivity complexity_sensitivity switching_cost_sensitivity digital_literacy institutional_trust
local outcomes realized_welfare chosen_utility selected_default selected_high_value_option cognitive_cost switching_cost

tempname handle
postfile `handle' str40 outcome str40 term double estimate double std_error double p_value double n using "$REG/stata_choice_architecture_estimates.dta", replace

foreach y of local outcomes {
    regress `y' default_heavy_treat guided_design_treat `controls', vce(robust)

    foreach x in default_heavy_treat guided_design_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_choice_architecture_estimates.dta", clear
export delimited using "$REG/stata_choice_architecture_estimates.csv", replace

* Heterogeneous welfare effect by complexity-sensitivity quartile.
import delimited "$TABLES/synthetic_choice_architecture_experiment.csv", clear varnames(1)
xtile complexity_quartile = complexity_sensitivity, nq(4)

tempname h
postfile `h' str30 group str40 term double estimate double std_error double p_value double n using "$REG/stata_choice_architecture_heterogeneous_welfare_effects.dta", replace

forvalues q = 1/4 {
    regress realized_welfare default_heavy_treat guided_design_treat `controls' if complexity_quartile == `q', vce(robust)

    foreach x in default_heavy_treat guided_design_treat {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `h' ("complexity_q`q'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `h'

use "$REG/stata_choice_architecture_heterogeneous_welfare_effects.dta", clear
export delimited using "$REG/stata_choice_architecture_heterogeneous_welfare_effects.csv", replace

display "Stata choice architecture policy-evaluation workflow complete."
