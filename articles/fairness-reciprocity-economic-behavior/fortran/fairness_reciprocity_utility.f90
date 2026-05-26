program fairness_reciprocity_utility
  implicit none
  real :: self_payoff, other_payoff, fairness_sensitivity
  real :: reciprocity_sensitivity, reciprocity_signal, process_fairness
  real :: disadvantage_penalty, reciprocity_component, process_component, utility

  self_payoff = 0.35
  other_payoff = 0.65
  fairness_sensitivity = 1.2
  reciprocity_sensitivity = 1.0
  reciprocity_signal = 0.40
  process_fairness = 0.70

  disadvantage_penalty = fairness_sensitivity * max(other_payoff - self_payoff, 0.0)
  reciprocity_component = reciprocity_sensitivity * reciprocity_signal
  process_component = 0.30 * process_fairness
  utility = self_payoff - disadvantage_penalty + reciprocity_component + process_component

  print *, "Fairness-reciprocity utility:", utility
end program fairness_reciprocity_utility
