FROM tensorflow/tensorflow

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app


CMD ["python", "prediction_module.py"]
