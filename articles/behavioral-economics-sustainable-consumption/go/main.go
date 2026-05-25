package main

import (
	"fmt"
	"math"
)

type Agent struct {
	Income               float64
	EnvironmentalConcern float64
	PresentBias          float64
	LossAversion         float64
	NormSensitivity      float64
	FrictionSensitivity  float64
	QualityUncertainty  float64
	InfrastructureAccess float64
}

func AdoptionProbability(a Agent, subsidy float64, defaultGreen float64, normSignal float64, friction float64) float64 {
	effectivePremium := math.Max(0.10-subsidy, 0.0)
	affordability := 1.0 / math.Log(a.Income)
	immediateCost := effectivePremium*affordability*100.0 + friction*a.FrictionSensitivity

	utilityDiff := -0.65 +
		1.10*a.EnvironmentalConcern +
		0.72*defaultGreen +
		0.85*a.NormSensitivity*normSignal +
		0.55*a.InfrastructureAccess -
		1.75*immediateCost -
		0.38*a.PresentBias -
		0.35*a.LossAversion*effectivePremium -
		0.62*a.QualityUncertainty

	return 1.0 / (1.0 + math.Exp(-utilityDiff))
}

func main() {
	agent := Agent{
		Income:               65000,
		EnvironmentalConcern: 0.62,
		PresentBias:          0.28,
		LossAversion:         2.0,
		NormSensitivity:      0.55,
		FrictionSensitivity:  0.50,
		QualityUncertainty:  0.25,
		InfrastructureAccess: 0.60,
	}

	fmt.Printf("%.6f\n", AdoptionProbability(agent, 0.05, 1.0, 0.70, 0.08))
}
