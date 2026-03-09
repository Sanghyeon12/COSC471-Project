# Database Management System (DBMS) Project

A complete implementation of a database management system in Python with Binary Search Tree indexing.

## Features

This DBMS implements all required commands:

1. **CREATE DATABASE** - Create a new database
2. **USE** - Select a database to work with
3. **CREATE TABLE** - Create tables with typed columns and optional primary keys
4. **DESCRIBE** - Show table schemas (single table or ALL)
5. **INSERT** - Insert records with constraint checking
6. **SELECT** - Query records with WHERE conditions
7. **SELECT with Aggregates** - COUNT(*), MIN, MAX, AVERAGE (graduate requirement)
8. **UPDATE** - Update records matching WHERE conditions
9. **DELETE** - Delete records or entire tables
10. **RENAME** - Rename table attributes
11. **LET** - Create new tables from SELECT queries with BST indexing
12. **INPUT** - Execute commands from file (with optional OUTPUT)
13. **EXIT** - Save and exit

## Key Implementation Details

### Binary Search Tree Indexing
- All tables with PRIMARY KEY use BST for indexing
- Primary key searches use the BST index directly
- Non-key searches traverse the BST in-order for consistent results
- Automatic index rebuilding on updates/deletes

### Data Storage
- Each table has its own `.tbl` file with JSON header and records
- Each indexed table has a `.idx` file containing the pickled BST
- Metadata stored in `metadata.json`
- All data persists between sessions

### Case Insensitivity
- Commands are case-insensitive (USE = use = Use)
- String comparisons are case-insensitive
- Numeric comparisons support type coercion (1 = 1.0)

### Grammar Features
- Recursive descent parser
- Multi-line command support (commands end with semicolon)
- Whitespace-flexible parsing
- Quoted string support for text values

## Usage

### Interactive Mode

```bash
python3 dbms.py
```

Then enter commands:

```sql
CREATE DATABASE MyDB;
USE MyDB;
CREATE TABLE Student (id Integer PRIMARY KEY, name Text, gpa Float);
INSERT Student VALUES (123, "John Doe", 3.5);
SELECT * FROM Student;
EXIT;
```

### Batch Mode (INPUT command)

```sql
INPUT test_commands.sql;
INPUT test_commands.sql OUTPUT results.txt;
```

## Command Examples

### Creating and Using Databases

```sql
CREATE DATABASE University;
USE University;
```

### Creating Tables

```sql
-- Table with primary key
CREATE TABLE Student (
    id Integer PRIMARY KEY,
    name Text,
    gpa Float
);

-- Table without primary key
CREATE TABLE Course (
    code Text,
    title Text,
    credits Integer
);
```

### Inserting Data

```sql
INSERT Student VALUES (123, "John Doe", 3.5);
INSERT Student VALUES (456, "Jane Smith", 3.8);
```

### Querying Data

```sql
-- Select all
SELECT * FROM Student;

-- Select specific columns
SELECT name, gpa FROM Student;

-- With WHERE clause
SELECT * FROM Student WHERE gpa > 3.5;
SELECT name FROM Student WHERE id = 123;

-- Complex conditions
SELECT * FROM Student WHERE gpa >= 3.5 AND gpa <= 3.8;
SELECT * FROM Student WHERE name = "John Doe" OR name = "Jane Smith";
```

### Aggregate Functions (Graduate Requirement)

```sql
SELECT count(*) FROM Student;
SELECT max(gpa) FROM Student;
SELECT min(gpa) FROM Student;
SELECT average(gpa) FROM Student;
SELECT average(gpa) FROM Student WHERE name = "John Doe";
```

### Updating Data

```sql
UPDATE Student SET gpa = 4.0 WHERE id = 123;
UPDATE Student SET name = "John Smith", gpa = 3.6 WHERE id = 123;
```

### Deleting Data

```sql
-- Delete specific records
DELETE Student WHERE gpa < 2.0;

-- Delete all records and remove table schema
DELETE Student;
```

### Renaming Attributes

```sql
RENAME Student (student_id, student_name, grade_point_average);
```

### Creating Tables from Queries (LET)

```sql
-- Create new table with BST index on specified key
LET HighPerformers KEY id 
SELECT id, name, gpa FROM Student WHERE gpa >= 3.5;
```

### Describing Tables

```sql
-- Describe specific table
DESCRIBE Student;

-- Describe all tables in current database
DESCRIBE ALL;
```

## Data Types

- **Integer**: 32-bit integer values
- **Float**: Floating-point numbers (e.g., 3.14, 100.5)
- **Text**: String values up to 100 characters (use quotes: "text")

## File Structure

```
dbms_data/
├── metadata.json              # Database metadata
└── university/                # Database directory
    ├── student.tbl           # Table data file
    ├── student.idx           # BST index file (if primary key exists)
    ├── course.tbl
    └── course.idx
```

## Testing

Run the comprehensive test:

```bash
python3 dbms.py
```

Then in the DBMS prompt:

```sql
INPUT test_commands.sql;
```

Or run with output:

```sql
INPUT test_commands.sql OUTPUT results.txt;
```

## Requirements Met

✅ Recursive descent parsing  
✅ Each table in separate file with header  
✅ Binary Search Tree indexing for primary keys  
✅ All primary key searches use BST  
✅ In-order traversal for non-key searches on indexed tables  
✅ Persistent storage (data saved on exit, loaded on start)  
✅ All 11 commands implemented  
✅ Aggregate functions (COUNT, MIN, MAX, AVERAGE) for graduate credit  
✅ Case-insensitive grammar and comparisons  
✅ Multi-line command support  
✅ INPUT/OUTPUT file processing  

## Implementation Notes

### BST Index Usage
- **With Primary Key**: 
  - All searches use BST (either direct lookup or in-order traversal)
  - Ensures consistent ordering across all operations
  - Primary key searches: O(log n) average case
  - Non-key searches: O(n) with in-order traversal

- **Without Primary Key**:
  - Sequential scan of table file
  - No ordering guarantees

### Constraint Checking
- **Domain Constraints**: Type checking on INSERT/UPDATE
- **Key Constraints**: Duplicate primary key prevention
- **Entity Integrity**: Primary key cannot be null
- **Referential Integrity**: Not implemented (as per requirements)

## Error Handling

The system handles:
- Invalid commands
- Missing databases/tables
- Type mismatches
- Duplicate primary keys
- Missing files
- Syntax errors

## Performance Considerations

- Primary key searches: O(log n) with BST
- Non-key searches: O(n) with in-order traversal
- Index rebuilding after DELETE/UPDATE on primary key
- Memory-efficient: Records loaded on-demand

## Future Enhancements (Not Required)

- Multi-table joins
- Referential integrity constraints
- Transaction support
- Query optimization
- B+ tree indexing for better disk performance

## Author Notes

This implementation follows all project requirements:
- Uses Python 3 (available in COSC lab)
- Recursive descent parser
- Separate files for tables and indexes
- BST for primary key indexing
- All 10 base commands + aggregates
- Persistent storage
- Case-insensitive operations
- Multi-line command support

The code is well-structured, documented, and ready for testing with the provided test file.
