
UPDATE ShareFond AS sf
INNER JOIN (
    SELECT per.id AS idPeriod, sh.id AS idShare, sh.name AS shareName, 
        MIN(IFNULL(hist.low, hist.close)) AS minPrice, MAX(IFNULL(hist.high, hist.close)) AS maxPrice, 
        AVG(hist.close) AS avgPrice, 
        MIN(hist.volume) AS minVolume, MAX(hist.volume) AS maxVolume, AVG(hist.volume) AS avgVolume, 
        COUNT(*) AS count
    FROM SHARE.Period per, SHARE.ShareHistory hist
    INNER JOIN SHARE.Share sh ON sh.id = hist.idShare
    WHERE per.fromDate BETWEEN '2017-01-01' AND '2017-03-31' 
        AND hist.date BETWEEN per.fromDate AND per.toDate
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
