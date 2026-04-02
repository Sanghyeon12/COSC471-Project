#!/usr/bin/env python3
"""
Database Management System Implementation
Supports: CREATE, USE, DESCRIBE, SELECT, LET, INSERT, UPDATE, DELETE, RENAME, INPUT, EXIT
With BST indexing on primary keys
"""

import os
import json
import pickle
import re
import sys
from typing import Any, List, Dict, Tuple, Optional


# ============================================================================
# Binary Search Tree Implementation
# ============================================================================

class BSTNode:
    """Node in a Binary Search Tree"""
    def __init__(self, key, record_pointer):
        self.key = key
        self.record_pointer = record_pointer  # Position in table file
        self.left = None
        self.right = None


class BST:
    """Binary Search Tree for indexing"""
    def __init__(self):
        self.root = None
    
    def insert(self, key, record_pointer):
        """Insert a key-value pair into the BST"""
        self.root = self._insert_recursive(self.root, key, record_pointer)
    
    def _insert_recursive(self, node, key, record_pointer):
        if node is None:
            return BSTNode(key, record_pointer)
        
        # Case insensitive comparison for strings
        node_key = node.key.lower() if isinstance(node.key, str) else node.key
        insert_key = key.lower() if isinstance(key, str) else key
        
        if insert_key < node_key:
            node.left = self._insert_recursive(node.left, key, record_pointer)
        elif insert_key > node_key:
            node.right = self._insert_recursive(node.right, key, record_pointer)
        else:
            # Update existing key
            node.record_pointer = record_pointer
        
        return node
    
    def search(self, key):
        """Search for a key in the BST"""
        return self._search_recursive(self.root, key)
    
    def _search_recursive(self, node, key):
        if node is None:
            return None
        
        # Case insensitive comparison for strings
        node_key = node.key.lower() if isinstance(node.key, str) else node.key
        search_key = key.lower() if isinstance(key, str) else key
        
        if search_key == node_key:
            return node.record_pointer
        elif search_key < node_key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)
    
    def inorder_traversal(self):
        """Return list of (key, record_pointer) in sorted order"""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append((node.key, node.record_pointer))
            self._inorder_recursive(node.right, result)
    
    def delete(self, key):
        """Delete a key from the BST"""
        self.root = self._delete_recursive(self.root, key)
    
    def _delete_recursive(self, node, key):
        if node is None:
            return None
        
        # Case insensitive comparison for strings
        node_key = node.key.lower() if isinstance(node.key, str) else node.key
        delete_key = key.lower() if isinstance(key, str) else key
        
        if delete_key < node_key:
            node.left = self._delete_recursive(node.left, key)
        elif delete_key > node_key:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Node to delete found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # Node has two children
            min_node = self._find_min(node.right)
            node.key = min_node.key
            node.record_pointer = min_node.record_pointer
            node.right = self._delete_recursive(node.right, min_node.key)
        
        return node
    
    def _find_min(self, node):
        """Find minimum node in subtree"""
        current = node
        while current.left is not None:
            current = current.left
        return current


# ============================================================================
# Database Management System
# ============================================================================

class DBMS:
    """Main Database Management System class"""
    
    def __init__(self, data_dir="./dbms_data"):
        self.data_dir = data_dir
        self.current_db = None
        self.metadata_file = os.path.join(data_dir, "metadata.json")
        self.databases = {}
        self.output_file = None
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Load existing metadata
        self._load_metadata()
    
    def _load_metadata(self):
        """Load database metadata from disk"""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                self.databases = json.load(f)
    
    def _save_metadata(self):
        """Save database metadata to disk"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.databases, f, indent=2)
    
    def _get_db_dir(self, db_name):
        """Get directory path for a database"""
        return os.path.join(self.data_dir, db_name.lower())
    
    def _get_table_file(self, db_name, table_name):
        """Get file path for a table"""
        return os.path.join(self._get_db_dir(db_name), f"{table_name.lower()}.tbl")
    
    def _get_index_file(self, db_name, table_name):
        """Get file path for a table's index"""
        return os.path.join(self._get_db_dir(db_name), f"{table_name.lower()}.idx")
    
    def _load_table_schema(self, table_name):
        """Load table schema from file"""
        if not self.current_db:
            raise Exception("No database selected")
        
        table_file = self._get_table_file(self.current_db, table_name)
        if not os.path.exists(table_file):
            raise Exception(f"Table {table_name} does not exist")
        
        with open(table_file, 'r') as f:
            header = f.readline().strip()
            schema = json.loads(header)
        
        return schema
    
    def _load_index(self, table_name):
        """Load BST index from file"""
        index_file = self._get_index_file(self.current_db, table_name)
        if os.path.exists(index_file):
            with open(index_file, 'rb') as f:
                return pickle.load(f)
        return BST()
    
    def _save_index(self, table_name, bst):
        """Save BST index to file"""
        index_file = self._get_index_file(self.current_db, table_name)
        with open(index_file, 'wb') as f:
            pickle.dump(bst, f)
    
    def _write_output(self, text):
        """Write output to screen or file"""
        print(text)
        if self.output_file:
            with open(self.output_file, 'a') as f:
                f.write(text + '\n')
    
    def _compare_values(self, val1, val2, op):
        """Compare two values with the given operator"""
        # Handle case-insensitive string comparison
        if isinstance(val1, str) and isinstance(val2, str):
            val1 = val1.lower()
            val2 = val2.lower()
        
        # Handle numeric comparison (1 == 1.0)
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            val1 = float(val1)
            val2 = float(val2)
        
        if op == '=':
            return val1 == val2
        elif op == '!=':
            return val1 != val2
        elif op == '<':
            return val1 < val2
        elif op == '>':
            return val1 > val2
        elif op == '<=':
            return val1 <= val2
        elif op == '>=':
            return val1 >= val2
        return False
    
    def _evaluate_condition(self, condition, record, schema):
        """Evaluate a WHERE condition against a record"""
        if condition is None or condition.strip() == "":
            return True
        
        # Parse condition: attr op value [(and|or) attr op value]*
        tokens = self._tokenize_condition(condition)
        return self._eval_condition_tokens(tokens, record, schema)
    
    def _tokenize_condition(self, condition):
        """Tokenize a condition string"""
        # Handle quoted strings
        tokens = []
        current = ""
        in_quote = False
        
        i = 0
        while i < len(condition):
            char = condition[i]
            
            if char == '"':
                if in_quote:
                    tokens.append(f'"{current}"')
                    current = ""
                    in_quote = False
                else:
                    in_quote = True
                i += 1
            elif in_quote:
                current += char
                i += 1
            elif char in ' \t\n':
                if current:
                    tokens.append(current)
                    current = ""
                i += 1
            elif i + 1 < len(condition) and condition[i:i+2] in ['<=', '>=', '!=']:
                if current:
                    tokens.append(current)
                    current = ""
                tokens.append(condition[i:i+2])
                i += 2
            elif char in '=<>':
                if current:
                    tokens.append(current)
                    current = ""
                tokens.append(char)
                i += 1
            else:
                current += char
                i += 1
        
        if current:
            tokens.append(current)
        
        return tokens
    
    def _eval_condition_tokens(self, tokens, record, schema):
        """Evaluate tokenized condition with AND precedence over OR"""

        if not tokens:
            return True

        # -------------------------------
        # Helper: evaluate single condition (attr op value)
        # -------------------------------
        def eval_simple(expr):
            attr = expr[0].lower()
            relop = expr[1]
            value = expr[2]

            # Find attribute index
            attr_idx = None
            for idx, col in enumerate(schema['columns']):
                if col['name'].lower() == attr:
                    attr_idx = idx
                    break

            if attr_idx is None:
                raise Exception(f"Unknown attribute: {attr}")

            val1 = record[attr_idx]

            # Check if value is another attribute
            attr_idx2 = None
            for idx, col in enumerate(schema['columns']):
                if col['name'].lower() == value.lower():
                    attr_idx2 = idx
                    break

            if attr_idx2 is not None:
                val2 = record[attr_idx2]
            else:
                val2 = self._parse_value(value, schema['columns'][attr_idx]['type'])

            return self._compare_values(val1, val2, relop)

        # -------------------------------
        # Step 1: Split by OR
        # -------------------------------
        or_parts = []
        current = []

        for t in tokens:
            if t.lower() == 'or':
                or_parts.append(current)
                current = []
            else:
                current.append(t)

        if current:
            or_parts.append(current)

        # -------------------------------
        # Step 2: Evaluate each OR block (AND inside)
        # -------------------------------
        for part in or_parts:
            and_result = True
            i = 0

            while i < len(part):
                if part[i].lower() == 'and':
                    i += 1
                    continue

                expr = part[i:i+3]

                if len(expr) < 3:
                    break

                and_result = and_result and eval_simple(expr)
                i += 3

            if and_result:
                return True

        return False
    
    def _parse_value(self, value_str, data_type):
        """Parse a value string to its appropriate type"""
        # Remove quotes if present
        if value_str.startswith('"') and value_str.endswith('"'):
            return value_str[1:-1]
        
        if data_type.lower() == 'integer':
            # Try to parse as float first for comparisons like 1.0
            try:
                float_val = float(value_str)
                if float_val == int(float_val):
                    return int(float_val)
                return int(value_str)
            except ValueError:
                return int(value_str)
        elif data_type.lower() == 'float':
            return float(value_str)
        else:  # text
            return value_str
    
    # ========================================================================
    # Command Implementations
    # ========================================================================
    
    def create_database(self, db_name):
        """CREATE DATABASE command"""
        db_name_lower = db_name.lower()
        
        if db_name_lower in self.databases:
            self._write_output(f"Database {db_name} already exists")
            return
        
        # Create database directory
        db_dir = self._get_db_dir(db_name)
        os.makedirs(db_dir, exist_ok=True)
        
        # Add to metadata
        self.databases[db_name_lower] = {
            'name': db_name,
            'tables': {}
        }
        self._save_metadata()
        
        self._write_output(f"Database {db_name} created")
    
    def use_database(self, db_name):
        """USE command"""
        db_name_lower = db_name.lower()
        
        if db_name_lower not in self.databases:
            self._write_output(f"Database {db_name} does not exist")
            return
        
        self.current_db = db_name_lower
        self._write_output(f"Using database {db_name}")
    
    def create_table(self, table_name, columns):
        """CREATE TABLE command"""
        if not self.current_db:
            self._write_output("No database selected")
            return
        
        table_name_lower = table_name.lower()
        
        # Check if table already exists
        if table_name_lower in self.databases[self.current_db]['tables']:
            self._write_output(f"Table {table_name} already exists")
            return
        
        # Parse columns
        schema = {
            'name': table_name,
            'columns': [],
            'primary_key': None
        }
        
        for col in columns:
            col_info = {
                'name': col['name'],
                'type': col['type'],
                'is_primary_key': col.get('is_primary_key', False)
            }
            schema['columns'].append(col_info)
            
            if col_info['is_primary_key']:
                schema['primary_key'] = col['name']
        
        # Create table file
        table_file = self._get_table_file(self.current_db, table_name)
        with open(table_file, 'w') as f:
            f.write(json.dumps(schema) + '\n')
        
        # Create empty index if there's a primary key
        if schema['primary_key']:
            bst = BST()
            self._save_index(table_name, bst)
        
        # Update metadata
        self.databases[self.current_db]['tables'][table_name_lower] = schema
        self._save_metadata()
        
        self._write_output(f"Table {table_name} created")
    
    def describe_table(self, table_name=None):
        """DESCRIBE command"""
        if not self.current_db:
            self._write_output("No database selected")
            return
        
        if table_name and table_name.upper() != 'ALL':
            # Describe specific table
            table_name_lower = table_name.lower()
            if table_name_lower not in self.databases[self.current_db]['tables']:
                self._write_output(f"Table {table_name} does not exist")
                return
            
            schema = self.databases[self.current_db]['tables'][table_name_lower]
            self._write_output(f"\n{schema['name'].upper()}")
            
            for col in schema['columns']:
                pk_str = "\tPRIMARY KEY" if col['is_primary_key'] else ""
                self._write_output(f"{col['name']}:\t\t{col['type']}{pk_str}")
        else:
            # Describe all tables
            for table_name_lower, schema in self.databases[self.current_db]['tables'].items():
                self._write_output(f"\n{schema['name'].upper()}")
                
                for col in schema['columns']:
                    pk_str = "\tPRIMARY KEY" if col['is_primary_key'] else ""
                    self._write_output(f"{col['name']}:\t\t{col['type']}{pk_str}")
    
    def insert_into(self, table_name, values):
        """INSERT command"""
        if not self.current_db:
            self._write_output("No database selected")
            return
        
        table_name_lower = table_name.lower()
        if table_name_lower not in self.databases[self.current_db]['tables']:
            self._write_output(f"Table {table_name} does not exist")
            return
        
        schema = self.databases[self.current_db]['tables'][table_name_lower]
        
        # Check number of values
        if len(values) != len(schema['columns']):
            self._write_output(f"Error: Expected {len(schema['columns'])} values, got {len(values)}")
            return
        
        # Parse and validate values
        parsed_values = []
        for i, (val, col) in enumerate(zip(values, schema['columns'])):
            try:
                parsed_val = self._parse_value(val, col['type'])
                parsed_values.append(parsed_val)
            except Exception as e:
                self._write_output(f"Error: Invalid value for {col['name']}: {val}")
                return
        
        # Check primary key constraint
        if schema['primary_key']:
            pk_idx = None
            for i, col in enumerate(schema['columns']):
                if col['name'] == schema['primary_key']:
                    pk_idx = i
                    break
            
            pk_value = parsed_values[pk_idx]
            
            # Load index and check for duplicate
            bst = self._load_index(table_name)
            if bst.search(pk_value) is not None:
                self._write_output(f"Error: Duplicate primary key value: {pk_value}")
                return
        
        # Append to table file and get record position
        table_file = self._get_table_file(self.current_db, table_name)
        
        # Count current records to get position
        record_position = 0
        with open(table_file, 'r') as f:
            f.readline()  # Skip header
            for line in f:
                if line.strip():
                    record_position += 1
        
        # Write record
        with open(table_file, 'a') as f:
            f.write(json.dumps(parsed_values) + '\n')
        
        # Update index if primary key exists
        if schema['primary_key']:
            bst = self._load_index(table_name)
            bst.insert(pk_value, record_position)
            self._save_index(table_name, bst)
        
        self._write_output("1 row inserted")
        
    def _extract_pk_condition(self, condition, schema):
        """WHERE에서 pk = value 형태 추출"""
        if not condition or not schema['primary_key']:
            return None

        pk = schema['primary_key'].lower()

        tokens = self._tokenize_condition(condition)

        # 단순 형태만 처리 (id = 3)
        if len(tokens) == 3:
            attr, op, value = tokens
            if attr.lower() == pk and op == '=':
                return value

        return None
    
    def select_from(self, attr_list, table_list, condition=None, aggregate=None):
        """SELECT command"""
        if not self.current_db:
            self._write_output("No database selected")
            return []

        # =========================================================
        # 1. MULTI TABLE 
        # =========================================================
        if len(table_list) > 1:
            combined_schema = {'columns': []}
            schemas = []

            # schema 결합
            for table_name in table_list:
                schema = self.databases[self.current_db]['tables'][table_name.lower()]
                schemas.append(schema)
                for col in schema['columns']:
                    combined_schema['columns'].append(col)

            # Load each tables
            table_records = []
            for table_name, schema in zip(table_list, schemas):
                records = self._load_records(table_name, schema)
                table_records.append(records)

            # Cartesian Product
            def cartesian_product(lists):
                result = [[]]
                for lst in lists:
                    temp = []
                    for r in result:
                        for item in lst:
                            temp.append(r + item)
                    result = temp
                return result

            all_records = cartesian_product(table_records)

            # apply WHERE
            records = []
            for record in all_records:
                if self._evaluate_condition(condition, record, combined_schema):
                    records.append(record)

            schema = combined_schema

        # =========================================================
        # 2. SINGLE TABLE
        # =========================================================
        else:
            table_name = table_list[0]
            table_name_lower = table_name.lower()

            if table_name_lower not in self.databases[self.current_db]['tables']:
                self._write_output(f"Table {table_name} does not exist")
                return []

            schema = self.databases[self.current_db]['tables'][table_name_lower]

            pk_value = self._extract_pk_condition(condition, schema)

            if pk_value is not None:
                # BST search
                bst = self._load_index(table_name)
                pos = bst.search(self._parse_value(pk_value, 
                        next(col['type'] for col in schema['columns'] if col['name'] == schema['primary_key'])
                ))

                records = []

                if pos is not None:
                    table_file = self._get_table_file(self.current_db, table_name)

                    with open(table_file, 'r') as f:
                        f.readline()
                        all_records = [json.loads(line.strip()) for line in f if line.strip()]

                    if pos < len(all_records):
                        record = all_records[pos]
                        if self._evaluate_condition(condition, record, schema):
                            records.append(record)
            else:
                records = self._load_records(table_name, schema, condition)

        # =========================================================
        # 3. No results
        # =========================================================
        if not records:
            if not aggregate:
                self._write_output("Nothing found")
            return []

        # =========================================================
        # 4. Aggregate
        # =========================================================
        if aggregate:
            return self._handle_aggregate(aggregate, attr_list, records, schema)

        # =========================================================
        # 5. SELECT column
        # =========================================================
        if attr_list == ['*']:
            selected_indices = list(range(len(schema['columns'])))
            selected_names = [col['name'] for col in schema['columns']]
        else:
            selected_indices = []
            selected_names = []

            for attr in attr_list:
                found = False
                for i, col in enumerate(schema['columns']):
                    if col['name'].lower() == attr.lower():
                        selected_indices.append(i)
                        selected_names.append(col['name'])
                        found = True
                        break

                if not found:
                    self._write_output(f"Error: Unknown attribute {attr}")
                    return []

        # =========================================================
        # 6. print
        # =========================================================
        header = "\t".join(selected_names)
        self._write_output(header)
        self._write_output("-" * len(header))

        result_records = []
        for idx, record in enumerate(records, 1):
            selected_values = [str(record[i]) for i in selected_indices]
            self._write_output(f"{idx}.\t" + "\t".join(selected_values))
            result_records.append([record[i] for i in selected_indices])

        return result_records
    
    def _load_records(self, table_name, schema, condition=None):
        """Load records from table file"""
        table_file = self._get_table_file(self.current_db, table_name)
        records = []
        
        # If there's a primary key, use in-order traversal
        if schema['primary_key']:
            bst = self._load_index(table_name)
            traversal = bst.inorder_traversal()
            
            # Load all records into memory indexed by position
            all_records = []
            with open(table_file, 'r') as f:
                f.readline()  # Skip header
                for line in f:
                    if line.strip():
                        all_records.append(json.loads(line.strip()))
            
            # Retrieve in BST order
            for key, pos in traversal:
                if pos < len(all_records):
                    record = all_records[pos]
                    if self._evaluate_condition(condition, record, schema):
                        records.append(record)
        else:
            # No primary key, just read sequentially
            with open(table_file, 'r') as f:
                f.readline()  # Skip header
                for line in f:
                    if line.strip():
                        record = json.loads(line.strip())
                        if self._evaluate_condition(condition, record, schema):
                            records.append(record)
        
        return records
    
    def _handle_aggregate(self, aggregate, attr_list, records, schema):
        """Handle aggregate functions"""

        agg_type = aggregate['type']

        # =====================================================
        # COUNT
        # =====================================================
        if agg_type == 'count':
            result = len(records)
            self._write_output(f"COUNT(*): {result}")
            return result

        attr_name = aggregate.get('attr')
        if not attr_name:
            self._write_output("Error: Aggregate requires attribute name")
            return None

        # attribute index
        attr_idx = None
        for i, col in enumerate(schema['columns']):
            if col['name'].lower() == attr_name.lower():
                attr_idx = i
                break

        if attr_idx is None:
            self._write_output(f"Error: Unknown attribute {attr_name}")
            return None

        # =====================================================
        # result value
        # =====================================================
        values = [record[attr_idx] for record in records]

        # =====================================================
        # MIN
        # =====================================================
        if agg_type == 'min':
            result = min(values)
            self._write_output(f"MIN({attr_name}): {result}")
            return result

        # =====================================================
        # MAX
        # =====================================================
        elif agg_type == 'max':
            result = max(values)
            self._write_output(f"MAX({attr_name}): {result}")
            return result

        # =====================================================
        # AVERAGE
        # =====================================================
        elif agg_type == 'average':
            try:
                numeric_values = [float(v) for v in values]
            except:
                self._write_output("Error: Non-numeric values for average")
                return None

            result = sum(numeric_values) / len(numeric_values)
            self._write_output(f"AVERAGE({attr_name}): {result}")
            return result
    
    def update_table(self, table_name, set_clauses, condition=None):
        """UPDATE command"""
        if not self.current_db:
            self._write_output("No database selected")
            return

        table_name_lower = table_name.lower()
        if table_name_lower not in self.databases[self.current_db]['tables']:
            self._write_output(f"Table {table_name} does not exist")
            return

        schema = self.databases[self.current_db]['tables'][table_name_lower]

        pk_name = schema['primary_key']
        pk_idx = None

        if pk_name:
            for i, col in enumerate(schema['columns']):
                if col['name'] == pk_name:
                    pk_idx = i
                    break

        table_file = self._get_table_file(self.current_db, table_name)

        # Load all records
        all_records = []
        with open(table_file, 'r') as f:
            header = f.readline()
            for line in f:
                if line.strip():
                    all_records.append(json.loads(line.strip()))

        # Update matching records
        updated_count = 0
        needs_reindex = False

        for i, record in enumerate(all_records):
            if self._evaluate_condition(condition, record, schema):

                # PK 중복 체크 — WHERE 조건에 맞는 행에 대해서만, 본인 행 제외
                if pk_name and pk_name in set_clauses:
                    new_pk_val = self._parse_value(
                        set_clauses[pk_name],
                        schema['columns'][pk_idx]['type']
                    )
                    old_pk_val = record[pk_idx]
                    if new_pk_val != old_pk_val:
                        bst = self._load_index(table_name)
                        if bst.search(new_pk_val) is not None:
                            self._write_output(f"Error: Duplicate primary key value: {new_pk_val}")
                            return

                # Apply updates
                for attr, value in set_clauses.items():
                    attr_idx = None
                    for j, col in enumerate(schema['columns']):
                        if col['name'].lower() == attr.lower():
                            attr_idx = j
                            break

                    if attr_idx is not None:
                        parsed_val = self._parse_value(value, schema['columns'][attr_idx]['type'])

                        if schema['columns'][attr_idx]['is_primary_key']:
                            needs_reindex = True

                        record[attr_idx] = parsed_val

                updated_count += 1

        # Write back all records
        with open(table_file, 'w') as f:
            f.write(header)
            for record in all_records:
                f.write(json.dumps(record) + '\n')

        # Rebuild index if needed
        if needs_reindex and schema['primary_key']:
            self._rebuild_index(table_name, schema)

        self._write_output(f"{updated_count} row(s) updated")
    
    def delete_from(self, table_name, condition=None):
        """DELETE command"""
        if not self.current_db:
            self._write_output("No database selected")
            return
        
        table_name_lower = table_name.lower()
        if table_name_lower not in self.databases[self.current_db]['tables']:
            self._write_output(f"Table {table_name} does not exist")
            return
        
        schema = self.databases[self.current_db]['tables'][table_name_lower]
        
        if condition is None:
            # Delete all records and remove table
            table_file = self._get_table_file(self.current_db, table_name)
            index_file = self._get_index_file(self.current_db, table_name)
            
            if os.path.exists(table_file):
                os.remove(table_file)
            if os.path.exists(index_file):
                os.remove(index_file)
            
            del self.databases[self.current_db]['tables'][table_name_lower]
            self._save_metadata()
            
            self._write_output(f"Table {table_name} deleted")
            return
        
        # Delete specific records
        table_file = self._get_table_file(self.current_db, table_name)
        
        all_records = []
        with open(table_file, 'r') as f:
            header = f.readline()
            for line in f:
                if line.strip():
                    all_records.append(json.loads(line.strip()))
        
        # Filter out records that match condition
        remaining_records = []
        deleted_count = 0
        
        for record in all_records:
            if not self._evaluate_condition(condition, record, schema):
                remaining_records.append(record)
            else:
                deleted_count += 1
        
        # Write back remaining records
        with open(table_file, 'w') as f:
            f.write(header)
            for record in remaining_records:
                f.write(json.dumps(record) + '\n')
        
        # Rebuild index
        if schema['primary_key']:
            self._rebuild_index(table_name, schema)
        
        self._write_output(f"{deleted_count} row(s) deleted")
    
    def _rebuild_index(self, table_name, schema):
        """Rebuild the BST index for a table"""
        bst = BST()
        table_file = self._get_table_file(self.current_db, table_name)
        
        # Find primary key index
        pk_idx = None
        for i, col in enumerate(schema['columns']):
            if col['name'] == schema['primary_key']:
                pk_idx = i
                break
        
        # Rebuild index
        position = 0
        with open(table_file, 'r') as f:
            f.readline()  # Skip header
            for line in f:
                if line.strip():
                    record = json.loads(line.strip())
                    bst.insert(record[pk_idx], position)
                    position += 1
        
        self._save_index(table_name, bst)
    
    def rename_table(self, table_name, new_attr_names):
        """RENAME command"""
        if not self.current_db:
            self._write_output("No database selected")
            return
        
        table_name_lower = table_name.lower()
        if table_name_lower not in self.databases[self.current_db]['tables']:
            self._write_output(f"Table {table_name} does not exist")
            return
        
        schema = self.databases[self.current_db]['tables'][table_name_lower]
        
        if len(new_attr_names) != len(schema['columns']):
            self._write_output(f"Error: Expected {len(schema['columns'])} attribute names")
            return
        
        # Update schema
        for i, new_name in enumerate(new_attr_names):
            schema['columns'][i]['name'] = new_name
        
        # Update primary key name if needed
        if schema['primary_key']:
            for col in schema['columns']:
                if col['is_primary_key']:
                    schema['primary_key'] = col['name']
                    break
        
        # Save updated schema to file
        table_file = self._get_table_file(self.current_db, table_name)
        
        # Read all records
        records = []
        with open(table_file, 'r') as f:
            f.readline()  # Skip old header
            for line in f:
                if line.strip():
                    records.append(line.strip())
        
        # Write with new header
        with open(table_file, 'w') as f:
            f.write(json.dumps(schema) + '\n')
            for record in records:
                f.write(record + '\n')
        
        # Update metadata
        self._save_metadata()
        
        self._write_output(f"Table {table_name} attributes renamed")
    
    def let_table(self, new_table_name, key_attr, select_query):
        """LET command (multi-table 지원)"""
        if not self.current_db:
            self._write_output("No database selected")
            return

        attr_list = select_query['attr_list']
        table_list = select_query['table_list']
        condition = select_query.get('condition')

        import sys, io
        _stdout = sys.stdout
        sys.stdout = io.StringIO()        # print 캡처 시작

        records = self.select_from(attr_list, table_list, condition)

        sys.stdout = _stdout              # print 복원

        if not records:
            self._write_output("No records to create table from")
            return

        source_schemas = []
        for table in table_list:
            source_schemas.append(self.databases[self.current_db]['tables'][table.lower()])

        # flatten columns
        all_columns = []
        for schema in source_schemas:
            all_columns.extend(schema['columns'])

        selected_cols = []

        if attr_list == ['*']:
            for col in all_columns:
                selected_cols.append({
                    'name': col['name'],
                    'type': col['type'],
                    'is_primary_key': False
                })
        else:
            for attr in attr_list:
                found = False
                for col in all_columns:
                    if col['name'].lower() == attr.lower():
                        selected_cols.append({
                            'name': col['name'],
                            'type': col['type'],
                            'is_primary_key': False
                        })
                        found = True
                        break
                if not found:
                    self._write_output(f"Error: Unknown attribute {attr}")
                    return

        # ================================
        # 2. KEY
        # ================================
        key_idx = None
        for i, col in enumerate(selected_cols):
            if col['name'].lower() == key_attr.lower():
                col['is_primary_key'] = True
                key_idx = i
                break

        if key_idx is None:
            self._write_output(f"Error: Key attribute {key_attr} must be in select list")
            return

        new_schema = {
            'name': new_table_name,
            'columns': selected_cols,
            'primary_key': selected_cols[key_idx]['name']
        }

        table_file = self._get_table_file(self.current_db, new_table_name)

        with open(table_file, 'w') as f:
            f.write(json.dumps(new_schema) + '\n')
            for record in records:
                f.write(json.dumps(record) + '\n')

        bst = BST()
        for pos, record in enumerate(records):
            bst.insert(record[key_idx], pos)

        self._save_index(new_table_name, bst)

        self.databases[self.current_db]['tables'][new_table_name.lower()] = new_schema
        self._save_metadata()

        self._write_output(f"Table {new_table_name} created with {len(records)} rows")

# ============================================================================
# Parser
# ============================================================================

class Parser:
    """Recursive descent parser for SQL-like commands"""
    
    def __init__(self, dbms):
        self.dbms = dbms
        self.tokens = []
        self.pos = 0
    
    def tokenize(self, sql):
        """Tokenize SQL string"""
        tokens = []
        current = ""
        in_quote = False
        i = 0
        
        while i < len(sql):
            char = sql[i]
            
            if char == '"':
                if in_quote:
                    current += char
                    tokens.append(current)
                    current = ""
                    in_quote = False
                else:
                    if current:
                        tokens.append(current)
                        current = ""
                    current = char
                    in_quote = True
                i += 1
            elif in_quote:
                current += char
                i += 1
            elif char in ' \t\n\r':
                if current:
                    tokens.append(current)
                    current = ""
                i += 1
            elif char in '();,':
                if current:
                    tokens.append(current)
                    current = ""
                tokens.append(char)
                i += 1
            elif i + 1 < len(sql) and sql[i:i+2] in ['<=', '>=', '!=']:
                if current:
                    tokens.append(current)
                    current = ""
                tokens.append(sql[i:i+2])
                i += 2
            elif char in '=<>':
                if current:
                    tokens.append(current)
                    current = ""
                tokens.append(char)
                i += 1
            else:
                current += char
                i += 1
        
        if current:
            tokens.append(current)
        
        return tokens
    
    def peek(self):
        """Peek at current token"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def consume(self):
        """Consume and return current token"""
        token = self.peek()
        self.pos += 1
        return token
    
    def expect(self, expected):
        """Expect a specific token"""
        token = self.consume()
        if token is None or token.upper() != expected.upper():
            raise Exception(f"Expected {expected}, got {token}")
        return token
    
    def parse(self, sql):
        """Parse SQL command"""
        self.tokens = self.tokenize(sql)
        self.pos = 0
        
        if not self.tokens:
            return
        
        command = self.consume().upper()
        
        try:
            if command == 'CREATE':
                self.parse_create()
            elif command == 'USE':
                self.parse_use()
            elif command == 'DESCRIBE' or command == 'DESC':
                self.parse_describe()
            elif command == 'INSERT':
                self.parse_insert()
            elif command == 'SELECT':
                self.parse_select()
            elif command == 'UPDATE':
                self.parse_update()
            elif command == 'DELETE':
                self.parse_delete()
            elif command == 'RENAME':
                self.parse_rename()
            elif command == 'LET':
                self.parse_let()
            elif command == 'INPUT':
                self.parse_input()
            elif command == 'EXIT':
                return 'EXIT'
            else:
                raise Exception(f"Unknown command: {command}")
        except Exception as e:
            self.dbms._write_output(f"Error: {str(e)}")
    
    def parse_create(self):
        """Parse CREATE command"""
        next_token = self.consume().upper()
        
        if next_token == 'DATABASE':
            db_name = self.consume()
            self.expect(';')
            self.dbms.create_database(db_name)
        elif next_token == 'TABLE':
            table_name = self.consume()
            self.expect('(')
            
            columns = []
            while True:
                col_name = self.consume()
                col_type = self.consume()
                
                col_info = {
                    'name': col_name,
                    'type': col_type,
                    'is_primary_key': False
                }
                
                # Check for PRIMARY KEY
                if self.peek() and self.peek().upper() == 'PRIMARY':
                    self.consume()  # PRIMARY
                    self.expect('KEY')
                    col_info['is_primary_key'] = True
                
                columns.append(col_info)
                
                if self.peek() == ',':
                    self.consume()
                else:
                    break
            
            self.expect(')')
            self.expect(';')
            
            self.dbms.create_table(table_name, columns)
        else:
            raise Exception(f"Invalid CREATE command")
    
    def parse_use(self):
        """Parse USE command"""
        db_name = self.consume()
        self.expect(';')
        self.dbms.use_database(db_name)
    
    def parse_describe(self):
        """Parse DESCRIBE command"""
        table_name = self.consume()
        self.expect(';')
        self.dbms.describe_table(table_name)
    
    def parse_insert(self):
        """Parse INSERT command"""
        table_name = self.consume()
        self.expect('VALUES')
        self.expect('(')
        
        values = []
        while True:
            value = self.consume()
            values.append(value)
            
            if self.peek() == ',':
                self.consume()
            else:
                break
        
        self.expect(')')
        self.expect(';')
        
        self.dbms.insert_into(table_name, values)
    
    def parse_select(self):
        """Parse SELECT command"""
        # Check for aggregate functions
        aggregate = None
        if self.peek() and self.peek().upper() in ['COUNT', 'MIN', 'MAX', 'AVERAGE']:
            agg_func = self.consume().upper()
            self.expect('(')
            
            if agg_func == 'COUNT':
                self.expect('*')
                aggregate = {'type': 'count'}
            else:
                attr_name = self.consume()
                aggregate = {'type': agg_func.lower(), 'attr': attr_name}
            
            self.expect(')')
            attr_list = []
        else:
            # Parse attribute list
            attr_list = []
            while True:
                attr = self.consume()
                attr_list.append(attr)
                
                if self.peek() == ',':
                    self.consume()
                elif self.peek() and self.peek().upper() == 'FROM':
                    break
                else:
                    break
        
        self.expect('FROM')
        
        # Parse table list
        table_list = []
        while True:
            table = self.consume()
            table_list.append(table)
            
            if self.peek() == ',':
                self.consume()
            elif self.peek() and self.peek().upper() == 'WHERE':
                break
            elif self.peek() == ';':
                break
            else:
                break
        
        # Parse WHERE clause
        condition = None
        if self.peek() and self.peek().upper() == 'WHERE':
            self.consume()  # WHERE
            
            condition_tokens = []
            while self.peek() != ';':
                condition_tokens.append(self.consume())
            
            condition = ' '.join(condition_tokens)
        
        self.expect(';')
        
        self.dbms.select_from(attr_list, table_list, condition, aggregate)
    
    def parse_update(self):
        """Parse UPDATE command"""
        table_name = self.consume()
        self.expect('SET')
        
        set_clauses = {}
        while True:
            attr_name = self.consume()
            self.expect('=')
            value = self.consume()
            
            set_clauses[attr_name] = value
            
            if self.peek() == ',':
                self.consume()
            elif self.peek() and self.peek().upper() == 'WHERE':
                break
            elif self.peek() == ';':
                break
            else:
                break
        
        condition = None
        if self.peek() and self.peek().upper() == 'WHERE':
            self.consume()  # WHERE
            
            condition_tokens = []
            while self.peek() != ';':
                condition_tokens.append(self.consume())
            
            condition = ' '.join(condition_tokens)
        
        self.expect(';')
        
        self.dbms.update_table(table_name, set_clauses, condition)
    
    def parse_delete(self):
        """Parse DELETE command"""
        table_name = self.consume()
        
        condition = None
        if self.peek() and self.peek().upper() == 'WHERE':
            self.consume()  # WHERE
            
            condition_tokens = []
            while self.peek() != ';':
                condition_tokens.append(self.consume())
            
            condition = ' '.join(condition_tokens)
        
        self.expect(';')
        
        self.dbms.delete_from(table_name, condition)
    
    def parse_rename(self):
        """Parse RENAME command"""
        table_name = self.consume()
        self.expect('(')
        
        new_names = []
        while True:
            name = self.consume()
            new_names.append(name)
            
            if self.peek() == ',':
                self.consume()
            else:
                break
        
        self.expect(')')
        self.expect(';')
        
        self.dbms.rename_table(table_name, new_names)
    
    def parse_let(self):
        """Parse LET command"""
        table_name = self.consume()
        self.expect('KEY')
        key_attr = self.consume()
        
        # Parse SELECT query
        self.expect('SELECT')
        
        # Parse attribute list
        attr_list = []
        while True:
            attr = self.consume()
            attr_list.append(attr)
            
            if self.peek() == ',':
                self.consume()
            elif self.peek() and self.peek().upper() == 'FROM':
                break
            else:
                break
        
        self.expect('FROM')
        
        # Parse table list
        table_list = []
        while True:
            table = self.consume()
            table_list.append(table)
            
            if self.peek() == ',':
                self.consume()
            elif self.peek() and self.peek().upper() == 'WHERE':
                break
            elif self.peek() == ';':
                break
            else:
                break
        
        # Parse WHERE clause
        condition = None
        if self.peek() and self.peek().upper() == 'WHERE':
            self.consume()  # WHERE
            
            condition_tokens = []
            while self.peek() != ';':
                condition_tokens.append(self.consume())
            
            condition = ' '.join(condition_tokens)
        
        self.expect(';')
        
        select_query = {
            'attr_list': attr_list,
            'table_list': table_list,
            'condition': condition
        }
        
        self.dbms.let_table(table_name, key_attr, select_query)
    
    def parse_input(self):
        """Parse INPUT command"""
        input_file = self.consume()
        
        output_file = None
        if self.peek() and self.peek().upper() == 'OUTPUT':
            self.consume()  # OUTPUT
            output_file = self.consume()
        
        self.expect(';')
        
        # Execute commands from file
        if output_file:
            self.dbms.output_file = output_file
            # Clear output file
            with open(output_file, 'w') as f:
                pass
        
        try:
            with open(input_file, 'r') as f:
                content = f.read()
                
                # Split into commands (by semicolon)
                commands = []
                current_cmd = ""
                in_quote = False
                
                for char in content:
                    if char == '"':
                        in_quote = not in_quote
                    
                    current_cmd += char
                    
                    if char == ';' and not in_quote:
                        commands.append(current_cmd.strip())
                        current_cmd = ""
                
                # Execute each command
                for cmd in commands:
                    if cmd:
                        try:
                            self.parse(cmd)
                        except Exception as e:
                            self.dbms._write_output(f"Error: {str(e)}")
                            continue
        except FileNotFoundError:
            self.dbms._write_output(f"Error: File {input_file} not found")
        finally:
            self.dbms.output_file = None


# ============================================================================
# Main REPL
# ============================================================================

def main():
    """Main REPL loop"""
    dbms = DBMS()
    parser = Parser(dbms)
    
    print("Database Management System")
    print("Type EXIT; to quit")
    print()
    
    current_command = ""
    
    while True:
        try:
            if not current_command:
                line = input("dbms> ")
            else:
                line = input("...> ")
            
            current_command += " " + line
            
            # Check if command is complete (ends with semicolon)
            if ';' in current_command:
                result = parser.parse(current_command.strip())
                current_command = ""
                
                if result == 'EXIT':
                    print("Goodbye!")
                    break
        except KeyboardInterrupt:
            print("\nInterrupted. Type EXIT; to quit")
            current_command = ""
        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            current_command = ""


if __name__ == "__main__":
    main()