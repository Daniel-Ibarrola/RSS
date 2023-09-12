# Configuring nginx

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
