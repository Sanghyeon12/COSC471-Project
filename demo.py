#!/usr/bin/env python3
"""
Simple demonstration of DBMS functionality
"""

import os
import shutil
from dbms import DBMS, Parser

def demo():
    # Clean up any previous test data
    if os.path.exists("./demo_data"):
        shutil.rmtree("./demo_data")
    
    # Create DBMS with demo data directory
    dbms = DBMS(data_dir="./demo_data")
    parser = Parser(dbms)
    
    print("="*70)
    print("DATABASE MANAGEMENT SYSTEM - DEMONSTRATION")
    print("="*70)
    print()
    
    commands = [
        ("Creating Database", "CREATE DATABASE University;"),
        ("Using Database", "USE University;"),
        ("Creating Student Table", """CREATE TABLE Student (
            id Integer PRIMARY KEY,
            name Text,
            gpa Float
        );"""),
        ("Creating Course Table", """CREATE TABLE Course (
            code Text PRIMARY KEY,
            title Text,
            credits Integer
        );"""),
        ("Describing All Tables", "DESCRIBE ALL;"),
        ("Inserting Students", None, [
            "INSERT Student VALUES (123, \"John Doe\", 3.5);",
            "INSERT Student VALUES (456, \"Jane Smith\", 3.8);",
            "INSERT Student VALUES (789, \"Bob Johnson\", 3.2);",
            "INSERT Student VALUES (234, \"Alice Williams\", 3.9);",
            "INSERT Student VALUES (567, \"John Brown\", 3.6);"
        ]),
        ("Inserting Courses", None, [
            "INSERT Course VALUES (\"CS101\", \"Intro to CS\", 3);",
            "INSERT Course VALUES (\"CS201\", \"Data Structures\", 4);",
            "INSERT Course VALUES (\"MATH101\", \"Calculus\", 4);"
        ]),
        ("Select All Students", "SELECT * FROM Student;"),
        ("Select Students with GPA > 3.5", "SELECT * FROM Student WHERE gpa > 3.5;"),
        ("Count All Students", "SELECT count(*) FROM Student;"),
        ("Maximum GPA", "SELECT max(gpa) FROM Student;"),
        ("Average GPA", "SELECT average(gpa) FROM Student;"),
        ("Update Student GPA", "UPDATE Student SET gpa = 4.0 WHERE id = 123;"),
        ("View Updated Student", "SELECT * FROM Student WHERE id = 123;"),
        ("Create High Performers Table", """LET HighPerformers KEY id 
            SELECT id, name, gpa FROM Student WHERE gpa >= 3.6;"""),
        ("View High Performers", "SELECT * FROM HighPerformers;"),
        ("Rename Course Attributes", "RENAME Course (course_code, course_name, credit_hours);"),
        ("View Renamed Table", "DESCRIBE Course;"),
        ("Delete Low Performing Student", "DELETE Student WHERE gpa < 3.3;"),
        ("Final Student List", "SELECT * FROM Student;"),
    ]
    
    for item in commands:
        if len(item) == 2:
            title, command = item
            print(f"\n{'─'*70}")
            print(f"📌 {title}")
            print(f"{'─'*70}")
            print(f"Command: {command}")
            print()
            parser.parse(command)
        else:
            title, _, command_list = item
            print(f"\n{'─'*70}")
            print(f"📌 {title}")
            print(f"{'─'*70}")
            for cmd in command_list:
                print(f"Command: {cmd}")
                parser.parse(cmd)
            print()
    
    print("\n" + "="*70)
    print("✅ DEMONSTRATION COMPLETED SUCCESSFULLY")
    print("="*70)
    print()
    print("Data stored in: ./demo_data/")
    print("Try running: python3 dbms.py")
    print("Then type: INPUT test_commands.sql;")
    print()

if __name__ == "__main__":
    demo()
