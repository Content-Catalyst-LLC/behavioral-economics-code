program mental_accounting_decision
  implicit none
  real :: debt_interest_rate, savings_rate, repayment_amount, label_penalty, gain
  integer :: decision

  debt_interest_rate = 0.22
  savings_rate = 0.02
  repayment_amount = 1000.0
  label_penalty = 150.0

  gain = (debt_interest_rate - savings_rate) * repayment_amount

  if (gain > label_penalty) then
    decision = 1
  else
    decision = 0
  end if

  print *, "Repay debt from labeled savings:", decision
end program mental_accounting_decision
