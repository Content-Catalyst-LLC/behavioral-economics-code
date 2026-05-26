program time_discounting_choice
  implicit none
  real :: future_value, discount_rate, present_val
  real :: beta, delta, delayed_reward, immediate_reward, support
  real :: delayed_value, immediate_value
  integer :: periods, delay, choice

  future_value = 1000.0
  discount_rate = 0.03
  periods = 10
  present_val = future_value / ((1.0 + discount_rate) ** periods)

  beta = 0.75
  delta = 0.97
  delayed_reward = 300.0
  delay = 12
  immediate_reward = 160.0
  support = 40.0

  delayed_value = beta * (delta ** delay) * delayed_reward
  immediate_value = immediate_reward - support

  if (delayed_value >= immediate_value) then
    choice = 1
  else
    choice = 0
  end if

  print *, "Present value:", present_val
  print *, "Synthetic delayed choice under discounting:", choice
end program time_discounting_choice
