FROM python:3

WORKDIR /usr/src/app

EXPOSE 5000

COPY . .

RUN pip install --no-cache-dir .


CMD [ "make", "run" ]