FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
COPY sample-models/iris.onnx iris.onnx

RUN pip3 install -r requirements.txt
COPY model .
RUN python3 interface_demo.py
