FROM python:3

WORKDIR /app

COPY . .

RUN pip install poetry && make install

EXPOSE 8000
EXPOSE 5434

CMD ["make", "start"]
