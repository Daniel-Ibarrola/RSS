# CAP RSS feed

Publish CAP alerts to RSS feed SASMEX's channel. This repository consists of a REST API to 
post and get CAP alerts, as well as the "CAP Generator" program that actively listens for
seismic events, and creates and posts alerts whenever such an event occurs.


## Installation

### Web client + REST API 

First clone this repository:

```shell
git clone https://github.com/Daniel-Ibarrola/RSS.git
```
Modify the .env file located in `services/cap-api/.env` with the appropriate credentials.
Also, create a .env file in `services/client/.env` with the following env variable `VITE_MAPS_API_KEY`, 
with the value of the Google Maps API key.

To install the web client and REST API simply run:

```shell
make prod-web
```

This will create three docker containers: one for the database necessary to store
the cap alerts, another for the REST API, and another one that uses nginx to host the
website.

### Obtaining an SSL certificate

To enable https, a ssl certificate must be obtained, to obtain the certificate run the following
commands:

```shell
make ssl-certificate
```

This will run certbot and generate a certificate. Finally, nginx config must
be updated to accept https traffic. To do that run:

```shell
make nginx-https
```

The website should be up and running over https. Finally, to restore the database
from a snapshot run the following (assuming that the snapshot file is called db.dump):

```shell
docker cp db.dump rss-db:/db.dump \ 
&& docker compose exec postgres pg_restore -U rss -d rss db.dump
```

### CAP Generator

Modify the .env file located in `services/cap-gen/.env` with the appropriate credentials.
To start the service run:

```shell
make generator
```

## Developing

### Web client + REST API 

First clone this repository:

```shell
git clone https://github.com/Daniel-Ibarrola/RSS.git
```

Run the development environment:

```shell
make web-dev
```

This will create three containers: one for the database necessary to store
the cap alerts, another for the flask development server for the REST API, 
and another with the vite development server for the client.

### CAP Generator

Run the cap generator as well as the testing server with:

```shell
make generator-dev
```

### Testing production configuration locally

Before running in production you can test that everything works locally by running the containers
with the following command:

```shell
make prod-http
```

This will create a very similar configuration to the one with `make prod-web`, the difference is that
the nginx server will only listen for http traffic in port 80.

## Testing

### API

Run unit and integration tests with the following commands:

```shell
make api-unit-tests
make api-integration-tests
make api-tests # runs unit and integration tests
```

### Client

To run the client test, use the following command:

```shell
make client-tests
```

This will run vitest in watch mode.

### CAP generator

To run unit tests, use the following command:

```shell
make cap-gen-tests
```
