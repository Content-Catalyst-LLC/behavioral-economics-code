# Data Dictionary

## synthetic_status_quo_bias_panel.csv

- `agent_id`: synthetic decision-maker identifier
- `regime`: default and switching-support regime
- `value_status_quo`: objective value of current option
- `value_alternative`: objective value of alternative option
- `objective_gain`: alternative value minus status quo value
- `switch_cost`: baseline switching cost
- `effective_switch_cost`: switching cost after support
- `loss_aversion`: loss-aversion parameter
- `status_quo_premium`: baseline psychological default/status quo premium
- `effective_status_quo_premium`: premium after disclosure/default shift
- `perceived_loss`: perceived loss from leaving the status quo
- `effective_perceived_loss`: perceived loss after disclosure
- `uncertainty_sensitivity`: aversion to ambiguity around alternatives
- `decision_fatigue`: cognitive burden / limited attention proxy
- `sophistication`: ability to use information and switching support
- `utility_status_quo`: utility of remaining with current arrangement
- `utility_alternative`: utility of switching
- `choose_alternative`: alternative adoption indicator
- `welfare`: synthetic welfare index
- `default_shift`: degree to which regime moves baseline away from passive status quo
- `switching_support`: support that reduces switching burden
- `disclosure_quality`: quality of information/disclosure
- `active_choice_treat`: treatment indicator
- `pro_switching_treat`: treatment indicator

## status_quo_bias_regime_summary.csv

Regime-level adoption and welfare summary.

## default_design_sensitivity.csv

Sensitivity grid over default shift, switching support, disclosure quality, loss aversion, and status quo premium.
