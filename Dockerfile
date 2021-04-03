FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
WORKDIR /app
COPY app .
COPY requirements.txt ./requirements.txt

ENV PORT=$PORT
EXPOSE $PORT
#opencv fix https://stackoverflow.com/questions/55313610/importerror-libgl-so-1-cannot-open-shared-object-file-no-such-file-or-directo
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
#end

RUN pip3 install -r requirements.txt
RUN pip3 install -r ./custom_model/custom_requirements.txt

CMD uvicorn main:app --host 0.0.0.0 --port $PORT
