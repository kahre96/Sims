
/* 	Created by:	Peter Stegeby
	Date:		22-09-14
	Modified:	22-10-14
*/
-- Create tables

CREATE TABLE Employee (
Emp_ID					INTEGER(4) NOT NULL AUTO_INCREMENT,
Firstname				VARCHAR(20),
Lastname				VARCHAR(20),
Birthdate				DATE,
Added_date				DATE DEFAULT CURDATE(),
PRIMARY KEY (Emp_ID));

CREATE TABLE Player (
Emp_ID					INTEGER(4) NOT NULL,
Level					INTEGER(2) DEFAULT 1,
Xp_Total				INTEGER(5) DEFAULT 0,
Xp_Month				INTEGER(3) DEFAULT 0,
Last_login				DATE DEFAULT CURDATE(),
Consecutive_days		INTEGER(1) DEFAULT 0,
PRIMARY KEY (Emp_ID),
FOREIGN KEY (Emp_ID) REFERENCES Employee(Emp_ID));

CREATE TABLE Hero (
Emp_ID					INTEGER(4) NOT NULL,
Date					DATE,
Xp_Month				INTEGER(3),
PRIMARY KEY (Emp_ID,Date),
FOREIGN KEY (Emp_ID) REFERENCES Employee(Emp_ID));

CREATE TABLE Greeting (
Greetings_ID			INTEGER(4) NOT NULL AUTO_INCREMENT,
Text					VARCHAR(300),
Category				VARCHAR(10),
PRIMARY KEY (Greetings_ID));
