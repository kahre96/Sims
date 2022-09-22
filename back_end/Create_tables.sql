
/* 	Skapad av:	Peter Stegeby
	Datum:		22-09-14
	Modifierad:	22-09-14
*/
-- Skapa tabellerna

CREATE TABLE Employee (
EmpID					INTEGER(3) NOT NULL,
Fname					VARCHAR(20),
Lname					VARCHAR(20),
PRIMARY KEY (EmpID));

CREATE TABLE Player (
PlayerID				INTEGER(3) NOT NULL,
EmpID					INTEGER(3) NOT NULL,
Experience				Integer(5),
PRIMARY KEY (PlayerID),
FOREIGN KEY (EmpID) REFERENCES Employee(EmpID));

CREATE TABLE Query (
String					VARCHAR(300) NOT NULL,
Times_used				INTEGER(3) DEFAULT 1,
PRIMARY KEY (String));





