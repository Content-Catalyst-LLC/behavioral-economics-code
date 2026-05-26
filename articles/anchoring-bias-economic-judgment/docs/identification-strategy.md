# Identification Strategy

## Research setting

The synthetic data represent anchoring environments with different anchor values, disclosure quality, counter-anchor support, adjustment capacity, numeracy, confidence, cognitive load, and domain knowledge.

Regimes include:

1. `low_anchor_low_support`
2. `neutral_anchor_with_context`
3. `high_anchor_low_support`
4. `high_anchor_with_counter_context`

## Core estimands

- Effect of a low anchor on final estimates, bias, absolute error, decision quality, and welfare proxy.
- Effect of a high anchor on final estimates, bias, absolute error, decision quality, and welfare proxy.
- Effect of counter-anchor context on reducing high-anchor bias.
- Effect of disclosure quality and domain knowledge on adjustment.
- Heterogeneous effects by effective adjustment, numeracy, domain knowledge, cognitive load, and confidence.

## Baseline specification

```text
Y_i = alpha
    + beta_1 LowAnchor_i
    + beta_2 HighAnchor_i
    + beta_3 CounterContext_i
    + X_i'gamma
    + epsilon_i
```

where `Y_i` may be final estimate, bias, absolute error, decision quality, welfare proxy, or adjustment magnitude.

## Benchmark / policy-anchor specification

```text
Y_ig = alpha
     + beta_1 AnchorValue_g
     + beta_2 DisclosureQuality_g
     + beta_3 CounterAnchorSupport_g
     + X_i'gamma
     + epsilon_ig
```

This is included for workflow demonstration. Real data would require careful attention to whether the anchor is informative, arbitrary, strategically selected, institutionally authoritative, or embedded in power asymmetries.

## Identification cautions for real data

- Anchors may carry real information, not only bias.
- Opening offers may reveal private information about reservation values.
- Reference prices may signal quality or be strategically inflated.
- Appraisals may combine expert information with historical bias.
- Salary bands may improve transparency or anchor compensation below fair value.
- Algorithmic estimates may appear objective while reflecting biased data.
- Policy baselines may embed prior political choices.
- Sustainability baselines may hide long-term ecological degradation.

Because the data here are synthetic, estimates are not empirical claims about any actual consumers, workers, investors, firms, platforms, housing markets, public agencies, climate policies, or institutions. The value of the workflow is methodological.
