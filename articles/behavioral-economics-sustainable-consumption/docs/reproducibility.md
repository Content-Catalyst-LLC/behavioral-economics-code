# Reproducibility Notes

## Recommended workflow

1. Generate synthetic data with Python or R.
2. Store processed outputs in `data/processed`.
3. Run scenario analysis in Python, R, Julia, or Stata.
4. Store model outputs in `outputs/models`.
5. Store tables in `outputs/tables`.
6. Store figures in `outputs/figures`.
7. Document assumptions in `docs`.

## Reproducibility requirements for real research

- Version controlled code.
- Locked package environments.
- Raw data provenance.
- Reproducible build scripts.
- Data cleaning logs.
- Sensitivity analysis.
- Identification diagnostics.
- Clear treatment definitions.
- Transparent exclusion rules.
