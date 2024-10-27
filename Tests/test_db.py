"""
    Name: Database Tests
    Description: Different tests to check the database (creation, insert, delete, update, select)
    Authors: Magaly Camacho [3072618]

    Date Created: 10/26/2024
    Revisions: 
        - None

    Preconditions: 
        - A string with the method to run (run, clean)
    Postconditions:
        - Output file with test results
    Errors/Exceptions: 
        - None
    Side Effects: 
        - None
    Invariants: 
        - run_module_method is defined in utils module
    Known Faults: 
        - None
"""


# Imports
import sys
from database import Database
from Models import Event_, Task, Category, Recurrence
from Models.databaseEnums import ItemType, Priority, Complete, Frequency
from Models.base import Base
from datetime import datetime
from .utils import run_module_method
from contextlib import redirect_stdout


# Paths to output files
SCHEMA_PATH = "./Tests/Output/test_db_schema.txt"
DB_PATH = "./Tests/Output/test_db.db"
PATHS = [SCHEMA_PATH, DB_PATH]


def schema():
    """Gets schema of database"""
    with open(SCHEMA_PATH, "w") as file: # open output file
        with redirect_stdout(file): # redirect output from terminal to file
            print("Table: <table name>\n\tColumn: <column name> - <column type>") # format
        
            # for each table
            for table in Base.metadata.sorted_tables:
                print(f"\nTable: {table.name}") # print it's name

                # print each column and it's data type
                for column in table.columns:
                    print(f"\tColumn: {column.name} - {column.type}")

def help():
    """Prints possible tests that can be run"""
    print("\npython -m Tests.test_db <option>")

    print("Valid options are:")
    print("   schema:  outputs database schema")
    print("   help:    prints syntax and valid options")


# Possible tests
methods = {
    "schema": schema,
    "help": help
}


# Run specified test
if __name__ == "__main__":
    run_module_method("test_db", sys.argv, methods, PATHS)


