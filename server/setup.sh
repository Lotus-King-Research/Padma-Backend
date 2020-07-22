read IP

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo apt-get install nginx -y
sudo apt-get install python3-pip -y
sudo apt-get install git -y
sudo apt-get install enchant -y
sudo apt-get install unzip -y
sudo apt-get install wget -y

git clone https://github.com/mikkokotila/Padma.git
cd Padma
pip3 install -r requirements.txt
python3 -m spacy download en

sudo cp ./server/Padma.service /etc/systemd/system/Padma.service
sudo sed "s/_IP_/$IP/" server/nginx.conf > /etc/nginx/nginx.conf

sudo systemctl daemon-reload
sudo systemctl start Padma
sudo systemctl status Padma