program choice_architecture_welfare
  implicit none

  real :: long_run_value, complexity_sensitivity, complexity
  real :: switching_sensitivity, switching_cost, digital_literacy
  real :: welfare

  long_run_value = 0.42
  complexity_sensitivity = 0.60
  complexity = 0.08
  switching_sensitivity = 0.52
  switching_cost = 0.04
  digital_literacy = 0.62

  welfare = long_run_value &
          - complexity_sensitivity * complexity &
          - switching_sensitivity * switching_cost &
          + 0.03 * digital_literacy

  print *, "Synthetic choice architecture welfare:", welfare
end program choice_architecture_welfare
