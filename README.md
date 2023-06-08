# CAP RSS feed

App to publish CAP alerts to RSS feed SASMEX's channel.

## Requirements

- Python 3.10.6

## Developing

The app consists of a program that listens for the latest alerts
and creates CAP alert file for them, and a flask app that can store
and retrieve the cap alerts in a database.

The first program is located in `src/main.py`. The flask app can be located
in `src/api/app.py`. 

To set up the package for developing use the following steps:

1. Create a virtual environment and install the package.

```bash
    python -m venv venv # create a virtual environment
    source venv/bin/activate
    pip install -r requirements.txt
    cd src
    python setup.py develop
```

2. Create a container to run the flask app
```bash
docker compose build
docker compose up -d
```

3. Run the tests to make sure everything's okay

```bash
 pytest      
```

### Manual testing

To test the app, the package includes a server for testing. The server simulates 
receiving alerts which then forwards to the client in the main module.

After following the previous instructions perform the following steps to test the main 
module manually. On another terminal insert the following commands:

```bash
source venv/bin/activate
cd tests/e2e
python server.py
```

Run the main module in another terminal
```bash
source venv/bin/activate
cd tests/e2e
python server.py
```

Each time the server emits an alert a CAP file should be written to the `feeds`
directory.

## Installation

The following section will cover how to install the app for production. Before installing
the app make sure PostgreSQL is installed.

1. First get the package from GitHub and install in the server.

```bash
    git clone https://github.com/Daniel-Ibarrola/RSS
    python3.10 -m venv venv # create a virtual environment
    source venv/bin/activate
    pip install -r requirements.txt
    cd src
    python setup.py develop
```

2. Now install the main module as a service. Copy the service file 
 from `tools/rss_sasmex.service`. The WorkingDirectory and ExecStart may
 need to be modified.

```bash
cp deploy_tools/rss_sasmex.service /etc/systemd/system/rss_sasmex.service
sudo systemctl daemon-reload
sudo systemctl start rss_sasmex.service
```

3. Check that it is working correctly.

```bash
sudo systemctl status rss_sasmex.service
```

### Installing the API


