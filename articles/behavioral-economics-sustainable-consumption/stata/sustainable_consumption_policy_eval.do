*******************************************************
* Behavioral Economics and Sustainable Consumption
* Stata workflow: economist-grade policy evaluation scaffold
* Synthetic data only. Replace with validated empirical data.
*******************************************************

clear all
set more off

global ARTICLE "articles/behavioral-economics-sustainable-consumption"
global DATA "$ARTICLE/data/processed/synthetic_sustainable_consumption_panel.csv"
global OUT "$ARTICLE/outputs/tables"

capture mkdir "$OUT"

import delimited "$DATA", clear varnames(1)

* Basic panel declaration
xtset household_id period

* Difference-in-differences with household and period fixed effects
* For production research, consider reghdfe with robust clustered SEs.
areg adopted post_policy i.period, absorb(household_id) vce(cluster locality_id)

estimates store did_basic

* Distributional heterogeneity by income quintile
levelsof income_quintile, local(quintiles)

foreach q of local quintiles {
    di "Estimating DID for income quintile `q'"
    preserve
    keep if income_quintile == "`q'"
    areg adopted post_policy i.period, absorb(household_id) vce(cluster locality_id)
    restore
}

* Event-time construction
gen event_time = period - policy_start_period if treated_locality == 1

forvalues k = -3/3 {
    if `k' != -1 {
        local name = cond(`k' < 0, "event_m" + string(abs(`k')), "event_p" + string(`k'))
        gen `name' = (event_time == `k') if treated_locality == 1
        replace `name' = 0 if missing(`name')
    }
}

areg adopted event_m3 event_m2 event_p0 event_p1 event_p2 event_p3 i.period, absorb(household_id) vce(cluster locality_id)

*******************************************************
* End
*******************************************************
