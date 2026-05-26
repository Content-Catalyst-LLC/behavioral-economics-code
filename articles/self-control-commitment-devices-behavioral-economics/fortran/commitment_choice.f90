program commitment_choice
  implicit none
  real :: beta, delta, future_benefit, immediate_temptation, commitment_cost
  real :: patient_value, temptation_value
  integer :: periods, patient_choice

  beta = 0.72
  delta = 0.97
  future_benefit = 1000.0
  immediate_temptation = 600.0
  commitment_cost = 300.0
  periods = 12

  patient_value = beta * (delta ** periods) * future_benefit
  temptation_value = immediate_temptation - commitment_cost

  if (patient_value >= temptation_value) then
    patient_choice = 1
  else
    patient_choice = 0
  end if

  print *, "Synthetic patient choice under commitment:", patient_choice
end program commitment_choice
