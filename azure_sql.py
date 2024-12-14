import logging
from sqlalchemy import create_engine, inspect, text
import pandas as pd

class UKCAzureSQL:
    def __init__(self, url, auth_token):
        self.url = url
        self.auth_token = auth_token
        self.engine = None
        self.connection = None
        self.init_engine()

    def init_engine(self):
        """
        Initialize SQL engine connection using PyODBC

        Returns:
            Engine object: connection to the SQL server
        """
        try:
            logging.debug("Database Connection Started")
            connection_str = f"sqlite+{self.url}/?authToken={self.auth_token}&secure=true"
            self.engine = create_engine(connection_str, connect_args={'check_same_thread': False}, echo=True)
            self.connection = self.engine.connect().execution_options(
                isolation_level="AUTOCOMMIT"
            )
            logging.info("Connected to Azure SQL Database")
        except Exception as e:
            logging.error(f"Error connecting to Azure SQL Database: {str(e)}")
            self.engine = None
            raise Exception(str(e))

    def fetch_table_data(self, table_name, query=None):
        """Function to fetch all data from a selected table

        Args:
            table_name (type): description

        Returns:
            type: description
        """
        if table_name == "TRANSACTION":
            query = "SELECT * FROM [TRANSACTION]"

        elif table_name == "TRANSACTION_CLASSIFICATION":
            query = "SELECT NAME FROM DIM.[TRANSACTION_CLASSIFICATION]"

        elif table_name == "DAILY_MENU":
            query = "SELECT * FROM [dbo].[DAILY_MENU]"

        elif table_name == "PROCUREMENT":
            query = "SELECT * FROM [dbo].[PROCUREMENT]"

        elif table_name == "EMPLOYEE_TIME_ENTRY":
            query = "SELECT * FROM [dbo].[EMPLOYEE_TIME_ENTRY]"

        elif table_name == "STALLS_DAILY_SALES":
            query = "SELECT * FROM [dbo].[STALLS_DAILY_SALES]"

        elif table_name == "CLIENT_DETAIL":
            query = "SELECT * FROM [WHAUTOMATE].[CLIENT_DETAIL]"

        elif query:
            pd.read_sql(query, self.connection)

        elif table_name == "MENU_ITEM":
            query = "SELECT * FROM MENU_ITEM"

        elif table_name == "RAW_MATERIAL":
            query = "SELECT * FROM RAW_MATERIAL"

        elif table_name == "RECIPE":
            query = "SELECT * FROM RECIPE "

        elif table_name == "UNIT_MEASURE":
            query = "SELECT * FROM UNIT_MEASURE"

        return pd.read_sql(query, self.connection)

    def execute_query_placeholders(self, query, params, type):
        try:
            if type in ["insert", "delete", "exec", "update"]:
                result = self.connection.execute(query, params)
                return result
            if type == "select":
                result = pd.read_sql(query, con=self.connection)
                return result

        except Exception as e:
            logging.error(str(e))
            print(e)
            raise Exception(str(e))

    def fetch_cell_value(self, table_data, column_name, row_id):
        try:
            row = table_data[table_data["Id"] == row_id]
            return row[column_name].values[0] if not row.empty else None
        except:
            try:
                row = table_data[table_data[column_name] == row_id]
                return row["ID"].values[0] if not row.empty else None
            except Exception as e:
                logging.error("ID column mismatch")

    def insert_row(self, table_name, row_data):
        """
        Inserts a row into the specified table.

        Args:
            table_name (str): The name of the table where the row will be inserted.
            row_data (dict): A dictionary containing column-value pairs for the new row.

        Returns:
            None
        """
        try:
            # Generate query dynamically based on row_data
            columns = ", ".join(row_data.keys())
            placeholders = ", ".join([f":{col}" for col in row_data.keys()])
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            # Execute query with parameters
            self.connection.execute(text(query), **row_data)
            logging.info(f"Row inserted into {table_name} successfully.")
        except Exception as e:
            logging.error(f"Failed to insert row into {table_name}: {e}")
            raise
