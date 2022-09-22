-- Fyller i alla Employees
INSERT INTO Employee VALUES (1, "peter", "stegeby");
INSERT INTO Employee VALUES (2, "andreas", "norin");
INSERT INTO Employee VALUES (3, "glenn", "verhaag");
INSERT INTO Employee VALUES (4, "nordin", "suleimani");
INSERT INTO Employee VALUES (5, "fredrik", "kåhre");
INSERT INTO Employee VALUES (6, "ina", "nilsson");

INSERT INTO Player VALUES (1, 6, 260);
INSERT INTO Player VALUES (2, 5, 80);
INSERT INTO Player VALUES (3, 4, 500);
INSERT INTO Player VALUES (4, 3, 145);
INSERT INTO Player VALUES (5, 2, 45);
INSERT INTO Player VALUES (6, 1, 115);


INSERT INTO Query VALUES ("SELECT * FROM employee AS e, player AS p WHERE e.empID = p.empID GROUP BY experience DESC;", 2);
INSERT INTO Query VALUES ("SELECT * FROM employee;", 5);
INSERT INTO Query VALUES ("SELECT * FROM employee WHERE lname=s%;", 12);