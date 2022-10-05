
/* 	Created by:	Peter Stegeby
	Date:		22-09-14
	Modified:	22-10-04
*/
-- Create tables

CREATE TABLE Employee (
Emp_ID					INTEGER(3) NOT NULL,
Firstname				VARCHAR(20),
Lastname				VARCHAR(20),
Birthdate				DATE,
Added_date				DATE DEFAULT CURDATE(),
PRIMARY KEY (emp_ID));

CREATE TABLE Player (
Player_ID				INTEGER(3) NOT NULL AUTO_INCREMENT,
Emp_ID					INTEGER(3) NOT NULL,
Xp_Total				Integer(5) DEFAULT 0,
Xp_Month				Integer(2) DEFAULT 0,
Level					Integer(2) DEFAULT 1,
Last_login				DATE DEFAULT CURDATE(),
Consecutive_days		Integer(1) DEFAULT 0,
PRIMARY KEY (player_ID),
FOREIGN KEY (emp_ID) REFERENCES Employee(emp_ID));

CREATE TABLE Ranking (
Ranking_ID				INTEGER(2) NOT NULL AUTO_INCREMENT,
Name					VARCHAR(40),
PRIMARY KEY(ranking_ID));


CREATE TABLE Query (
String					VARCHAR(300) NOT NULL,
Times_used				INTEGER(3) DEFAULT 1,
PRIMARY KEY (string));


