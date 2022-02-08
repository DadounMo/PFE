FROM python:slim

COPY install-iperf.sh .
RUN chmod +x install-iperf.sh
RUN ./install-iperf.sh


COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app


CMD ["python", "client.py"]
