from typing import Union, Tuple

from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import pandas as pd


# https://github.com/googleapis/python-bigquery
# https://googleapis.dev/python/google-api-core/latest/auth.html
# https://cloud.google.com/bigquery/docs/bq-command-line-tool


class BigQuery:

    def __init__(self, table_id: Union[str, None] = None):
        self.client = bigquery.Client()
        self.table_id = table_id  # "your-project.your_dataset.your_table"

    @property
    def table_exists(self):
        try:
            if self.client.get_table(self.table_id):  # Make an API request.
                return "Table '{}' already exists.".format(self.table_id)
        except NotFound:
            print("Table {} is not found.".format(self.table_id))
            return None

    @staticmethod
    def get_query_results(query: Union[str, Tuple], configuration: Union[dict, None] = None) -> pd.DataFrame:
        # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
        print("The query data:")
        return pd.read_gbq(query, configuration=configuration)

    def add_empty_column(self, field_name: str, data_type: str):
        table = self.client.get_table(self.table_id)  # Make an API request.
        original_schema = table.schema
        new_schema = original_schema[:]  # Creates a copy of the schema.
        new_schema.append(bigquery.SchemaField(field_name, data_type))

        table.schema = new_schema
        table = self.client.update_table(table, ["schema"])  # Make an API request.

        if len(table.schema) == len(original_schema) + 1 == len(new_schema):
            print("A new column has been added.")
        else:
            print("The column has not been added.")
