program intertemporal_discounting
  implicit none
  integer :: k
  real :: beta, delta, utility, payoff

  beta = 0.70
  delta = 0.95
  utility = 0.0

  do k = 1, 10
     payoff = 10.0
     utility = utility + beta * (delta ** k) * payoff
  end do

  print *, "Present-biased discounted utility:", utility
end program intertemporal_discounting
