import sqlite3
import uuid


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
    def __init__(self, key: str, type: DataType, required: bool = False, unique=False):
        self.primary = False
        self.key = key.upper()
        self.type = type
        self.required = "NOT NULL" if required else ""
        self.unique = "UNIQUE" if unique else ""

    def __str__(self):
        return f"{self.key} {self.type} {self.required} {self.unique}"


class PrimaryColumn(Column):
    def __init__(self, key: str, type: DataType, required: bool = False, unique=False):
        super().__init__(key, type, required, unique)
        self.primary = True

    def __str__(self):
        return f"{self.key} {self.type} {self.required} PRIMARY KEY"


class Database():
    columns: list[Column] = []

    def __init__(self) -> None:
        try:
            self.connection = sqlite3.connect('todo.db')
            print("Opened database successfully")

        except Exception as e:
            print(e)
            print("Something went wrong while connecting to database..")

    def create_table(self, table_name: str, columns: list[Column]):
        '''
            Create a new table if the table does not exit
            @Param table_name : str, columns -> list of Columns

        '''

        string_columns = []
        for column in columns:
            string_columns.append(column.__str__())

        try:
            query = f"CREATE TABLE {table_name.upper()} ({','.join(string_columns)});"
            self.query(query)
        except Exception as e:
            print(e)
            print("Something went wrong while creating table")

    def insert_into(self, table_name: str, column_names: list[str], column_values: list[str]):
        '''
            Insert new data to a table
            @Param table_name : str, columns_names -> list of strings, column_values -> list of string values

        '''
        print("Inserting data....")
        try:
            query = f"""INSERT INTO {table_name.upper()} ({','.join(column_names)}) \
                    VALUES ({', '.join(len(column_values)*"?")})"""
            self.prepared_query(query, tuple([i for i in column_values]))
        except Exception as e:
            if isinstance(e, sqlite3.IntegrityError):
                print(
                    f"{', '.join(self.get_unique_columns())} must be unique!")

    def select(self, table_name, filter_columns: list[str] = []):
        '''
            Get data from specified table, filter columns is optional, else it will return all columns
            @Param table_name : str, columns -> list of String [column names]

        '''
        if (len(filter_columns) == 0):
            query = f"SELECT * from {table_name}"
            res = self.query(query)
            print(self.format_select_res(res))
        else:
            query = f"SELECT {', '.join(filter_columns)} from {table_name.upper()} "
            res = self.query(query)
            print(self.format_select_res(res))

    def select_by_key(self, table_name, filter_key, filter_value):
        query = f"SELECT * from {table_name} WHERE {filter_key} = ?"
        res = self.prepared_query(query, (filter_value, ))
        return self.format_select_res(res)

    def add_columns(self, columns: list[Column]):
        # self.columns.append([*columns])
        for column in columns:
            if column in self.columns:
                print("Column already exit")
            else:
                self.columns.append(column)

    def get_unique_columns(self) -> list[Column]:
        unique_columns = []
        for column in self.columns:
            if "UNIQUE" in column.__str__():
                unique_columns.append(column.key)
        return unique_columns

    def update_by_id(self, table_name, id, column, new_value):
        try:
            query = f"UPDATE {table_name.upper()} set {column} = {new_value} where ID=?"
            res = self.prepared_query(query, (id,))
        except Exception as e:
            print(e)
            print("Something went wrong while trying to update.")

    def delete_by_id(self, table_name, id):
        try:
            query = f"DELETE from {table_name} where ID=(?)"
            res = self.prepared_query(query, (id,))
        except Exception as e:
            print(e)
            print("Something went wrong while trying to delete")

    def query(self, query):
        '''
            Run an SQL query
            @Param SQL query
            @Return instance of query/ results from query

        '''
        res = self.connection.execute(query)
        self.connection.commit()
        print("Successfully ran query!")
        return res

    def prepared_query(self, query, params: tuple):
        res = self.connection.execute(query, params)
        self.connection.commit()
        print("Successfully ran query!")
        return res

    def format_select_res(self, results) -> list[tuple]:
        '''
            Formats data returned from SQL as a list of tuples
            @Param results -> instance of SQL results

        '''
        data = []
        try:
            for row in results:
                colum = []
                for column in row:
                    colum.append(column)
                data.append(tuple(colum))
                colum = []
            return data
        except Exception as e:
            print(e)
            print("Something went wrong while trying to format select.")
            return []


# database = Database()

# Id = Column("id", DataType.CHAR(36), required=True, unique=True)
# Name = Column("name", DataType.CHAR(255), unique=True)
# Age = Column("age", DataType.INT)

# database.add_columns([Id, Name, Age])


# database.create_table(table_name="dummy4", columns=[Id, Name, Age])
# database.insert_into("DUMMY4", column_names=[
#                      Id.key, Name.key, Age.key], column_values=[f"{uuid.uuid4()}", "Njabulo", "20"])
# database.insert_into("DUMMY4", column_names=[
#                      Id.key, Name.key, Age.key], column_values=[f"{uuid.uuid4()}", "Siyabogak", "30"])

# database.select("dummy4")

# database.update_by_id(
#     "dummy4", "0ccd7049-ffe7-427b-9f2f-855dbfc59310", "Age", "27")
