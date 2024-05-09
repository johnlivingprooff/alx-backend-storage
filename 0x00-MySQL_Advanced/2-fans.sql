-- ranks country origins of bands,
-- ordered by the number of (non-unique) fans

SELECT origin, COUNT(*) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;

-- Rank the country origins based on the number of fans
SELECT 
    origin,
    nb_fans,
    RANK() OVER (ORDER BY nb_fans DESC) AS country_rank
FROM (
    SELECT origin, COUNT(*) AS nb_fans
    FROM metal_bands
    GROUP BY origin
) AS fan_counts;
