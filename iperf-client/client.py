import imp
from typing import Tuple
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import subprocess
import csv
import time
import requests

token = "NUuAendilxjox8GDVd03"
org = "primary"
bucket = "primary"


my_list = []
with open('dataset.csv','r') as f:
  data = csv.DictReader(f)
  for row in data:
      my_list.append(float(row['values']))

URL = 'http://192.168.49.2:30031/'

while True:
	for i in my_list:
		res = dict()
		for x in range(int(i)*10):
			response = requests.get(URL)
			host = response.text.splitlines()[-1].split()[-1]
			if(host in res.keys()):
				res[host] = res[host]+1
			else:
				res[host] = 1
		print(res)

		pts = []
		for pod in res : 
			pts.append(Point("NetTrafficByPod").tag("PodName", pod).field("Size", res[pod]))

		print(pts)

		p = Point("NetTraffic").tag("Type", "Received").field("Size", i*10)
		with InfluxDBClient(url="http://192.168.49.2:32405/", token=token, org=org) as client:
			write_api = client.write_api(write_options=SYNCHRONOUS)
			write_api.write(bucket, org, p)
			write_api.write(bucket, org, pts)
		print('Data added to DB')
		time.sleep(3)

