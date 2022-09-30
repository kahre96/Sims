SELECT * FROM employee;

SELECT * FROM player;

SELECT * FROM ranking GROUP BY tier;

SELECT * FROM player_meets_requirement;

SELECT * FROM requirement;

SELECT * FROM day;

SELECT CONCAT(e.fname," ",e.lname) AS Display_name, p.Player_ID, r.Name AS Ranking, p.xp_Total AS "Total XP", p.Level
FROM employee AS e, player AS p, ranking AS r
WHERE e.emp_ID = p.emp_ID AND p.ranking_tier = r.tier;

SELECT CONCAT(e.fname," ",e.lname) AS Display_name, p.Player_ID, r.Name AS Ranking, p.xp_Total AS "Total XP", p.Level, ((req.value * (SELECT value FROM requirement AS req WHERE req.name = r.name)) * p.level) AS Next_Level, ((req.value * (SELECT value FROM requirement AS req WHERE req.name = r.name)) * p.level) - p.xp_total AS xp_Needed
FROM employee AS e, player AS p, ranking AS r, player_meets_requirement AS pmr, requirement AS req
WHERE (req.id = pmr.requirement_id AND p.player_id = pmr.player_id) AND (e.emp_id = p.emp_id AND p.ranking_tier = r.tier);

