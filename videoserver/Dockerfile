FROM python:3.8
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 v4l-utils  -y
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . .
CMD ["chmod",  "777", "/dev/video0"]
CMD ["python", "main.py"]