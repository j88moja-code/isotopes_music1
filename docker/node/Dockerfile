FROM node:18-alpine

WORKDIR /app/

ENV PATH /app/node_modules/.bin:$PATH

COPY frontend/package.json /app/package.json
RUN npm install --silent \
    && npm install react-scripts@3.0.1 -g --silent

COPY . /app/
