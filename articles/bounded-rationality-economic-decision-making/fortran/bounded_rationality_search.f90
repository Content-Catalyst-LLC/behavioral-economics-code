program bounded_rationality_search
  implicit none
  real, dimension(6) :: values
  real :: aspiration, search_cost, optimal, chosen_value, net_value
  integer :: i, chosen_index

  values = (/0.20, 0.35, 0.62, 0.75, 0.91, 0.55/)
  aspiration = 0.70
  search_cost = 0.02

  optimal = maxval(values)
  chosen_index = size(values)
  chosen_value = values(size(values))

  do i = 1, size(values)
    if (values(i) >= aspiration) then
      chosen_index = i
      chosen_value = values(i)
      exit
    end if
  end do

  net_value = chosen_value - search_cost * chosen_index

  print *, "Chosen index:", chosen_index
  print *, "Chosen value:", chosen_value
  print *, "Optimal value:", optimal
  print *, "Net value:", net_value
  print *, "Optimization gap:", optimal - chosen_value

end program bounded_rationality_search
