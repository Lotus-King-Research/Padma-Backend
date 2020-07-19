ssh -i ~/.ssh/padma.pem ubuntu@3.120.34.196

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo apt-get install nginx -y
sudo apt-get install python3-pip -y
sudo apt-get install git
sudo apt-get install enchant
sudo apt-get install unzip
sudo apt-get install wget

git clone https://github.com/mikkokotila/Padma.git
cd Padma
pip3 install -r requirements.txt
python3 -m spacy download en

sudo reboot
