
/* 	Created by:	Peter Stegeby
	Date:		22-09-14
	Modified:	22-10-04
*/
-- Create tables

CREATE TABLE Employee (
emp_ID					INTEGER(3) NOT NULL,
firstname					VARCHAR(20),
lastname					VARCHAR(20),
birthdate				DATE,
added_date				DATE DEFAULT CURDATE(),
PRIMARY KEY (emp_ID));

CREATE TABLE Player (
player_ID				INTEGER(3) NOT NULL AUTO_INCREMENT,
emp_ID					INTEGER(3) NOT NULL,
xp_Total				Integer(5) DEFAULT 0,
xp_Month				Integer(2) DEFAULT 0,
level					Integer(2) DEFAULT 1,
last_login				DATE DEFAULT CURDATE(),
consecutive_days		Integer(1) DEFAULT 0,
PRIMARY KEY (player_ID),
FOREIGN KEY (emp_ID) REFERENCES Employee(emp_ID));

CREATE TABLE Ranking (
ranking_ID				INTEGER(2) NOT NULL AUTO_INCREMENT,
name					VARCHAR(40),
xp_required				INTEGER(4) DEFAULT NULL,
PRIMARY KEY(ranking_ID));

CREATE TABLE Player_in_Ranking(
player_ID				INTEGER(3) NOT NULL,
ranking_ID				INTEGER(2) NOT NULL,
PRIMARY KEY (player_ID, ranking_ID),
FOREIGN KEY (player_ID) REFERENCES Player (player_ID),
FOREIGN KEY (ranking_ID) REFERENCES Ranking (ranking_ID));

CREATE TABLE Query (
string					VARCHAR(300) NOT NULL,
times_used				INTEGER(3) DEFAULT 1,
PRIMARY KEY (string));


