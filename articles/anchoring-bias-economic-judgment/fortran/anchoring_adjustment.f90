program anchoring_adjustment
  implicit none
  real :: anchor, true_value, adjustment_rate, estimate, bias

  anchor = 85.0
  true_value = 65.0
  adjustment_rate = 0.55

  estimate = anchor + adjustment_rate * (true_value - anchor)
  bias = estimate - true_value

  print *, "Anchored estimate:", estimate
  print *, "Anchoring bias:", bias
end program anchoring_adjustment
