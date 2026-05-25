program adoption_kernel
  implicit none

  real(8) :: income, environmental_concern, present_bias, loss_aversion
  real(8) :: norm_sensitivity, friction_sensitivity, quality_uncertainty
  real(8) :: infrastructure_access, subsidy, norm_signal, friction
  real(8) :: effective_premium, affordability, immediate_cost, utility_diff, probability
  integer :: default_green

  income = 65000.0d0
  environmental_concern = 0.62d0
  present_bias = 0.28d0
  loss_aversion = 2.0d0
  norm_sensitivity = 0.55d0
  friction_sensitivity = 0.50d0
  quality_uncertainty = 0.25d0
  infrastructure_access = 0.60d0
  subsidy = 0.05d0
  default_green = 1
  norm_signal = 0.70d0
  friction = 0.08d0

  effective_premium = max(0.10d0 - subsidy, 0.0d0)
  affordability = 1.0d0 / log(income)
  immediate_cost = effective_premium * affordability * 100.0d0 + friction * friction_sensitivity

  utility_diff = -0.65d0 &
      + 1.10d0 * environmental_concern &
      + 0.72d0 * default_green &
      + 0.85d0 * norm_sensitivity * norm_signal &
      + 0.55d0 * infrastructure_access &
      - 1.75d0 * immediate_cost &
      - 0.38d0 * present_bias &
      - 0.35d0 * loss_aversion * effective_premium &
      - 0.62d0 * quality_uncertainty

  probability = 1.0d0 / (1.0d0 + exp(-utility_diff))

  print *, probability
end program adoption_kernel
