from google.cloud import bigquery
from big_query_api import BigQuery
import pandas as pd

# https://github.com/googleapis/python-bigquery
# https://googleapis.dev/python/google-api-core/latest/auth.html
# https://cloud.google.com/bigquery/docs/bq-command-line-tool

# client = bigquery.Client()

QUERY = (
    """
    SELECT
      *
    FROM
      `aesthetic-way-296008.babynames.names_yob2019`
    WHERE
      count > 10000
      AND gender = 'F'
    ORDER BY
      count DESC
    LIMIT
      1000;
    """
)

# query_job = client.query(QUERY)  # API request
# rows = query_job.result() # waits for query to finish
#
# for row in rows:
#     print(row.name, row.gender, row.count)

client = BigQuery('aesthetic-way-296008.babynames.names_yob2019')
print(client.table_exists)
print(client.get_query_results(QUERY, configuration={"query": {"useQueryCache": True, "dryRun": True}}))
# print(pd.read_gbq(QUERY))
