FROM python:3.7-slim

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app


CMD ["python", "prediction_module.py"]
