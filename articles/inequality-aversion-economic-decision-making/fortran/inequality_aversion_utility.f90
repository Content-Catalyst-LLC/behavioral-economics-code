program inequality_aversion_utility
  implicit none
  real :: self_payoff, other_payoff, alpha, beta, utility

  self_payoff = 0.30
  other_payoff = 0.70
  alpha = 1.5
  beta = 0.6

  utility = self_payoff - alpha * max(other_payoff - self_payoff, 0.0) - beta * max(self_payoff - other_payoff, 0.0)

  print *, "Fehr-Schmidt utility:", utility
end program inequality_aversion_utility
