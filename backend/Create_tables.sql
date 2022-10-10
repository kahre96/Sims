
/* 	Created by:	Peter Stegeby
	Date:		22-09-14
	Modified:	22-10-10
*/
-- Create tables

CREATE TABLE Employee (
Emp_ID					INTEGER(3) NOT NULL AUTO_INCREMENT,
Firstname				VARCHAR(20),
Lastname				VARCHAR(20),
Birthdate				DATE,
Added_date				DATE DEFAULT CURDATE(),
PRIMARY KEY (Emp_ID));

CREATE TABLE Ranking (
Ranking_ID				INTEGER(2) NOT NULL AUTO_INCREMENT,
Name					VARCHAR(40),
PRIMARY KEY(Ranking_ID));

CREATE TABLE Player (
Emp_ID					INTEGER(3) NOT NULL,
Ranking_ID				INTEGER(2) NOT NULL DEFAULT 1,
Level					INTEGER(2) DEFAULT 1,
Xp_Total				INTEGER(5) DEFAULT 0,
Xp_Month				INTEGER(3) DEFAULT 0,
Last_login				DATE DEFAULT CURDATE(),
Consecutive_days		INTEGER(1) DEFAULT 0,
PRIMARY KEY (Emp_ID),
FOREIGN KEY (Emp_ID) REFERENCES Employee(Emp_ID),
FOREIGN KEY (Ranking_ID) REFERENCES Ranking(Ranking_ID));

CREATE TABLE Hero (
Emp_ID					INTEGER(3) NOT NULL,
Date					DATE,
Xp_Month				INTEGER(3),
PRIMARY KEY (Emp_ID),
FOREIGN KEY (Emp_ID) REFERENCES Employee(Emp_ID));

CREATE TABLE Char_emp (
Char_ID					INTEGER(3) NOT NULL,
Emp_ID					INTEGER(3) NOT NULL,
PRIMARY KEY (Char_ID),
FOREIGN KEY (Emp_ID) REFERENCES Employee(Emp_ID));

CREATE TABLE Greeting (
Greetings_ID			INTEGER(4) NOT NULL,
Text					VARCHAR(300),
PRIMARY KEY (Greetings_ID));
