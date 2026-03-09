# DBMS Quick Start Guide

## Installation & Running

### Run Interactive Mode
```bash
python3 dbms.py
```

### Run Demo
```bash
python3 demo.py
```

### Run Test Suite
```bash
python3 test_runner.py
```

### Execute SQL File
```bash
python3 dbms.py
# Then in the prompt:
dbms> INPUT test_commands.sql;
```

## Quick Command Reference

### Database Operations
```sql
CREATE DATABASE MyDB;
USE MyDB;
```

### Table Operations
```sql
-- Create table with primary key
CREATE TABLE Student (id Integer PRIMARY KEY, name Text, gpa Float);

-- Create table without primary key
CREATE TABLE Log (timestamp Integer, message Text);

-- Describe tables
DESCRIBE Student;
DESCRIBE ALL;

-- Rename attributes
RENAME Student (student_id, student_name, grade_point_average);
```

### Data Operations
```sql
-- Insert
INSERT Student VALUES (123, "John Doe", 3.5);

-- Select
SELECT * FROM Student;
SELECT name, gpa FROM Student WHERE gpa > 3.5;

-- Update
UPDATE Student SET gpa = 4.0 WHERE id = 123;

-- Delete specific records
DELETE Student WHERE gpa < 2.0;

-- Delete all records and table
DELETE Student;
```

### Aggregate Functions (Graduate Credit)
```sql
SELECT count(*) FROM Student;
SELECT max(gpa) FROM Student;
SELECT min(gpa) FROM Student;
SELECT average(gpa) FROM Student;
SELECT average(gpa) FROM Student WHERE name = "John";
```

### Advanced Operations
```sql
-- Create new table from query
LET HighPerformers KEY id 
    SELECT id, name, gpa FROM Student WHERE gpa >= 3.5;

-- File I/O
INPUT commands.sql;
INPUT commands.sql OUTPUT results.txt;

-- Exit
EXIT;
```

## Key Features

✅ **Binary Search Tree Indexing**
- Automatic BST creation for primary key tables
- O(log n) primary key lookups
- In-order traversal for consistent non-key searches

✅ **Persistent Storage**
- All data saved automatically on exit
- Separate files for tables and indexes
- JSON format for easy inspection

✅ **Constraint Checking**
- Domain constraints (type checking)
- Primary key uniqueness
- Entity integrity (no null primary keys)

✅ **Case Insensitive**
- Commands: CREATE = create = Create
- Comparisons: "John" = "JOHN" = "john"
- Type coercion: 1 = 1.0

## File Structure

```
dbms_data/
├── metadata.json           # Database registry
└── university/             # Database directory
    ├── student.tbl        # Table data (JSON header + records)
    ├── student.idx        # BST index (pickled)
    ├── course.tbl
    └── course.idx
```

## Example Session

```sql
-- Start the DBMS
$ python3 dbms.py

-- Create and use database
dbms> CREATE DATABASE School;
dbms> USE School;

-- Create table
dbms> CREATE TABLE Student (
...>     id Integer PRIMARY KEY,
...>     name Text,
...>     gpa Float
...> );

-- Insert data
dbms> INSERT Student VALUES (1, "Alice", 3.8);
dbms> INSERT Student VALUES (2, "Bob", 3.5);

-- Query data
dbms> SELECT * FROM Student WHERE gpa > 3.6;

-- Use aggregates
dbms> SELECT average(gpa) FROM Student;

-- Exit (saves automatically)
dbms> EXIT;
```

## Troubleshooting

**Problem**: "No database selected"
**Solution**: Run `USE DatabaseName;` first

**Problem**: "Duplicate primary key"
**Solution**: Primary keys must be unique

**Problem**: "Table does not exist"
**Solution**: Check table name spelling (case doesn't matter)

**Problem**: Data not persisting
**Solution**: Use EXIT; to properly save data

## Testing Your Implementation

1. **Run the demo**: `python3 demo.py`
2. **Run test suite**: `python3 test_runner.py`
3. **Test with SQL file**: 
   ```bash
   python3 dbms.py
   dbms> INPUT test_commands.sql;
   ```
4. **Manual testing**: Use interactive mode

## Grading Checklist

- [x] CREATE DATABASE & USE
- [x] CREATE TABLE with primary key
- [x] DESCRIBE (single & ALL)
- [x] INSERT with constraint checking
- [x] SELECT with WHERE conditions
- [x] Aggregate functions (COUNT, MIN, MAX, AVERAGE)
- [x] UPDATE with WHERE
- [x] DELETE with WHERE & table deletion
- [x] RENAME attributes
- [x] LET (create table from query)
- [x] INPUT with optional OUTPUT
- [x] EXIT with persistence
- [x] BST indexing on primary keys
- [x] In-order traversal for non-key searches
- [x] Case-insensitive operations
- [x] Multi-line command support
- [x] Recursive descent parsing

## Tips for Success

1. **Test thoroughly**: Use the provided test files
2. **Check BST**: Verify in-order traversal gives consistent results
3. **Verify persistence**: Exit and restart to ensure data is saved
4. **Test edge cases**: Empty tables, duplicate keys, missing tables
5. **Test aggregates**: All four functions (graduate requirement)

## Common Patterns

### Pattern 1: Data Analysis Pipeline
```sql
CREATE DATABASE Analytics;
USE Analytics;
CREATE TABLE Sales (id Integer PRIMARY KEY, amount Float, region Text);
-- Insert data...
SELECT average(amount) FROM Sales WHERE region = "North";
LET HighSales KEY id SELECT * FROM Sales WHERE amount > 1000;
```

### Pattern 2: Data Transformation
```sql
-- Create base table
CREATE TABLE Raw (id Integer PRIMARY KEY, data Text);
-- Insert data...
-- Create processed view
LET Processed KEY id SELECT id, data FROM Raw WHERE data != "";
```

### Pattern 3: Batch Processing
```sql
INPUT load_data.sql OUTPUT data_loaded.txt;
INPUT analyze.sql OUTPUT results.txt;
```

## Support

For questions about the project:
1. Review the README.md
2. Check this Quick Start Guide
3. Examine the test files
4. Run demo.py to see expected behavior
