import sqlite3
from typing import Any


class DataType():
    """
        SQL DATA Types Enums
    """
    BOOL = "BOOL"
    DATE = "DATE"
    INT = "INT"

    @classmethod
    def CHAR(self, size):
          '''
          A FIXED length string (can contain letters, numbers, 
          and special characters). The size parameter specifies the 
          column length in characters - can be from 0 to 255. Default is 1
          '''
          return f"CHAR({size})"
     
    @classmethod
    def VARCHAR(sefl, size):
          '''
          A VARIABLE length string (can contain letters, numbers, and special characters). 
          The size parameter specifies the maximum string length in characters 
          - can be from 0 to 65535
          '''
          return f"VARCHAR({size})"
    


class Column():
    def __init__(self, key : str, type : DataType, required : bool = False):
            self.key = key.upper()
            self.type = type
            self.required = "NOT NULL" if required else ""
    
    def __str__(self):
         return f"{self.key} {self.type} {self.required}"
    


class Database():
    def __init__(self) -> None:
        try:
            self.connection = sqlite3.connect('todo.db')
            print("Opened database successfully")
        except:
            print("Something went wrong while connecting to database..")
    
    def create_table(self, table_name : str, columns : list[Column]):
        string_columns = []
        for column in columns:
             string_columns.append(column.__str__())

        try:
            query = f"CREATE TABLE {table_name.upper()} ({','.join(string_columns)});"
            self.query(query)
        except:
             print("Something went wrong while creating table")

    def insert_into(self, table_name : str, column_names : list[str], column_values : list[str]):
        query = f"""INSERT INTO {table_name.upper()} ({','.join(column_names)}) \
                    VALUES ({', '.join(column_values)})"""
        self.query(query)

    
    def query(self, query):
        self.connection.execute(query)
        self.connection.commit()
        print("Running query..")
        
         



database = Database()

Name = Column("name", DataType.CHAR(255))
Age = Column("age", DataType.INT)

database.create_table(table_name="dummy3", columns=[Name, Age])
database.insert_into("DUMMY3", column_names=[Name.key, Age.key], column_values=["'Njabulo'", "20"])
database.insert_into("DUMMY3", column_names=[Name.key, Age.key], column_values=["'Siyaboga'", "30"])



