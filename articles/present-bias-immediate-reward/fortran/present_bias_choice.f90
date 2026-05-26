program present_bias_choice
  implicit none
  real :: beta, delta, delayed_reward, immediate_reward, commitment_cost
  real :: delayed_value, immediate_value
  integer :: delay, choice

  beta = 0.72
  delta = 0.97
  delayed_reward = 300.0
  delay = 12
  immediate_reward = 160.0
  commitment_cost = 70.0

  delayed_value = beta * (delta ** delay) * delayed_reward
  immediate_value = immediate_reward - commitment_cost

  if (delayed_value >= immediate_value) then
    choice = 1
  else
    choice = 0
  end if

  print *, "Synthetic delayed choice under present bias:", choice
end program present_bias_choice
