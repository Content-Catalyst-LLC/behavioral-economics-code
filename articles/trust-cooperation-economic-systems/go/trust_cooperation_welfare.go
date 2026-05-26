package main
import "fmt"
func main() {
	welfare := 0.70 + (0.30*0.80 + 0.25*0.75 + 0.20) - 0.05 - (0.05 * 0.80)
	fmt.Printf("Synthetic trust and cooperation welfare: %.3f\n", welfare)
}
