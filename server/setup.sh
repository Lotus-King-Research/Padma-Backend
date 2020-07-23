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

sudo systemctl nginx stop
sudo sed "s/_IP_/$IP/" server/nginx.conf > /etc/nginx/nginx.conf
sudo systemctl nginx start

# install docker
sudo apt-get update -y

sudo apt-get install \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg-agent \
  software-properties-common -y

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update -y
sudo apt-get install docker-ce docker-ce-cli containerd.io -y

sudo docker login docker.pkg.github.com --username mikkokotila --password ${{ secrets.MIKKOKOTILA_TOKEN }}
sudo docker pull docker.pkg.github.com/mikkokotila/padma/core_api:master
NEW_IMAGE_ID=$(sudo docker images | grep core_api | tail -1 | tr -s ' ' | cut -d ' ' -f3)
sudo docker stop $CURRENT_IMAGE_ID
sudo docker run --restart unless-stopped -p 5000:5000 $NEW_IMAGE_ID
echo $NEW_IMAGE_ID > current_image_id.txt