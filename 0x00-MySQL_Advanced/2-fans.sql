-- import the metal_bands.sql dump 
-- Create a temporary table with the fan count for each band
-- Rank the bands based on the number of fans
SELECT origin, SUM(fans) AS nb_fans
    FROM metal_bands
    GROUP BY origin
    ORDER BY nb_fans DESC;
