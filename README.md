# CAP RSS feed

Publish CAP alerts to RSS feed SASMEX's channel. This repository consists of a REST API to 
post and get CAP alerts, as well as the "CAP Generator" program that actively listens for
seismic events, and creates and posts alerts whenever such an event occurs.


## Installation

### API

Before installing make sure to modify the api.env file with the proper values.

The api can be installed manually or run in docker. Next, the steps for both types of
installation are detailed.

#### On docker

First clone the repository:

```shell
git clone https://github.com/Daniel-Ibarrola/RSS
cd RSS
```

To install and run the API on docker simply run the following commands:

```shell
make build
make api
```

Check the logs to see everything is working as expected:

```shell
make logs
```

Also, check [configuring Nginx](docs/nginx.md) if necessary.

#### Manual Installation

The manual installation consists og the following steps:

1. [Set up PostgreSQL](docs/postgresql.md)
2. [Run the API with systemd](docs/api_systemd.md)
3. [Configure Nginx](docs/nginx.md)

### Cap generator

First clone the repository:

```shell
git clone https://github.com/Daniel-Ibarrola/RSS
cd RSS
```

Use docker to run the cap generator program:

```shell
make build
make generator
```

## Developing

### On docker

Start the development server on docker. This is necessary before running
the tests.

```shell
make build
make dev
```

Now you can run the tests in another terminal. You can run all test, only unit tests
or also E2E2 test.

```shell
make test
make unit-tests
make e2e-tests
```

### Testing the cap generator program

Although there are automated E2E tests for the cap generator, it may be a good idea to do some manual
tests. You can start the cap generator program on docker as well as a test simulation server to produce
alerts. Use the following commands:

```shell
make dev-generator
```

Now check that the cap generator is posting new alerts to the API.


## API Documentation

...