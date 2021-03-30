FROM python:3.8-slim-buster
WORKDIR /app
COPY app .
COPY requirements.txt ./requirements.txt

#opencv fix https://stackoverflow.com/questions/55313610/importerror-libgl-so-1-cannot-open-shared-object-file-no-such-file-or-directo
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
#end

RUN pip3 install -r requirements.txt
EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
