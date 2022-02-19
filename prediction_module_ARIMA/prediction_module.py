import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import timedelta
from statsmodels.tsa.arima.model import ARIMA
from kubernetes import client, config


token = "NUuAendilxjox8GDVd03"
org = "primary"
bucket = "primary"


step_size = 3 
steps_ahead = 60

config.load_incluster_config()
v1 = client.AppsV1Api()

base = 850
th = 850

while True:
    with InfluxDBClient(url="http://influxdb.monitoring.svc:8086", token=token, org=org) as client:
        query = 'from(bucket: "primary") |> range(start: -10m) |> filter(fn: (r) => r["_measurement"] == "NetTraffic") |> filter(fn: (r) => r["Type"] == "Received") |> filter(fn: (r) => r["_field"] == "Size")'
        result = client.query_api().query(query, org=org)

    points = []
    time_stamps = []
    for table in result:
        for record in table.records:
                points.append(record.get_value())
                time_stamps.append(record.get_time())

    if len(points)<50 : 
        time.sleep(5)
        continue

    
    model = ARIMA(points,order=(3,0,1))
    model_fit = model.fit()
    predicted_points = model_fit.forecast(steps=steps_ahead)

    last_time = time_stamps[-1]
    with InfluxDBClient(url="http://influxdb.monitoring.svc:8086", token=token, org=org) as client:
        delete_api = client.delete_api()
        delete_api.delete(last_time+timedelta(seconds=3),last_time+timedelta(seconds=600), '_measurement="ARIMATrafficPrediction"', bucket='primary', org='primary')
        write_api = client.write_api(write_options=SYNCHRONOUS)
        p = Point("Threshold").field("value", th)
        write_api.write(bucket, org, p)
        for i in range(len(predicted_points)):
            p = Point("ARIMATrafficPrediction").tag("Algo", "ARIMA").field("Size", int(predicted_points[i])).time(last_time+timedelta(seconds=step_size*(i+1)))
            write_api.write(bucket, org, p) 
    
    print('Predictions have been inserted to DB')

    if max(predicted_points)>th:
        print("current th :",th)
        ret = v1.read_namespaced_deployment_scale("helloweb","default")
        cuurent_pods = ret.spec.replicas+1
        th = base*cuurent_pods
        print("new th : ",th)
        ret.spec.replicas = ret.spec.replicas+1
        rpla = v1.replace_namespaced_deployment_scale("helloweb","default", ret)
        print(rpla)
    time.sleep(5)