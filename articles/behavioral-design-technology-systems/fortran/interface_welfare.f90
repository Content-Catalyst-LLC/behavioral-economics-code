program interface_welfare
  implicit none

  real :: baseline_value, reward_intensity, friction_asymmetry
  real :: autonomy_preference, privacy_cost, cognitive_overload
  real :: welfare, autonomy_cost

  baseline_value = 0.45
  reward_intensity = 0.35
  friction_asymmetry = 0.0
  autonomy_preference = 0.58
  privacy_cost = 0.05
  cognitive_overload = 0.42

  autonomy_cost = max(friction_asymmetry, 0.0) * autonomy_preference * 0.7

  welfare = baseline_value + 0.35 * reward_intensity - autonomy_cost - privacy_cost - 0.45 * cognitive_overload

  print *, "Synthetic user welfare:", welfare
end program interface_welfare
