# Run API as a service with systemd

The API webserver can be run as a service on Ubuntu with the use of
systemd. Systemd is an ubuntu utility that will take care of starting
the service on boot and in case it crashes or there is an error.

## Install the package

First clone the repository:

```shell
git clone https://github.com/Daniel-Ibarrola/RSS
cd RSS
```

Now create a virtual environment and install dependencies and this package:

```shell
    python3.11 -m venv venv # create a virtual environment
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -e .
```

## Apply migrations

Export environment variables:

```shell
source api.env
```

Now apply migrations

```shell
flask db upgrade
```

## Start gunicorn

Check that the gunicorn server can start with no issues.

```shell
source venv/bin/activate
cd src/rss/api/
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

If everything went well, you can close the gunicorn server and proceed with the next step.

## Run as a service

Install the api to run as a service. Check the file in `deploy_tools/rss_api.service`, modify
any parameters necessary and then copy it to `/etc/systemd/system/` and then enable the service.

```shell
sudo cp deploy_tools/rss_api.service /etc/systemd/system/rss_api.service
sudo systemctl daemon-reload
sudo systemctl start rss_api
```

Check that it is working correctly.

```shell
sudo systemctl status rss_api
```

Finally, enable the service to start on boot:

```shell
sudo systemctl enable rss_api
```
