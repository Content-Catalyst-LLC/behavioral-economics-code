-- Adoption and welfare by policy regime.
SELECT
    pr.regime_name,
    AVG(ao.adopted) AS adoption_rate,
    AVG(ao.private_welfare) AS mean_private_welfare,
    AVG(ao.external_benefit) AS mean_external_benefit,
    AVG(ao.fiscal_cost) AS mean_fiscal_cost,
    AVG(ao.total_welfare) AS mean_total_welfare
FROM adoption_outcome ao
JOIN policy_regime pr
    ON ao.policy_regime_id = pr.policy_regime_id
GROUP BY pr.regime_name
ORDER BY mean_total_welfare DESC;

-- Distributional incidence by income quintile.
SELECT
    pr.regime_name,
    h.income_quintile,
    AVG(ao.adopted) AS adoption_rate,
    AVG(ao.total_welfare) AS mean_total_welfare,
    AVG(ao.fiscal_cost) AS mean_fiscal_cost
FROM adoption_outcome ao
JOIN policy_regime pr
    ON ao.policy_regime_id = pr.policy_regime_id
JOIN household h
    ON ao.household_id = h.household_id
GROUP BY pr.regime_name, h.income_quintile
ORDER BY pr.regime_name, h.income_quintile;
