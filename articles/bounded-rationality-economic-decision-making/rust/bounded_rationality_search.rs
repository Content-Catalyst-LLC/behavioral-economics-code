fn main() {
    let values = vec![0.20, 0.35, 0.62, 0.75, 0.91, 0.55];
    let aspiration = 0.70;
    let search_cost = 0.02;

    let optimal = values.iter().cloned().fold(f64::NEG_INFINITY, f64::max);

    let mut chosen_index = values.len();
    let mut chosen_value = *values.last().unwrap();

    for (i, value) in values.iter().enumerate() {
        if *value >= aspiration {
            chosen_index = i + 1;
            chosen_value = *value;
            break;
        }
    }

    let net_value = chosen_value - search_cost * chosen_index as f64;

    println!("Chosen index: {}", chosen_index);
    println!("Chosen value: {:.3}", chosen_value);
    println!("Optimal value: {:.3}", optimal);
    println!("Net value: {:.3}", net_value);
    println!("Optimization gap: {:.3}", optimal - chosen_value);
}
