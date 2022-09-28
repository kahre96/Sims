/* 	Created by:	Peter Stegeby
	Date:		22-09-14
	Modified:	22-09-26
*/

-- Fills the database with dummy information
INSERT INTO Employee(emp_id, fname, lname, birthdate) VALUES (1, "peter", "stegeby", STR_TO_DATE('05-Aug-1993', '%e-%M-%Y'));
INSERT INTO Employee(emp_id, fname, lname, birthdate) VALUES (2, "andreas", "norin", STR_TO_DATE('18-Dec-1995', '%e-%M-%Y'));
INSERT INTO Employee(emp_id, fname, lname, birthdate) VALUES (3, "glenn", "verhaag", STR_TO_DATE('06-Sep-1998', '%e-%M-%Y'));
INSERT INTO Employee(emp_id, fname, lname, birthdate) VALUES (4, "nordin", "suleimani", STR_TO_DATE('28-Mar-1983', '%e-%M-%Y'));
INSERT INTO Employee(emp_id, fname, lname, birthdate) VALUES (5, "fredrik", "kåhre", STR_TO_DATE('14-Oct-1996', '%e-%M-%Y'));
INSERT INTO Employee(emp_id, fname, lname, birthdate) VALUES (6, "ina", "nilsson", STR_TO_DATE('16-Jan-1999', '%e-%M-%Y'));

INSERT INTO Ranking(Tier, Name) VALUES (1, "Android");
INSERT INTO Ranking(Tier, Name) VALUES (2, "Ewok");
INSERT INTO Ranking(Tier, Name) VALUES (3, "Wookie");
INSERT INTO Ranking(Tier, Name) VALUES (4, "Padawan");
INSERT INTO Ranking(Tier, Name) VALUES (5, "Jedi Knight");

INSERT INTO Player(emp_id, ranking_tier, xp_total, xp_month, level) VALUES (6, 1, 260, 40, 6);
INSERT INTO Player(emp_id, ranking_tier, xp_total, xp_month, level) VALUES (5, 1, 80, 10, 2);
INSERT INTO Player(emp_id, ranking_tier, xp_total, xp_month, level) VALUES (4, 2, 500, 100, 2);
INSERT INTO Player(emp_id, ranking_tier, xp_total, xp_month, level) VALUES (3, 1, 145, 15, 3);
INSERT INTO Player(emp_id, ranking_tier, xp_total, xp_month, level) VALUES (2, 1, 45, 30, 1);
INSERT INTO Player(emp_id, ranking_tier, xp_total, xp_month, level) VALUES (1, 1, 115, 20, 3);

INSERT INTO Requirement(Name, Value) VALUES ("xp_Level", 50);
INSERT INTO Requirement(Name, Value) VALUES ("Birthday_today", NULL);
INSERT INTO Requirement(Name, Value) VALUES ("Consecutive_days", 3);
INSERT INTO Requirement(Name, Value) VALUES ("Android", 1);
INSERT INTO Requirement(Name, Value) VALUES ("Ewok", 10);
INSERT INTO Requirement(Name, Value) VALUES ("Wookie", 20);
INSERT INTO Requirement(Name, Value) VALUES ("Padawan", 20);
INSERT INTO Requirement(Name, Value) VALUES ("Jedi Knight", 40);

INSERT INTO Player_Meets_Requirement(player_id, requirement_id, value) VALUES (1,1,50);
INSERT INTO Player_Meets_Requirement(player_id, requirement_id, value) VALUES (2,1,50);
INSERT INTO Player_Meets_Requirement(player_id, requirement_id, value) VALUES (3,1,50);
INSERT INTO Player_Meets_Requirement(player_id, requirement_id, value) VALUES (4,1,50);
INSERT INTO Player_Meets_Requirement(player_id, requirement_id, value) VALUES (5,1,50);
INSERT INTO Player_Meets_Requirement(player_id, requirement_id, value) VALUES (6,1,50);

INSERT INTO Query VALUES ("SELECT * FROM employee AS e, player AS p WHERE e.emp_ID = p.emp_ID GROUP BY xp_total DESC;", 2);
INSERT INTO Query VALUES ("SELECT * FROM employee;", 5);
INSERT INTO Query VALUES ("SELECT * FROM employee WHERE lname=s%;", 12);


