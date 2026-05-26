program framing_choice
  implicit none
  real :: lambda, eta, certain, risky, frame_shift
  integer :: choice

  lambda = 2.0
  eta = 0.88
  frame_shift = -10.0

  certain = 200.0 ** eta
  risky = (1.0 / 3.0) * (600.0 ** eta) + (2.0 / 3.0) * 0.0

  if (risky + frame_shift >= certain) then
    choice = 1
  else
    choice = 0
  end if

  print *, "Synthetic risky choice under gain frame:", choice
end program framing_choice
