SELECT MAX(timestamp) FROM roster;

-- Review all data sorted by character and time
SELECT
	ts.name AS Server,
	v.name AS Village,
	c.name AS Character,
	tr.name AS Rank,
	r.custom_rank_name,
	r.level,
	r.timestamp
FROM roster r
INNER JOIN villages v ON r.village_id = v.id
INNER JOIN characters c ON r.character_id = c.id
INNER JOIN types tr ON r.rank_id = tr.id
INNER JOIN types ts ON v.server_id = ts.id
ORDER BY c.name, r.timestamp;

-- Min and max level in timeframe
SELECT
	ts.name AS Server,
	v.name AS Village,
	c.name AS Character,
	MIN(r.level),
	MAX(r.level)
FROM roster r
INNER JOIN villages v ON r.village_id = v.id
INNER JOIN characters c ON r.character_id = c.id
INNER JOIN types tr ON r.rank_id = tr.id
INNER JOIN types ts ON v.server_id = ts.id
GROUP BY ts.name, v.name, c.name;

-- Who is in the village as of the latest date?
SELECT *
FROM roster
WHERE village_id = 1
AND timestamp > (SELECT MAX(timestamp) FROM roster WHERE village_id = 1);

SELECT MAX(timestamp)
FROM roster
GROUP BY village_id, character_id;

SELECT village_id, character_id
FROM roster;

SELECT
	ts.name AS Server,
	v.name AS Village,
	c.name AS Character
FROM roster r
INNER JOIN villages v ON r.village_id = v.id
INNER JOIN characters c ON r.character_id = c.id
INNER JOIN types ts ON v.server_id = ts.id
ORDER BY c.name, r.timestamp;

-- Current Roster per Village
WITH most_recent AS (
	SELECT
		village_id,
		MAX(timestamp) AS timestamp,
		datetime(MAX(timestamp), '-7.5 minutes') AS range_start,
		datetime(MAX(timestamp), '+7.5 minutes') AS range_end
	FROM roster
	GROUP BY village_id
)
SELECT
	ts.name AS server,
	v.name AS village,
	c.id AS character_id,
	c.name AS character,
	r.level,
	tr.name AS rank,
	r.custom_rank_name
FROM roster r
INNER JOIN most_recent mr ON r.village_id = mr.village_id
INNER JOIN villages v ON r.village_id = v.id
INNER JOIN characters c ON r.character_id = c.id
INNER JOIN types ts ON v.server_id = ts.id
INNER JOIN types tr ON r.rank_id = tr.id
WHERE r.timestamp BETWEEN mr.range_start AND mr.range_end
ORDER BY
	ts.name, -- server
	v.name; -- village