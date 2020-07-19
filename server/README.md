# intialize server

./setup.sh

# setup Padma as systemd service

sudo vim /etc/systemd/system/Padma.service
sudo systemctl daemon-reload
sudo systemctl start Padma
sudo systemctl status Padma

# configure nginx

sudo vim /etc/nginx/nginx.conf
