program organizational_decision_model
  implicit none

  real :: expected_payoff, risk, sunk_cost, prestige_value
  real :: complexity, overconfidence, review_strength
  real :: short_term_pressure, long_horizon_value, long_horizon_weight
  real :: value, probability

  expected_payoff = 0.14
  risk = 0.22
  sunk_cost = 0.31
  prestige_value = 0.20
  complexity = 0.35
  overconfidence = 0.18
  short_term_pressure = 0.70
  review_strength = 0.85
  long_horizon_value = 0.26
  long_horizon_weight = 0.60

  value = expected_payoff &
        + prestige_value * short_term_pressure &
        - risk &
        - complexity &
        + 0.9 * sunk_cost &
        + 0.7 * overconfidence &
        - 0.8 * review_strength * sunk_cost &
        - 0.5 * review_strength * overconfidence &
        + long_horizon_weight * long_horizon_value

  probability = 1.0 / (1.0 + exp(-value))

  print *, "Synthetic approval probability:", probability
end program organizational_decision_model
