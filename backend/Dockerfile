FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app
COPY app .
COPY requirements.txt ./requirements.txt

ENV IS_IN_DOCKER=true

RUN pip3 install -r requirements.txt
RUN pip3 install -r ./custom_model/custom_requirements.txt

CMD uvicorn main:app --host 0.0.0.0 --port $PORT
