fn debt_repayment_gain(debt_interest_rate: f64, savings_rate: f64, repayment_amount: f64) -> f64 {
    (debt_interest_rate - savings_rate) * repayment_amount
}

fn repay_debt_from_labeled_savings(
    debt_interest_rate: f64,
    savings_rate: f64,
    repayment_amount: f64,
    label_penalty: f64,
) -> bool {
    debt_repayment_gain(debt_interest_rate, savings_rate, repayment_amount) > label_penalty
}

fn main() {
    println!(
        "Repay debt from labeled savings: {}",
        repay_debt_from_labeled_savings(0.22, 0.02, 1000.0, 150.0)
    );
}
