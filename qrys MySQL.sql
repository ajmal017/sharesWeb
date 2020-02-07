SET SQL_SAFE_UPDATES = 0;

-- Actualizar las carteras de fondos trimestrales con los valores minimo, maximo y media de cada accion
UPDATE ShareFond AS sf
INNER JOIN (
    SELECT per.id AS idPeriod, sh.id AS idShare, sh.name AS shareName, 
        MIN(IFNULL(hist.low, hist.close)) AS minPrice, MAX(IFNULL(hist.high, hist.close)) AS maxPrice, 
        AVG(hist.close) AS avgPrice, 
        MIN(hist.volume) AS minVolume, MAX(hist.volume) AS maxVolume, AVG(hist.volume) AS avgVolume, 
        COUNT(*) AS count
    FROM (
        SELECT id, fromDate, toDate
        FROM SHARE.Period
        ORDER BY fromDate DESC
        LIMIT 1
    ) per, SHARE.ShareHistory hist
    INNER JOIN SHARE.Share sh ON sh.id = hist.idShare
    WHERE hist.date BETWEEN per.fromDate AND per.toDate
        AND sh.update = 1
    GROUP BY per.id, sh.id, sh.name
) qry ON qry.idShare = sf.idShare AND sf.idPeriod = qry.idPeriod
SET sf.minPrice = qry.minPrice,
    sf.maxPrice = qry.maxPrice,
    sf.avgPrice = qry.avgPrice,
    sf.minVolume = qry.minVolume,
    sf.maxVolume = qry.maxVolume,
    sf.avgVolume = qry.avgVolume,
    sf.count = qry.count;


-- Ordenar las acciones con menor crecimiento sobre el valor minimo del trimestre anterior 
SELECT s.name, s.lastValue, sf.minPrice, sf.maxPrice, sf.avgPrice, round((s.lastValue / sf.minPrice -1) * 100 , 2) as PorcentSobreMin
FROM ShareFond sf
INNER JOIN Share s ON s.id = sf.idShare
INNER JOIN
    (
        SELECT id
        FROM SHARE.Period
        ORDER BY fromDate DESC
        LIMIT 1
    ) per  ON sf.idPeriod = per.id
ORDER BY PorcentSobreMin;




SELECT YEAR(`date`),MIN(priceBuyCurrent) AS min,MAX(priceBuyCurrent) AS max,AVG(priceBuyCurrent) AS avg
FROM SHARE.Summary
WHERE `date` >'2015-08-19'
GROUP BY YEAR(`date`);



-- Calcular los dividendos en un periodo:
SELECT `date`, A.`name`, importGross as bruto, importNet as Neto , importGross/currencyValue as BrutoEur, importNet/currencyValue as NetoEur, currencyValue
FROM Dividend D
INNER JOIN `Transaction` TR ON D.idTransaction = TR.Id
INNER JOIN `Share` A ON A.id = TR.idShare
WHERE `date` >='2018/01/01' and `date` <'2019/01/01'
ORDER BY `date`;

