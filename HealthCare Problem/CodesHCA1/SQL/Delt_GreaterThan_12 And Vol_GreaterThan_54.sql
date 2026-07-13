SELECT c13 AS Daily_Vol,  COUNT(*) as Quant 
FROM ambulance_response_data_CLEAN
WHERE c7  > 12 AND c13 > 54
GROUP BY c8
ORDER BY c13 Desc