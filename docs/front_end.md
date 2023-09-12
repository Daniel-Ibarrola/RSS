# Building the front end 

Build the front end app. 

```shell
npm run build
npm run preview
```

Copy the dist folder to `/var/www/<site-name>`

Change the owner of the directory of the site. Example:

```shell
sudo chown -R testuser:testuser /var/www/<site-name>
```
