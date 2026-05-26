program regulatory_welfare
  implicit none

  integer :: complied
  real :: compliance_utility, admin_burden, burden_sensitivity
  real :: sanction_strength, social_benefit, compliance_cost
  real :: enforcement_cost, administrative_cost, welfare

  complied = 1
  compliance_utility = 0.70
  admin_burden = 0.10
  burden_sensitivity = 0.60
  sanction_strength = 0.55

  social_benefit = 0.90 * complied
  compliance_cost = admin_burden * burden_sensitivity
  enforcement_cost = 0.20 * sanction_strength
  administrative_cost = 0.10 + 0.25 * admin_burden

  welfare = compliance_utility + social_benefit - compliance_cost - enforcement_cost - administrative_cost

  print *, "Synthetic regulatory policy welfare:", welfare
end program regulatory_welfare
