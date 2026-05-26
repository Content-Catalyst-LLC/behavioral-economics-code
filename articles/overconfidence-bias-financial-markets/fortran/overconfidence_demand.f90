program overconfidence_demand
  implicit none
  real :: expected_return, perceived_variance, alpha, beta
  real :: demand, gross_return, trading_intensity, cost_per_turnover, net_return

  expected_return = 0.08
  perceived_variance = 0.03
  alpha = 1.2
  beta = 0.7
  demand = alpha * expected_return - beta * perceived_variance

  gross_return = 0.05
  trading_intensity = 1.4
  cost_per_turnover = 0.0025
  net_return = gross_return - cost_per_turnover * trading_intensity

  print *, "Synthetic investor demand:", demand
  print *, "Synthetic net return after cost:", net_return
end program overconfidence_demand
