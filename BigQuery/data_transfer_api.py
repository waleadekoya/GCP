from google.cloud import bigquery_datatransfer_v1
import google.protobuf.json_format

# https://googleapis.dev/python/bigquerydatatransfer/latest/index.html
# https://cloud.google.com/bigquery-transfer/docs/third-party-transfer
# https://console.cloud.google.com/marketplace/browse?filter=category:data-transfer-services&_ga=2.49015398.198552912.1605890072-1648947292.1605685508
# https://cloud.google.com/bigquery/docs/scheduling-queries

client = bigquery_datatransfer_v1.DataTransferServiceClient()

print(dir(client))