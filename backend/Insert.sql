/* 	Created by:	Peter Stegeby
	Date:		22-09-14
	Modified:	22-09-26
*/

-- Fills the database with dummy information
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (1, "peter", "stegeby", STR_TO_DATE('19930805', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (2, "andreas", "norin", STR_TO_DATE('19951218', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (3, "glenn", "verhaag", STR_TO_DATE('19980906', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (4, "nordin", "suleimani", STR_TO_DATE('19830328', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (5, "fredrik", "kåhre", STR_TO_DATE('19961014', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (6, "ina", "nilsson", STR_TO_DATE('19990116', '%Y%m%d'));

INSERT INTO Ranking(ranking_ID, name, xp_required) VALUES (1, "Android", 0);
INSERT INTO Ranking(ranking_ID, name, xp_required) VALUES (2, "Ewok",100);
INSERT INTO Ranking(ranking_ID, name, xp_required) VALUES (3, "Wookie", 200);
INSERT INTO Ranking(ranking_ID, name, xp_required) VALUES (4, "Padawan",300);
INSERT INTO Ranking(ranking_ID, name, xp_required) VALUES (5, "Jedi Knight",400);

INSERT INTO Player(emp_ID, xp_total, xp_month, level, last_login, consecutive_days) VALUES (6,260, 40, 6, STR_TO_DATE('20221001', '%Y%m%d'), 2);
INSERT INTO Player(emp_ID, xp_total, xp_month, level, consecutive_days) VALUES (5,80, 10, 2, 3);
INSERT INTO Player(emp_ID, xp_total, xp_month, level, consecutive_days) VALUES (4,500, 100, 2, 5);
INSERT INTO Player(emp_ID, xp_total, xp_month, level) VALUES (3,145, 15, 3);
INSERT INTO Player(emp_ID, xp_total, xp_month, level) VALUES (2,45, 30, 1);
INSERT INTO Player(emp_ID, xp_total, xp_month, level) VALUES (1,115, 20, 3);

INSERT INTO Player_in_Ranking(player_ID, ranking_ID) VALUES (1,1);
INSERT INTO Player_in_Ranking(player_ID, ranking_ID) VALUES (2,1);
INSERT INTO Player_in_Ranking(player_ID, ranking_ID) VALUES (3,1);
INSERT INTO Player_in_Ranking(player_ID, ranking_ID) VALUES (4,1);
INSERT INTO Player_in_Ranking(player_ID, ranking_ID) VALUES (5,1);
INSERT INTO Player_in_Ranking(player_ID, ranking_ID) VALUES (6,1);

INSERT INTO Query VALUES ("SELECT * FROM employee AS e, player AS p WHERE e.emp_ID = p.emp_ID GROUP BY xp_total DESC;", 2);
INSERT INTO Query VALUES ("SELECT * FROM employee;", 5);
INSERT INTO Query VALUES ("SELECT * FROM employee WHERE lastname=s%;", 12);


