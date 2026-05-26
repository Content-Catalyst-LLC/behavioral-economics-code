program interface_model
  implicit none

  real :: baseline_value, salience_sensitivity, default_sensitivity
  real :: friction_sensitivity, reward_sensitivity, cognitive_overload
  real :: salience, default_on, entry_friction, reward_intensity
  real :: score, probability

  baseline_value = 0.45
  salience_sensitivity = 0.55
  default_sensitivity = 0.50
  friction_sensitivity = 0.60
  reward_sensitivity = 0.58
  cognitive_overload = 0.42
  salience = 0.55
  default_on = 0.0
  entry_friction = 0.08
  reward_intensity = 0.35

  score = baseline_value &
        + salience_sensitivity * salience &
        + default_sensitivity * default_on &
        - friction_sensitivity * entry_friction &
        + reward_sensitivity * reward_intensity &
        - cognitive_overload * 0.4

  probability = 1.0 / (1.0 + exp(-score))

  print *, "Synthetic join probability:", probability
end program interface_model
