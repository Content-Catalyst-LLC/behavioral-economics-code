program trust_cooperation_welfare
  implicit none
  real :: welfare
  welfare = 0.70 + (0.30 * 0.80 + 0.25 * 0.75 + 0.20) - 0.05 - (0.05 * 0.80)
  print *, "Synthetic trust and cooperation welfare:", welfare
end program trust_cooperation_welfare
