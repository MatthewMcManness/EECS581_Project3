"""
    Name: Database Tests
    Description: Different tests to check the database (creation, insert, delete, update, select)
    Authors: Magaly Camacho [3072618]

    Date Created: 10/26/2024
    Revisions: 
        - 10/27/2024 Magaly Camacho
            Removed Models.databaseEnums.Complete import
        - 10/29/2024 Magaly Camacho
            Added data tests (insert, update, delete)
        - 11/01/2024 Magaly Camacho
            Updated way to get session to match Database class method

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
from Models import Event_, Task
from Models.databaseEnums import Priority
from Models.base import Base
from datetime import datetime
from .utils import run_module_method
from contextlib import redirect_stdout
from sqlalchemy import select


# Paths to output files
TEST_PATH = "./Tests/Output/test_db" # partial path to put test results at
DB_PATH = TEST_PATH + ".db" # database (path to create it at)
SCHEMA_PATH = TEST_PATH + "_schema.txt" # schema test results
INSERT_PATH = TEST_PATH + "_insert.txt" # insert test results
SELECT_PATH = TEST_PATH + "_select.txt" # select test results
DELETE_PATH = TEST_PATH + "_delete.txt" # delete test results
PATHS = [DB_PATH, SCHEMA_PATH, INSERT_PATH, SELECT_PATH, DELETE_PATH] # all paths used by this test


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


def insert():
    """Insert some dummy data"""
    with open(INSERT_PATH, "w") as file: # open output file
        with redirect_stdout(file): # redirect output from terminal to file
            db = Database(DB_PATH, True) # connect to db, debug statements on

            # create some event
            event1 = Event_(
                name="Event 1",
                place="Eaton Hall", 
                start_time=datetime(
                    year=2024, 
                    month=10, 
                    day=29
                )
            )

            # create some task
            task1 = Task(
                name="Task 1",
                priority = Priority.HIGH,
                notes="Demo insert"
            )

            # start db transaction, will commit if no exceptions are raised
            with db.get_session() as session, session.begin(): 
                session.add(event1) # add event
                session.add(task1) # add task


def select_t():
    """Select events and tasks"""
    with open(SELECT_PATH, "w") as file: # open output file
        with redirect_stdout(file): # redirect output from terminal to file
            db = Database(DB_PATH, True)

            # start db session, rollback any changes
            with db.get_session() as session:
                for table in [Event_, Task]: # Event, and for Task
                    stmt = select(table).where(True) # select all

                    # print all records
                    for record in session.scalars(stmt):
                        print(f"\n{record}\n")


def delete_t():
    """Delete event with id=1"""
    with open(DELETE_PATH, "w") as file: # open output file
        with redirect_stdout(file): # redirect output from terminal to file
            db = Database(DB_PATH, True) # connect to db

            # start db transaction, will commit if no exceptions are raised
            with db.get_session() as session, session.begin():
                event1 = session.get(Event_, 1) # get event by id
                session.delete(event1) # delete event


def help():
    """Prints possible tests that can be run"""
    print("\npython -m Tests.test_db <option>")

    print("\nValid options are:")
    print("   schema:  outputs database schema")
    print("   insert:  inserts some dummy data")
    print("   select:  prints data in database")
    print("   delete:  deletes event with id=1")
    print("   help:    prints syntax and valid options\n")


# Possible tests
methods = {
    "help": help,
    "schema": schema,
    "insert": insert,
    "select": select_t,
    "delete": delete_t
}


# Run specified test
if __name__ == "__main__":
    run_module_method("test_db", sys.argv, methods, PATHS)