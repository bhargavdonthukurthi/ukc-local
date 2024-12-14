import logging
import libsql_experimental as libsql
import pandas as pd
from sqlalchemy import create_engine, text


class UKCAzureSQL:
    def __init__(self, url, auth_token):
        self.url = url
        self.auth_token = auth_token
        self.conn = None
        self.engine = None
        self.init_connection()

    def init_connection(self):
        """
        Initialize libsql connection using the provided URL and auth token and create the SQLAlchemy engine.
        """
        try:
            self.url = url
            self.auth_token = auth_token
            logging.debug("Database Connection Started")
            dbUrl = f"sqlite+{self.url}/?authToken={self.auth_token}&secure=true"
            self.engine = create_engine(dbUrl, connect_args={'check_same_thread': False}, echo=True)
        except Exception as e:
            logging.error(f"Error connecting to libsql database: {str(e)}")
            self.conn = None
            self.engine = None
            raise Exception(str(e))

    def fetch_table_data(self, table_name, query=None):
        """
        Fetch all data from a selected table or run a custom query.

        Args:
            table_name (str): The name of the table to query.
            query (str, optional): The custom query to run.

        Returns:
            pd.DataFrame: DataFrame with the result set.
        """
        if query:
            return pd.read_sql(query, self.engine)

        # Example queries
        query = f"SELECT * FROM {table_name}"
        return pd.read_sql(query, self.engine)

    def execute_query_placeholders(self, query, params, query_type):
        """
        Execute a query with placeholders and parameters.
        """
        try:
            with self.engine.connect() as connection:
                if query_type in ["insert", "delete", "exec", "update"]:
                    connection.execute(text(query), **params)
                    connection.commit()
                    return "Query executed successfully"
                if query_type == "select":
                    result = pd.read_sql(query, con=connection)
                    return result
        except Exception as e:
            logging.error(f"Error executing query: {str(e)}")
            raise Exception(str(e))

# Example of using the class
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    # Example connection details
    url = "libsql://bhargav-bhargavdonthukurthi.turso.io"
    auth_token = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3MzQwMTUxMzYsImlkIjoiYTc4NjExOGMtYTY1MC0xMWVlLTg1YzktMWE1OTZkZGUwY2MwIn0.3SkOzckYCTCPCjV0_JlbFyCWXs5iZveI3-XMu6WOd2zC4JHuqSKXJNXMUu-iq6NxtaAmMVFGIr5evDJnybR1Bg"
    
    # Create instance of UKCAzureSQL
    db = UKCAzureSQL(url, auth_token)
    
    # Fetch data from a table
    data = db.fetch_table_data("users")
    print(data)
