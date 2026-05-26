program status_quo_choice
  implicit none
  real :: value_status_quo, value_alternative, premium, switch_cost, loss_aversion, perceived_loss
  real :: utility_sq, utility_alt
  integer :: adoption

  value_status_quo = 0.50
  value_alternative = 0.68
  premium = 0.08
  switch_cost = 0.05
  loss_aversion = 1.50
  perceived_loss = 0.04

  utility_sq = value_status_quo + premium
  utility_alt = value_alternative - switch_cost - loss_aversion * perceived_loss

  if (utility_alt >= utility_sq) then
    adoption = 1
  else
    adoption = 0
  end if

  print *, "Synthetic alternative adoption under status quo bias:", adoption
end program status_quo_choice
