FROM nikolaik/python-nodejs:latest

WORKDIR /backend/app
COPY backend/app .
COPY backend/requirements.txt ./requirements.txt

ENV IS_IN_DOCKER=true

RUN pip3 install -r requirements.txt
RUN pip3 install -r ./custom_model/custom_requirements.txt

# set working directory
WORKDIR /frontend/app

# add `/app/node_modules/.bin` to $PATH
ENV PATH frontend/app/node_modules/.bin:$PATH
ENV IS_IN_DOCKER true

# install app dependencies
COPY ./frontend/package.json ./
COPY ./frontend/package-lock.json ./
RUN npm install --silent
RUN npm install react-scripts@3.4.1 -g --silent

# add app
COPY ./frontend ./
# start app

CMD ["npm", "start"]
CMD uvicorn main:app --host 0.0.0.0 --port 8800
