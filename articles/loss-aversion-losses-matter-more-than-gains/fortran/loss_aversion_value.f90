program loss_aversion_value
  implicit none
  real :: lambda_loss, alpha_gain, beta_loss, mixed_value

  lambda_loss = 2.0
  alpha_gain = 0.88
  beta_loss = 0.88

  mixed_value = 0.5 * prospect_value(240.0, lambda_loss, alpha_gain, beta_loss) + &
                0.5 * prospect_value(-100.0, lambda_loss, alpha_gain, beta_loss)

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

end program loss_aversion_value
