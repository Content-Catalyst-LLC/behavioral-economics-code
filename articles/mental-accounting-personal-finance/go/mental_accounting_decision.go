package main

import "fmt"

func debtRepaymentGain(debtInterestRate, savingsRate, repaymentAmount float64) float64 {
	return (debtInterestRate - savingsRate) * repaymentAmount
}

func repayDebtFromLabeledSavings(debtInterestRate, savingsRate, repaymentAmount, labelPenalty float64) bool {
	gain := debtRepaymentGain(debtInterestRate, savingsRate, repaymentAmount)
	return gain > labelPenalty
}

func main() {
	fmt.Printf("Repay debt from labeled savings: %v\n", repayDebtFromLabeledSavings(0.22, 0.02, 1000.0, 150.0))
}
