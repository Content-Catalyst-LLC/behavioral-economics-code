program heuristic_error
  implicit none
  real :: true_value, raw_error, estimate, correction_capacity

  true_value = 0.35
  correction_capacity = 0.55

  raw_error = 0.30 * 0.10 + 0.25 * (-0.05) + 0.40 * 0.12 + 0.20 * (-0.08)
  estimate = true_value + raw_error * (1.0 - correction_capacity)

  if (estimate < 0.0) estimate = 0.0
  if (estimate > 1.0) estimate = 1.0

  print *, "Synthetic heuristic estimate:", estimate
  print *, "Synthetic judgment error:", estimate - true_value
end program heuristic_error
