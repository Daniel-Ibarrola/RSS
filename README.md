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

```shell
    python -m venv venv # create a virtual environment
    source venv/bin/activate
    pip install -r requirements.txt
    cd src
    python setup.py develop
```

2. Create a container to run the flask app
```shell
docker compose build
docker compose up -d
```

3. Run the tests to make sure everything's okay

```shell
 pytest      
```

### Manual testing

To test the app, the package includes a server for testing. The server simulates 
receiving alerts which then forwards to the client in the main module.

After following the previous instructions perform the following steps to test the main 
module manually. On another terminal insert the following commands:

```shell
source venv/bin/activate
cd tests/e2e
python server.py
```

Run the main module in another terminal
```shell
source venv/bin/activate
cd tests/e2e
python server.py
```

Each time the server emits an alert a CAP file should be written to the `feeds`
directory.

## Installation

The following section will cover how to install the app for production. Before installing
the app make sure PostgreSQL is installed.

First get the package from GitHub and install in the server.

```shell
    git clone https://github.com/Daniel-Ibarrola/RSS
    python3.10 -m venv venv # create a virtual environment
    source venv/bin/activate
    pip install -r requirements.txt
    cd src
    python setup.py develop
```

Create a file called .env and save it in the root directory. In this
file declare all the environment variables necessary for the app to run.
Use the file in `deploy_tools/rss.template.env` as a guide.

Now install the main module as a service. Copy the service file 
from `deploy_tools/rss_sasmex.service`. The WorkingDirectory and ExecStart may
need to be modified.

```shell
cp deploy_tools/rss_sasmex.service /etc/systemd/system/rss_sasmex.service
sudo systemctl daemon-reload
sudo systemctl start rss_sasmex.service
```

Check that it is working correctly.

```shell
sudo systemctl status rss_sasmex.service
```

### Installing the API

#### Configuring PostgreSQL

Create the appropiate roles and databases in PostgreSQL. First connect
to postgre with the default user.

```shell
sudo -u postgres psql
```

Creating a role and a database

```sql
CREATE ROLE dba 
CREATEDB 
LOGIN 
PASSWORD 'Abcd1234';

CREATE DATABASE database_name
WITH
   OWNER = role_name;
```

#### Creating the .env file

Create a file called .env and save it in the root directory. In this
file declare all the environment variables necessary for the app to run.
Use the file in `deploy_tools/api.template.env` as a guide.


#### Upgrade database

Apply migrations to the database. 

Copy the .env file and create a new file called env.sh. Add an export statement
to each variable, also add the FLASK_APP variable. Example

```shell
export CONFIG=prod 
export FLASK_APP=rss/api/app.py
```

Source the new scripts
```shell
source env.sh
```

Run the database migrations
```shell
flask db upgrade
```

#### Configure gunicorn

Check that the app can start with no issues.

```shell
source venv/bin/activate
cd src/rss/api/
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

Install the api to run as a service. Check the file in `deploy_tools/rss_api.service`, modify
any parameters necessary and then copy it to `/etc/systemd/system/` and then enable the service.


```shell
cp deploy_tools/rss_api.service /etc/systemd/system/rss_api.service
sudo systemctl daemon-reload
sudo systemctl start rss_sasmex.service
```

Check that it is working correctly.

```shell
sudo systemctl status rss_api.service
```

#### Configuring nginx

Modify the template nginx configuration file in `deploy_tools/nginx.template.conf`,
create a new server block and copy the config file there.

```shell

sudo cp deploy_tools/nginx.template.conf /etc/nginx/sites-available/rss
```

To enable the Nginx server block configuration you’ve just created, link the file to the sites-enabled directory:

```shell
sudo ln -s /etc/nginx/sites-available/rss /etc/nginx/sites-enabled
```

With the file in that directory, you can test for syntax errors:

```shell
sudo nginx -t
```

```shell
sudo systemctl restart nginx
```
