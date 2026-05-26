clear all
set more off

* Bounded Rationality: Cognitive Limits and Economic Decision-Making
* Stata search, satisficing, and cognitive-constraint workflow using synthetic data.

global ROOT "`c(pwd)'"
global TABLES "$ROOT/outputs/tables"
global REG "$ROOT/outputs/regression_tables"

capture mkdir "$REG"

import delimited "$TABLES/synthetic_bounded_rationality_panel.csv", clear varnames(1)

label variable chosen_value "Value of satisficing choice"
label variable optimal_value "Full-search optimal value"
label variable net_value "Chosen value net of search cost"
label variable optimization_gap "Full-search optimum minus chosen value"
label variable chosen_index "Sequential search depth"
label variable aspiration "Aspiration threshold"
label variable search_cost "Search cost"
label variable time_budget "Time budget"
label variable cognitive_capacity "Cognitive capacity"
label variable stress "Stress proxy"
label variable institutional_trust "Institutional trust proxy"
label variable digital_access "Digital access proxy"
label variable administrative_capacity "Administrative capacity proxy"
label variable medium_constraint_treat "Medium-constraint environment"
label variable high_constraint_treat "High-constraint environment"

local controls medium_constraint_treat high_constraint_treat aspiration search_cost time_budget cognitive_capacity numeracy stress institutional_trust digital_access income_security administrative_capacity
local outcomes chosen_value net_value optimization_gap chosen_index

tempname handle
postfile `handle' str55 outcome str55 term double estimate double std_error double p_value double n using "$REG/stata_bounded_rationality_estimates.dta", replace

foreach y of local outcomes {
    regress `y' `controls', vce(robust)

    foreach x in medium_constraint_treat high_constraint_treat aspiration search_cost time_budget cognitive_capacity numeracy stress institutional_trust digital_access income_security administrative_capacity {
        local b = _b[`x']
        local se = _se[`x']
        local p = 2 * ttail(e(df_r), abs(_b[`x'] / _se[`x']))
        local n = e(N)
        post `handle' ("`y'") ("`x'") (`b') (`se') (`p') (`n')
    }
}

postclose `handle'

use "$REG/stata_bounded_rationality_estimates.dta", clear
export delimited using "$REG/stata_bounded_rationality_estimates.csv", replace

* Heterogeneity by aspiration, stress, and cognitive capacity.
import delimited "$TABLES/synthetic_bounded_rationality_panel.csv", clear varnames(1)

xtile aspiration_quartile = aspiration, nq(4)
xtile stress_quartile = stress, nq(4)
xtile capacity_quartile = cognitive_capacity, nq(4)

tempname h
postfile `h' str35 group str30 regime double mean_chosen_value double mean_net_value double mean_optimization_gap double mean_search_depth double n using "$REG/stata_bounded_rationality_heterogeneity.dta", replace

levelsof regime, local(regimes)

forvalues q = 1/4 {
    foreach r of local regimes {
        summarize chosen_value if aspiration_quartile == `q' & regime == "`r'"
        local chosen = r(mean)
        local n = r(N)

        summarize net_value if aspiration_quartile == `q' & regime == "`r'"
        local net = r(mean)

        summarize optimization_gap if aspiration_quartile == `q' & regime == "`r'"
        local gap = r(mean)

        summarize chosen_index if aspiration_quartile == `q' & regime == "`r'"
        local depth = r(mean)

        post `h' ("aspiration_q`q'") ("`r'") (`chosen') (`net') (`gap') (`depth') (`n')

        summarize chosen_value if stress_quartile == `q' & regime == "`r'"
        local chosen_s = r(mean)
        local n_s = r(N)

        summarize net_value if stress_quartile == `q' & regime == "`r'"
        local net_s = r(mean)

        summarize optimization_gap if stress_quartile == `q' & regime == "`r'"
        local gap_s = r(mean)

        summarize chosen_index if stress_quartile == `q' & regime == "`r'"
        local depth_s = r(mean)

        post `h' ("stress_q`q'") ("`r'") (`chosen_s') (`net_s') (`gap_s') (`depth_s') (`n_s')

        summarize chosen_value if capacity_quartile == `q' & regime == "`r'"
        local chosen_c = r(mean)
        local n_c = r(N)

        summarize net_value if capacity_quartile == `q' & regime == "`r'"
        local net_c = r(mean)

        summarize optimization_gap if capacity_quartile == `q' & regime == "`r'"
        local gap_c = r(mean)

        summarize chosen_index if capacity_quartile == `q' & regime == "`r'"
        local depth_c = r(mean)

        post `h' ("capacity_q`q'") ("`r'") (`chosen_c') (`net_c') (`gap_c') (`depth_c') (`n_c')
    }
}

postclose `h'

use "$REG/stata_bounded_rationality_heterogeneity.dta", clear
export delimited using "$REG/stata_bounded_rationality_heterogeneity.csv", replace

display "Stata bounded-rationality workflow complete."
