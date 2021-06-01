FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN pip install --upgrade pip
ENV IS_IN_DOCKER true

RUN apt update
RUN apt-get install -y default-jdk
WORKDIR /ml-starter
COPY ./startBackend.sh ./startBackend.sh
COPY ./startFrontend.sh ./startFrontend.sh
COPY ./startup.sh ./startup.sh

RUN chmod a+x ./startBackend.sh
RUN chmod a+x ./startFrontend.sh
RUN chmod a+x ./startup.sh

RUN sed -i 's/\r$//' ./startBackend.sh
RUN sed -i 's/\r$//' ./startFrontend.sh
RUN sed -i 's/\r$//' ./startup.sh

WORKDIR /ml-starter/backend
ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN apt -y install nodejs npm
RUN npm i npm@latest -g
COPY ./backend ./
RUN pip install -r requirements.txt

WORKDIR /ml-starter/backend/app/custom_model
RUN pip install -r custom_requirements.txt

WORKDIR /ml-starter/frontend

COPY ./frontend/package.json ./
COPY ./frontend/package-lock.json ./

COPY ./frontend ./
RUN npm install

WORKDIR /ml-starter
CMD ./startup.sh

