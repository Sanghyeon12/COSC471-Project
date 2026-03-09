-- Test file for Database Management System
-- This file demonstrates all required commands

-- 1. CREATE DATABASE and USE
CREATE DATABASE University;
USE University;

-- 2. CREATE TABLE with primary key
CREATE TABLE Student (
    id Integer PRIMARY KEY,
    name Text,
    gpa Float
);

CREATE TABLE Course (
    code Text PRIMARY KEY,
    title Text,
    credits Integer
);

CREATE TABLE Employee (
    ssn Integer PRIMARY KEY,
    name Text,
    salary Float
);

-- 3. DESCRIBE command
DESCRIBE ALL;

-- 4. INSERT records
INSERT Student VALUES (123, "John Doe", 3.5);
INSERT Student VALUES (456, "Jane Smith", 3.8);
INSERT Student VALUES (789, "Bob Johnson", 3.2);
INSERT Student VALUES (234, "Alice Williams", 3.9);
INSERT Student VALUES (567, "John Brown", 3.6);

INSERT Course VALUES ("CS101", "Intro to CS", 3);
INSERT Course VALUES ("CS201", "Data Structures", 4);
INSERT Course VALUES ("MATH101", "Calculus", 4);

INSERT Employee VALUES (111223333, "Alice Manager", 85000.50);
INSERT Employee VALUES (222334444, "Bob Developer", 75000.00);
INSERT Employee VALUES (333445555, "Carol Engineer", 80000.25);

-- 5. SELECT commands
SELECT * FROM Student;

SELECT name, gpa FROM Student;

SELECT * FROM Student WHERE gpa > 3.5;

SELECT name FROM Student WHERE id = 123;

SELECT * FROM Student WHERE name = "John Doe";

SELECT * FROM Course WHERE credits >= 4;

-- 6. SELECT with aggregates (for graduate students)
SELECT count(*) FROM Student;

SELECT max(gpa) FROM Student;

SELECT min(gpa) FROM Student;

SELECT average(gpa) FROM Student;

SELECT average(gpa) FROM Student WHERE name = "John Doe";

SELECT max(salary) FROM Employee;

SELECT min(salary) FROM Employee;

SELECT average(salary) FROM Employee;

-- 7. UPDATE command
UPDATE Student SET gpa = 4.0 WHERE id = 123;

SELECT * FROM Student WHERE id = 123;

UPDATE Employee SET salary = 90000.00 WHERE ssn = 111223333;

SELECT * FROM Employee;

-- 8. DELETE with WHERE
DELETE Student WHERE id = 789;

SELECT * FROM Student;

-- 9. RENAME command
RENAME Course (course_code, course_name, credit_hours);

DESCRIBE Course;

SELECT * FROM Course;

-- 10. LET command (create new table from SELECT)
LET HighPerformers KEY id SELECT id, name, gpa FROM Student WHERE gpa >= 3.6;

DESCRIBE HighPerformers;

SELECT * FROM HighPerformers;

-- 11. More complex queries
SELECT * FROM Student WHERE gpa >= 3.5 AND gpa <= 3.8;

SELECT name, gpa FROM Student WHERE gpa > 3.0 OR gpa < 2.0;

-- 12. Test case insensitivity
select * from student where name = "JOHN DOE";

SELECT NAME, GPA FROM STUDENT WHERE ID = 456;

-- 13. Clean up - DELETE without WHERE removes table
CREATE TABLE TempTable (
    id Integer PRIMARY KEY,
    value Text
);

INSERT TempTable VALUES (1, "test");

SELECT * FROM TempTable;

DELETE TempTable;

DESCRIBE ALL;
