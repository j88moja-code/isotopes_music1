FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
RUN pip install --upgrade pip
COPY backend/requirements.txt /app/

RUN pip install -r requirements.txt
COPY . /app/