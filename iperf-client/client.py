from typing import Tuple
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import subprocess
import csv
import time


token = "FWe2VDkJXDmLp0o9Qid4"
org = "primary"
bucket = "primary"


my_list = []
with open('dataset.csv','r') as f:
  data = csv.DictReader(f)
  for row in data:
      my_list.append(float(row['values']))

while True:
	for i in my_list:
		#process = subprocess.run('iperf3 -c iperf-server.default.svc -n {}M'.format(i), shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True, timeout=5)
		#output = process.stdout
		#res = output.splitlines()[-3].split()
		#size = float(res[4])
		#tos = res[5]
		#if tos == 'KBytes' : 
		#	size = size/1024
		#elif tos[5] == 'GBytes':
		#	size = size*1024 
		#print(size)
		p = Point("NetTraffic").tag("Type", "Received").field("Size", i)
		with InfluxDBClient(url="http://influxdb:8086", token=token, org=org) as client:
			write_api = client.write_api(write_options=SYNCHRONOUS)
			write_api.write(bucket, org, p)
		print('Data added to DB')
		time.sleep(3)

