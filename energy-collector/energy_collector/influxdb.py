# export INFLUXDB_TOKEN=

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# TODO: write influxdb wrapper
def write():
    write_api = client.write_api(write_options=SYNCHRONOUS)

    for value in range(5000):
        point = (
            Point("measurement1")
            .tag("tagname1", "tagvalue1")
            .field("field1", value)
        )
        write_api.write(bucket=bucket, org=org, record=point)
        # time.sleep(1) # separate points by 1 second

def simple_query():
    query_api = client.query_api()

    query = f"""from(bucket: "{bucket}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "measurement1")"""
    tables = query_api.query(query, org=org)

    for table in tables:
        for record in table.records:
            print(record)

def flux_query():
    query = f"""from(bucket: "{bucket}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "measurement1")
    |> mean()"""
    tables = query_api.query(query, org=org)

    for table in tables:
        for record in table.records:
            print(record)

if __name__ == '__main__':
    # token = os.environ.get("INFLUXDB_TOKEN")
    token = "-mJVxHfZSyCiI8PdW-4usF8PebiExZ2lQLPBfjS2d__255VaMCDVZEVOMzOGULlvqhVLNF9F3_3e28CXWMaP-g=="
    org = "home"
    bucket = "energy"
    url = "http://localhost:8086"
    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    write()


