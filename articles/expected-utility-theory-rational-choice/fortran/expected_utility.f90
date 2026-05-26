program expected_utility
  implicit none
  real :: wealth, rho, eu_certain, eu_risky

  wealth = 50000.0
  rho = 1.5

  eu_certain = crra_utility(wealth + 100.0, rho)
  eu_risky = 0.5 * crra_utility(wealth + 40.0, rho) + 0.5 * crra_utility(wealth + 220.0, rho)

  print *, "EU certain:", eu_certain
  print *, "EU risky:", eu_risky
  if (eu_risky > eu_certain) then
    print *, "Choose risky: yes"
  else
    print *, "Choose risky: no"
  end if

contains

  real function crra_utility(x, r)
    implicit none
    real, intent(in) :: x, r

    if (abs(r - 1.0) < 1.0e-8) then
      crra_utility = log(x)
    else
      crra_utility = (x ** (1.0 - r)) / (1.0 - r)
    end if
  end function crra_utility

end program expected_utility
