UPDATE Player_meets_requirement pmr
INNER JOIN Player p
ON pmr.player_id = p.player_id
SET 
value = 1337
WHERE p.player_id = 6;