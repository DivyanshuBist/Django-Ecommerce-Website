From 3.12.0a2-slim-buster
RUN pip install --upgrade pip
WORKDIR /app 

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./ec .

COPY ./entrypoint /

ENTRYPOINT ["sh","/entrypoint.sh"]