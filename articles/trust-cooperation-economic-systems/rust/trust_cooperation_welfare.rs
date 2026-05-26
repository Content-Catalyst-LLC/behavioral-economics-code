fn main() {
    let welfare = 0.70 + (0.30 * 0.80 + 0.25 * 0.75 + 0.20) - 0.05 - (0.05 * 0.80);
    println!("Synthetic trust and cooperation welfare: {:.3}", welfare);
}
