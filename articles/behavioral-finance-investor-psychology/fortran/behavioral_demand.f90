program behavioral_demand
  implicit none
  real :: expected_return, perceived_variance, behavioral_term
  real :: alpha, beta, gamma, demand
  real :: gross_return, turnover, cost_per_turnover, net_return

  expected_return = 0.08
  perceived_variance = 0.03
  behavioral_term = 0.40
  alpha = 1.2
  beta = 0.7
  gamma = 0.5

  demand = alpha * expected_return - beta * perceived_variance + gamma * behavioral_term

  gross_return = 0.05
  turnover = 1.4
  cost_per_turnover = 0.0025
  net_return = gross_return - cost_per_turnover * turnover

  print *, "Synthetic behavioral demand:", demand
  print *, "Synthetic net return after turnover:", net_return
end program behavioral_demand
