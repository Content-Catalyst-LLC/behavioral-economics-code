program nudge_welfare
  implicit none

  integer :: adopted
  real :: utility, user_benefit, social_benefit
  real :: friction_cost, admin_cost, implementation_cost, welfare

  utility = 0.65
  adopted = 1
  user_benefit = 0.50 * adopted
  social_benefit = 0.40 * adopted
  friction_cost = 0.06
  admin_cost = 0.05
  implementation_cost = 0.073

  welfare = utility + user_benefit + social_benefit - friction_cost - admin_cost - implementation_cost

  print *, "Synthetic nudge policy welfare:", welfare
end program nudge_welfare
