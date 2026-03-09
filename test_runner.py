#!/usr/bin/env python3
"""
Test runner for DBMS - Demonstrates all functionality
"""

import os
import shutil
from dbms import DBMS, Parser

def clean_test_environment():
    """Clean up test data"""
    if os.path.exists("./dbms_data"):
        shutil.rmtree("./dbms_data")

def run_test(name, commands):
    """Run a test case"""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}\n")
    
    dbms = DBMS()
    parser = Parser(dbms)
    
    for cmd in commands:
        print(f"> {cmd}")
        try:
            parser.parse(cmd)
        except Exception as e:
            print(f"ERROR: {e}")
        print()

def main():
    print("DBMS Test Suite")
    print("="*60)
    
    # Clean environment
    clean_test_environment()
    
    # Test 1: Database Creation
    run_test("CREATE DATABASE and USE", [
        "CREATE DATABASE TestDB;",
        "USE TestDB;"
    ])
    
    # Test 2: Table Creation
    run_test("CREATE TABLE with Primary Key", [
        "USE TestDB;",
        "CREATE TABLE Student (id Integer PRIMARY KEY, name Text, gpa Float);",
        "CREATE TABLE Course (code Text PRIMARY KEY, title Text, credits Integer);",
        "CREATE TABLE Enrollment (sid Integer, ccode Text);"
    ])
    
    # Test 3: DESCRIBE
    run_test("DESCRIBE Tables", [
        "USE TestDB;",
        "DESCRIBE ALL;"
    ])
    
    # Test 4: INSERT
    run_test("INSERT Records", [
        "USE TestDB;",
        "INSERT Student VALUES (101, \"Alice\", 3.8);",
        "INSERT Student VALUES (102, \"Bob\", 3.5);",
        "INSERT Student VALUES (103, \"Charlie\", 3.9);",
        "INSERT Student VALUES (104, \"Diana\", 3.2);",
        "INSERT Student VALUES (105, \"John\", 3.6);",
        "INSERT Student VALUES (106, \"John\", 3.4);",
        "INSERT Course VALUES (\"CS101\", \"Intro to CS\", 3);",
        "INSERT Course VALUES (\"CS201\", \"Data Structures\", 4);",
        "INSERT Enrollment VALUES (101, \"CS101\");",
        "INSERT Enrollment VALUES (101, \"CS201\");"
    ])
    
    # Test 5: SELECT
    run_test("SELECT Queries", [
        "USE TestDB;",
        "SELECT * FROM Student;",
        "SELECT name, gpa FROM Student;",
        "SELECT * FROM Student WHERE gpa > 3.5;",
        "SELECT name FROM Student WHERE id = 101;",
        "SELECT * FROM Student WHERE name = \"John\";"
    ])
    
    # Test 6: Aggregates
    run_test("Aggregate Functions (Graduate Credit)", [
        "USE TestDB;",
        "SELECT count(*) FROM Student;",
        "SELECT max(gpa) FROM Student;",
        "SELECT min(gpa) FROM Student;",
        "SELECT average(gpa) FROM Student;",
        "SELECT average(gpa) FROM Student WHERE name = \"John\";"
    ])
    
    # Test 7: UPDATE
    run_test("UPDATE Records", [
        "USE TestDB;",
        "UPDATE Student SET gpa = 4.0 WHERE id = 101;",
        "SELECT * FROM Student WHERE id = 101;",
        "UPDATE Student SET gpa = 3.7 WHERE gpa < 3.5;",
        "SELECT * FROM Student;"
    ])
    
    # Test 8: DELETE
    run_test("DELETE Records", [
        "USE TestDB;",
        "DELETE Student WHERE id = 104;",
        "SELECT * FROM Student;",
        "SELECT count(*) FROM Student;"
    ])
    
    # Test 9: RENAME
    run_test("RENAME Attributes", [
        "USE TestDB;",
        "RENAME Course (course_code, course_title, course_credits);",
        "DESCRIBE Course;",
        "SELECT * FROM Course;"
    ])
    
    # Test 10: LET
    run_test("LET Command (Create Table from Query)", [
        "USE TestDB;",
        "LET HighPerformers KEY id SELECT id, name, gpa FROM Student WHERE gpa >= 3.7;",
        "DESCRIBE HighPerformers;",
        "SELECT * FROM HighPerformers;"
    ])
    
    # Test 11: Case Insensitivity
    run_test("Case Insensitivity", [
        "USE TestDB;",
        "select * from student where name = \"ALICE\";",
        "SELECT NAME FROM STUDENT WHERE ID = 102;",
        "SelEcT * FrOm StUdEnT;"
    ])
    
    # Test 12: Complex Conditions
    run_test("Complex WHERE Conditions", [
        "USE TestDB;",
        "SELECT * FROM Student WHERE gpa >= 3.6 AND gpa <= 3.9;",
        "SELECT * FROM Student WHERE name = \"Alice\" OR name = \"Bob\";"
    ])
    
    # Test 13: Non-Primary Key Search (BST In-Order)
    run_test("Non-Primary Key Search Uses BST In-Order", [
        "USE TestDB;",
        "SELECT * FROM Student WHERE name = \"John\";",
        "SELECT * FROM Student WHERE gpa > 3.0;"
    ])
    
    # Test 14: Table Without Primary Key
    run_test("Table Without Primary Key", [
        "USE TestDB;",
        "SELECT * FROM Enrollment;",
        "INSERT Enrollment VALUES (102, \"CS101\");",
        "SELECT * FROM Enrollment WHERE sid = 101;"
    ])
    
    # Test 15: DELETE Table
    run_test("DELETE Entire Table", [
        "USE TestDB;",
        "DELETE Enrollment;",
        "DESCRIBE ALL;"
    ])
    
    # Test 16: Error Handling
    run_test("Error Cases", [
        "USE NonExistent;",
        "USE TestDB;",
        "INSERT Student VALUES (101, \"Duplicate\", 3.0);",  # Duplicate PK
        "SELECT * FROM NonExistentTable;",
        "INSERT Student VALUES (999);",  # Wrong number of values
    ])
    
    # Test 17: Numeric Comparison
    run_test("Numeric Type Coercion (1 = 1.0)", [
        "USE TestDB;",
        "CREATE TABLE Numbers (id Integer PRIMARY KEY, value Float);",
        "INSERT Numbers VALUES (1, 1.0);",
        "INSERT Numbers VALUES (2, 2.5);",
        "SELECT * FROM Numbers WHERE id = 1.0;",  # Integer = Float
        "SELECT * FROM Numbers WHERE value = 1;"  # Float = Integer
    ])
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)
    
    # Show final state
    print("\nFinal Database State:")
    print("="*60)
    dbms = DBMS()
    parser = Parser(dbms)
    parser.parse("USE TestDB;")
    parser.parse("DESCRIBE ALL;")

if __name__ == "__main__":
    main()
