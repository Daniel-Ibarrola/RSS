Commands for autostarting script
================================

First create a service file using the template and put it in

`/etc/systemd/system/<FILE-NAME>.service`

Then, run this command after creating the file
```bash
sudo systemctl daemon-reload
```

Enable the service with the following command
```bash
sudo systemctl enable <YOUR-NAME>.service
```

And finally start the service.
```bash
sudo systemctl start <YOUR-NAME>.service
```

### Other useful commands are:

Restart process
```bash
sudo systemctl restart <YOUR-NAME>.service
```

Stop process
```bash
sudo systemctl stop <YOUR-NAME>.service
```

Status
```bash
sudo systemctl status <YOUR-NAME>.service
```

Disable autostart
```bash
sudo systemctl disable <YOUR-NAME>.service
```

Check logs
```bash
journalctl -u <YOUR-NAME>.service
```