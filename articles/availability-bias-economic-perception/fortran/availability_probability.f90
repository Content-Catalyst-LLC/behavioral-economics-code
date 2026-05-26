program availability_probability
  implicit none
  real :: true_probability, availability_sensitivity, availability_score, base_rate_correction
  real :: subjective_probability

  true_probability = 0.12
  availability_sensitivity = 0.70
  availability_score = 0.85
  base_rate_correction = 0.04

  subjective_probability = true_probability + availability_sensitivity * availability_score * 0.25 - base_rate_correction

  if (subjective_probability < 0.0) subjective_probability = 0.0
  if (subjective_probability > 1.0) subjective_probability = 1.0

  print *, "Synthetic subjective probability under availability bias:", subjective_probability
end program availability_probability
