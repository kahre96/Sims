/* 	Created by:	Peter Stegeby
	Date:		22-09-14
	Modified:	22-10-25
*/

-- Fills the database with dummy information
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (1, "andreas", "norin", STR_TO_DATE('19951218', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (2, "fredrik", "kåhre", STR_TO_DATE('19961014', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (3, "glenn", "verhaag", STR_TO_DATE('19980906', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (4, "ina", "nilsson", STR_TO_DATE('19990116', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (5, "nordin", "suleimani", STR_TO_DATE('19830328', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (6, "peter", "stegeby", STR_TO_DATE('19930805', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (9, "Jonas", "Sandström", STR_TO_DATE('19960727', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (10, "Dennis", "Löfqvist", STR_TO_DATE('19911203', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (11, "Wictor", "Svensson", STR_TO_DATE('19950711', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (12, "Björn", "Lindström", STR_TO_DATE('19701004', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (13, "Test", "User1", STR_TO_DATE('19701025', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (14, "Test", "User2", STR_TO_DATE('19701004', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (15, "Test", "User3", STR_TO_DATE('19701026', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (16, "Test", "User4", STR_TO_DATE('19701027', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (17, "Test", "User5", STR_TO_DATE('19701004', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (18, "Test", "User6", STR_TO_DATE('19701004', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (19, "Test", "User7", STR_TO_DATE('19701004', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (20, "Test", "User8", STR_TO_DATE('19701004', '%Y%m%d'));
INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (21, "Test", "User9", STR_TO_DATE('19701004', '%Y%m%d'));

/*
INSERT INTO Ranking(ranking_ID, name) VALUES (1, "android");
INSERT INTO Ranking(ranking_ID, name) VALUES (2, "ewok");
INSERT INTO Ranking(ranking_ID, name) VALUES (3, "wookie");
INSERT INTO Ranking(ranking_ID, name) VALUES (4, "padawan");
INSERT INTO Ranking(ranking_ID, name) VALUES (5, "jedi knight");
*/

INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (1, 1, 10,0, STR_TO_DATE('20221003', '%Y%m%d'), 1);
INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (2, 1, 40,0, STR_TO_DATE('20221004', '%Y%m%d'), 2);
INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (3, 1, 50,0, STR_TO_DATE('20221004', '%Y%m%d'), 3);
INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (4, 1, 990,0, STR_TO_DATE('20221004', '%Y%m%d'), 4);
INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (5, 1, 991,0, STR_TO_DATE('20221004', '%Y%m%d'), 5);
INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (6, 1, 991,0, STR_TO_DATE('20221004', '%Y%m%d'), 5);
INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (9, 1, 991,0, STR_TO_DATE('20221004', '%Y%m%d'), 5);
INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (10, 1, 991,0, STR_TO_DATE('20221004', '%Y%m%d'), 5);
INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (11, 1, 991,0, STR_TO_DATE('20221004', '%Y%m%d'), 5);
INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (12, 1, 991,0, STR_TO_DATE('20221004', '%Y%m%d'), 5);
INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (13, 1,40,0, STR_TO_DATE('20221004', '%Y%m%d'), 1);
INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (14, 1,50,10, STR_TO_DATE('20221004', '%Y%m%d'), 2);
INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (15, 1,80,20, STR_TO_DATE('20221004', '%Y%m%d'), 3);
INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (16, 1,90,30, STR_TO_DATE('20221004', '%Y%m%d'), 4);
INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (17, 1,101,40, STR_TO_DATE('20221004', '%Y%m%d'), 5);
INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (18, 1,991,50, STR_TO_DATE('20221004', '%Y%m%d'), 1);
INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (19, 1,1600,100, STR_TO_DATE('20221004', '%Y%m%d'), 1);
INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (20, 1,6000,250, STR_TO_DATE('20221004', '%Y%m%d'), 1);
INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (21, 1,6001,500, STR_TO_DATE('20221004', '%Y%m%d'), 1);

INSERT INTO Greeting(Text,Category) VALUES ("Hej","default");
INSERT INTO Greeting(Text,Category) VALUES ("Hej Hej","default");
INSERT INTO Greeting(Text,Category) VALUES ("God dag","default");
INSERT INTO Greeting(Text,Category) VALUES ("Hur går allt","default");
INSERT INTO Greeting(Text,Category) VALUES ("Grattis på födelsedagen","birthday");
INSERT INTO Greeting(Text,Category) VALUES ("Grattis","birthday");
INSERT INTO Greeting(Text,Category) VALUES ("God morgon","morning");
INSERT INTO Greeting(Text,Category) VALUES ("Morgon","morning");
INSERT INTO Greeting(Text,Category) VALUES ("Välkommen tillbaka","second");
INSERT INTO Greeting(Text,Category) VALUES ("Trevligt att se dig igen","second");