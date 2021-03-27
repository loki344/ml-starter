FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
COPY app .

ENV MODEL_FILE_NAME='iris.onnx'
ENV SOURCE_CODE_FILE='test_input_method.py'

RUN pip3 install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
