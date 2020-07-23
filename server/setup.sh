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

wget -qq --show-progress https://goo.gl/GyTv7n -O /tmp/dictionaries.zip
unzip -qq -o /tmp/dictionaries.zip -d /tmp

wget -qq --show-progress https://github.com/mikkokotila/Rinchen-Terdzo-Tokenized/raw/master/docs/docs.zip -O /tmp/docs.zip
unzip -qq -o /tmp/docs.zip -d /tmp/docs/

wget -qq --show-progress https://github.com/mikkokotila/Rinchen-Terdzo-Tokenized/raw/master/tokens/tokens.zip -O /tmp/tokens.zip
unzip -qq -o /tmp/tokens.zip -d /tmp/tokens

sudo cp ./server/Padma.service /etc/systemd/system/Padma.service
sudo sed "s/_IP_/$IP/" server/nginx.conf > /etc/nginx/nginx.conf

sudo systemctl daemon-reload
sudo systemctl start Padma
sudo systemctl status Padma