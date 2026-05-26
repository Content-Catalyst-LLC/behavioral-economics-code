program prospect_value_example
  implicit none
  real :: lambda_loss, alpha_gain, beta_loss, gamma_weight, mixed_value

  lambda_loss = 2.0
  alpha_gain = 0.88
  beta_loss = 0.88
  gamma_weight = 0.70

  mixed_value = probability_weight(0.5, gamma_weight) * prospect_value(240.0, lambda_loss, alpha_gain, beta_loss) + &
                probability_weight(0.5, gamma_weight) * prospect_value(-100.0, lambda_loss, alpha_gain, beta_loss)

  print *, "Mixed gamble prospect value:", mixed_value
  if (mixed_value > 0.0) then
    print *, "Accept mixed gamble: yes"
  else
    print *, "Accept mixed gamble: no"
  end if

contains

  real function prospect_value(x, lambda_loss, alpha_gain, beta_loss)
    implicit none
    real, intent(in) :: x, lambda_loss, alpha_gain, beta_loss

    if (x >= 0.0) then
      prospect_value = x ** alpha_gain
    else
      prospect_value = -lambda_loss * ((-x) ** beta_loss)
    end if
  end function prospect_value

  real function probability_weight(p, gamma)
    implicit none
    real, intent(in) :: p, gamma
    probability_weight = (p ** gamma) / (((p ** gamma) + ((1.0 - p) ** gamma)) ** (1.0 / gamma))
  end function probability_weight

end program prospect_value_example
