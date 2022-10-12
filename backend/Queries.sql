SELECT * FROM employee;

SELECT * FROM player;

SELECT * FROM ranking GROUP BY ranking_id;

SELECT CONCAT(e.firstname," ",e.lastname) AS Display_name, p.emp_ID, r.Name AS Ranking, p.xp_Total AS "Total XP", p.Level
FROM employee AS e, player AS p, ranking AS r
WHERE e.emp_ID = p.emp_ID AND p.ranking_id = r.ranking_id;

SELECT p.emp_id, CONCAT(e.firstname," ",e.lastname) "Display name", r.name "Rank", p.xp_total, xp_month FROM employee e, player p, ranking r
WHERE e.emp_id=1 AND (p.emp_id = e.emp_id) AND (p.ranking_id = r.ranking_id);


SELECT emp_id, firstname, lastname FROM employee ORDER BY emp_id DESC LIMIT 5;

