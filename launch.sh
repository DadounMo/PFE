#!/bin/bash
docker build -t iperf-client iperf-client 
docker build -t module_lstm prediction_module_LSTM
docker build -t module_lr prediction_module_LR
docker build -t module_arima prediction_module_ARIMA

docker rm -f iperf-client module_lstm module_lr module_arima

docker run -dit --name iperf-client iperf-client
docker run -dit --name module_lstm module_lstm 
docker run -dit --name module_lr module_lr 
docker run -dit --name module_arima module_arima