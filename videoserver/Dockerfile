FROM python:3.8-slim
RUN apk update
#RUN apk add make automake gcc g++ subversion python3-dev libffi-dev
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . .
CMD ["python", "main.py"]
