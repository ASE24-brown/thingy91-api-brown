from influxdb_client import InfluxDBClient, Point
import os

# Load InfluxDB connection settings
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://influxdb:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "YOUR_INFLUXDB_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "your_org")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "your_bucket")

# Initialize InfluxDB client
influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = influx_client.write_api()
query_api = influx_client.query_api()
