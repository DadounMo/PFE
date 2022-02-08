import time
from datetime import timedelta
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from sklearn.linear_model import LinearRegression
import numpy as np 

token = "f9c38TMHYgj-J6v8eAM3G-5-eCiDhT-GoLm_rkQdssjQ0NTUxNu646bCotRq3qvg1a0BRt-UDxI1pb7upuaU5w=="
org = "pfe"
bucket = "pfe"

time.sleep(20)

step_size = 5
pt = False
showa = False
th = 85

while True:
    with InfluxDBClient(url="http://172.17.0.4:8086", token=token, org=org) as client:
        query = 'from(bucket: "pfe") |> range(start: -7m) |> filter(fn: (r) => r["_measurement"] == "NetTraffic") |> filter(fn: (r) => r["Type"] == "Received") |> filter(fn: (r) => r["_field"] == "Size")'
        result = client.query_api().query(query, org=org)

    points = []
    time_stamps = []
    for table in result:
        for record in table.records:
                points.append(record.get_value())
                time_stamps.append(record.get_time())
    last_time = time_stamps[-1]

    points = points[-5:]
    num = np.array([i+1 for i in range(5)]).reshape(-1,1)
    reg = LinearRegression().fit(num, points)
    y_hat = reg.predict(np.array([6,7,8,9,10]).reshape(-1,1))
    predicted_points = y_hat.tolist()
    if not(pt) :
        if max(predicted_points)>th:
            showa = True
            pt = True
    with InfluxDBClient(url="http://172.17.0.4:8086", token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        for i in range(len(predicted_points)):
            p = Point("TrafficPrediction").tag("Algo", "LR").field("Size", int(predicted_points[i])).time(last_time+timedelta(seconds=step_size*(i+1)))
            write_api.write(bucket, org, p)
            if showa:
                p = Point("AfterAction").tag("Algo", "LR").field("Size", int(predicted_points[i])*0.5).time(last_time+timedelta(seconds=step_size*(i+1)))
                write_api.write(bucket, org, p)

    
    print('Predictions have been inserted to DB')
    time.sleep(7)