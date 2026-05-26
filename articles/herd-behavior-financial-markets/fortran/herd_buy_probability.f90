program herd_buy_probability
  implicit none
  real :: fundamental, private_signal, herd_signal, perceived_risk
  real :: alpha, beta, gamma, utility, probability

  fundamental = 0.15
  private_signal = 0.20
  herd_signal = 0.70
  perceived_risk = 0.10
  alpha = 1.0
  beta = 1.4
  gamma = 0.8

  utility = fundamental + alpha * private_signal + beta * herd_signal - gamma * perceived_risk
  probability = 1.0 / (1.0 + exp(-utility))

  print *, "Synthetic herd buy probability:", probability
end program herd_buy_probability
