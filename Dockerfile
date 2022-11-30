From 3.12.0a2-slim-buster

WORKDIR /app 

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ec/ .
COPY media/ .
CMD ["python3","manage.py","runserver","0.0.0.0:8000"]