
/* 	Created by:	Peter Stegeby
	Date:		22-09-14
	Modified:	22-10-06
*/
-- Create tables

CREATE TABLE Employee (
Emp_ID					INTEGER(3) NOT NULL,
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
Player_ID				INTEGER(3) NOT NULL AUTO_INCREMENT,
Emp_ID					INTEGER(3) NOT NULL,
Ranking_ID				INTEGER(2) NOT NULL DEFAULT 1,
Level					INTEGER(2) DEFAULT 1,
Xp_Total				INTEGER(5) DEFAULT 0,
Xp_Month				INTEGER(2) DEFAULT 0,
Last_login				DATE DEFAULT CURDATE(),
Consecutive_days		INTEGER(1) DEFAULT 0,
PRIMARY KEY (Player_ID),
FOREIGN KEY (Emp_ID) REFERENCES Employee(Emp_ID),
FOREIGN KEY (Ranking_ID) REFERENCES Ranking(Ranking_ID));

CREATE TABLE Data (
ID						SMALLINT NOT NULL AUTO_INCREMENT,
Month					VARCHAR(15),
PRIMARY KEY(ID));

CREATE TABLE Player_in_Data (
Player_ID				INTEGER(3) NOT NULL,
Data_ID					SMALLINT NOT NULL,
Xp_month				INTEGER(4),
PRIMARY KEY(Player_ID, Data_ID),
FOREIGN KEY(Player_ID) REFERENCES Player(Player_ID),
FOREIGN KEY(Data_ID) REFERENCES Data(ID));

CREATE TABLE Greeting (
Greetings_ID			INTEGER(4) NOT NULL,
Text					VARCHAR(300),
PRIMARY KEY (Greetings_ID));
