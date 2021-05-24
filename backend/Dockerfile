FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN pip install --upgrade pip
ENV IS_IN_DOCKER true

RUN apt update
RUN apt-get install -y default-jdk

WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY ./app ./
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

CMD uvicorn main:app --host localhost --port 8800

