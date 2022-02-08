import keras
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from pickle import load
from datetime import timedelta
from sklearn.preprocessing import MinMaxScaler
import numpy as np 


model = keras.models.load_model('trained_model')
scaler = load(open('scaler.pkl', 'rb'))

token = "f9c38TMHYgj-J6v8eAM3G-5-eCiDhT-GoLm_rkQdssjQ0NTUxNu646bCotRq3qvg1a0BRt-UDxI1pb7upuaU5w=="
org = "pfe"
bucket = "pfe"

step_size = 3 
steps_ahead = 60
input_num = 30

pt = False
showa = False
th = 85

time.sleep(200)
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

    scaled_pointes = scaler.transform(np.array(points).reshape(-1,1))
    scaled_pointes = scaled_pointes.reshape(scaled_pointes.shape[0])

    for step in range(steps_ahead):
        Xs = np.reshape(scaled_pointes[-input_num:], (1, 1, input_num))
        Y = model.predict(Xs)
        scaled_pointes = np.concatenate([scaled_pointes,Y[0]])

    predicted_points = scaler.inverse_transform(np.array(scaled_pointes[-steps_ahead:]).reshape(-1,1))
    predicted_points = predicted_points.reshape(predicted_points.shape[0])

    if not(pt) :
        if max(predicted_points)>th:
            showa = True
            pt = True

    last_time = time_stamps[-1]
    with InfluxDBClient(url="http://172.17.0.4:8086", token=token, org=org) as client:
        delete_api = client.delete_api()
        delete_api.delete(last_time+timedelta(seconds=7),last_time+timedelta(seconds=600), '_measurement="LSTMTrafficPrediction"', bucket='pfe', org='pfe')    
        delete_api.delete(last_time+timedelta(seconds=7),last_time+timedelta(seconds=600), '_measurement="LSTMAfterAction"', bucket='pfe', org='pfe')    
        write_api = client.write_api(write_options=SYNCHRONOUS)
        for i in range(len(predicted_points)):
            p = Point("LSTMTrafficPrediction").tag("Algo", "LSTM").field("Size", int(predicted_points[i])).time(last_time+timedelta(seconds=step_size*(i+1)))
            write_api.write(bucket, org, p)
            if showa:
                p = Point("LSTMAfterAction").tag("Algo", "LSTM").field("Size", int(predicted_points[i])*0.5).time(last_time+timedelta(seconds=step_size*(i+1)))
                write_api.write(bucket, org, p)
    
    print('Predictions have been inserted to DB')
    time.sleep(10)