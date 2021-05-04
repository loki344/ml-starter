FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN pip install --upgrade pip
ENV IS_IN_DOCKER true

WORKDIR /ml-starter
COPY ./startBackend.sh ./startBackend.sh
COPY ./startFrontend.sh ./startFrontend.sh
COPY ./startup.sh ./startup.sh

RUN chmod a+x ./startBackend.sh
RUN chmod a+x ./startFrontend.sh
RUN chmod a+x ./startup.sh

WORKDIR /ml-starter/backend
ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN apt update
RUN apt -y install nodejs npm
COPY ./backend ./
RUN pip install -r requirements.txt

WORKDIR /ml-starter/frontend

COPY ./frontend/package.json ./
COPY ./frontend/package-lock.json ./

COPY ./frontend ./
RUN npm install

WORKDIR /ml-starter
CMD ./startup.sh

