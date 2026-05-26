# Data Dictionary

## synthetic_platform_panel.csv

| Column | Type | Description |
|---|---:|---|
| user_id | integer | Synthetic user identifier |
| period | integer | Time period |
| post | integer | Post-treatment period indicator |
| regime | text | Platform design regime |
| engagement_optimized | integer | Engagement-optimized ranking indicator |
| socially_amplified | integer | Socially amplified ranking indicator |
| cognitive_overload | numeric | Cognitive burden |
| privacy_sensitivity | numeric | Sensitivity to data extraction and privacy cost |
| digital_literacy | numeric | Simulated platform literacy |
| baseline_user_value | numeric | Baseline expected value from platform use |
| recommendation_intensity | numeric | Recommendation strength |
| salience | numeric | Ranking or visual prominence |
| social_proof | numeric | Popularity/review/social signal strength |
| friction | numeric | Effort cost |
| data_extraction_intensity | numeric | Intensity of data extraction |
| clicked | integer | Simulated click/selection outcome |
| retained | integer | Simulated retention outcome |
| consented | integer | Simulated data-sharing consent outcome |
| exposure_quality | numeric | Synthetic quality of exposure |
| user_welfare | numeric | Synthetic user welfare |
| platform_value | numeric | Synthetic platform value |
| welfare_platform_gap | numeric | Platform value minus user welfare |

## synthetic_platform_experiment.csv

One row per synthetic user after treatment assignment. Useful for cross-sectional treatment-effect estimation.
