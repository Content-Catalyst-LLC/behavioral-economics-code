program environmental_welfare
  implicit none

  integer :: adopted
  real :: private_benefit, environmental_benefit, fiscal_cost
  real :: admin_cost, friction_cost, welfare

  adopted = 1
  private_benefit = 0.26
  environmental_benefit = 0.90
  fiscal_cost = 0.06
  admin_cost = 0.058
  friction_cost = 0.04

  welfare = adopted + private_benefit + environmental_benefit - fiscal_cost - admin_cost - 0.20 * friction_cost

  print *, "Synthetic environmental policy welfare:", welfare
end program environmental_welfare
