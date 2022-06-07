FROM python:3.8-alpine
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . .
CMD ["source", ".env"]
ENV SPOT_MOVING=
CMD ["python", "main.py"]
