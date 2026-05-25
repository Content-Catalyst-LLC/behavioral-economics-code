program compliance_model
  implicit none

  real :: trust, salience, norm_sensitivity, burden_sensitivity
  real :: present_bias, admin_burden, reminder_salience
  real :: trust_signal, penalty_strength, utility, probability

  trust = 0.60
  salience = 0.55
  norm_sensitivity = 0.45
  burden_sensitivity = 0.60
  present_bias = 0.35
  admin_burden = 0.12
  reminder_salience = 0.80
  trust_signal = 0.80
  penalty_strength = 0.30

  utility = 0.8 * reminder_salience * salience &
          + 0.7 * norm_sensitivity &
          + 1.0 * trust_signal * trust &
          + 0.9 * penalty_strength &
          - 1.2 * admin_burden * burden_sensitivity &
          - 0.7 * present_bias * admin_burden

  probability = 1.0 / (1.0 + exp(-(utility - 0.5)))

  print *, "Synthetic compliance probability:", probability
end program compliance_model
