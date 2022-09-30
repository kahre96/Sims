
/* 	Created by:	Peter Stegeby
	Date:		22-09-14
	Modified:	22-09-26
*/
-- Create tables

CREATE TABLE Employee (
Emp_ID					INTEGER(3) NOT NULL,
Fname					VARCHAR(20),
Lname					VARCHAR(20),
Birthdate				DATE,
added_date				DATE DEFAULT CURDATE(),
PRIMARY KEY (Emp_ID));

CREATE TABLE Ranking (
Tier					INTEGER(2) NOT NULL AUTO_INCREMENT,
Name					VARCHAR(20) UNIQUE,
PRIMARY KEY (Tier));

CREATE TABLE Player (
Player_ID				INTEGER(3) NOT NULL AUTO_INCREMENT,
Emp_ID					INTEGER(3) NOT NULL,
Ranking_tier			INTEGER(2) NOT NULL DEFAULT 1,
xp_Total				Integer(5) DEFAULT 0,
xp_Month				Integer(2) DEFAULT 0,
Level					Integer(2) DEFAULT 1,
PRIMARY KEY (Player_ID),
FOREIGN KEY (Emp_ID) REFERENCES Employee(Emp_ID),
FOREIGN KEY (Ranking_tier) REFERENCES Ranking(Tier));

CREATE TABLE Query (
String					VARCHAR(300) NOT NULL,
Times_used				INTEGER(3) DEFAULT 1,
PRIMARY KEY (String));

CREATE TABLE Requirement (
ID						INTEGER(2) NOT NULL AUTO_INCREMENT,
Name					VARCHAR(40),
Value					INTEGER(4) DEFAULT NULL,
PRIMARY KEY(ID));

CREATE TABLE Player_meets_Requirement(
Player_ID				INTEGER(3) NOT NULL,
Requirement_ID			INTEGER(2) NOT NULL,
Value					INTEGER(4),
PRIMARY KEY (Player_ID, Requirement_ID),
FOREIGN KEY (Player_ID) REFERENCES Player (Player_ID),
FOREIGN KEY (Requirement_ID) REFERENCES Requirement (ID));

CREATE TABLE xp_actions (
ID						INTEGER(2) NOT NULL AUTO_INCREMENT,
Name					VARCHAR(30),
Value					INTEGER(3),
PRIMARY KEY (ID));

CREATE TABLE Day (
Date					DATE NOT NULL,
PRIMARY KEY (Date));

