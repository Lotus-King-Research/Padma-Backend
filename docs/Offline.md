# Offline

There are several options for running Padma on your local machine (or network) locally. The below method is intended for development purpose, and not recommend for regular users. A fully feautured desktop version of Padma will be available in the coming months.

## Development 

```
# get the package
git clone https://github.com/mikkokotila/Padma.git

# install packages
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo apt-get install nginx -y
sudo apt-get install python3-pip -y
sudo apt-get install git
sudo apt-get install enchant
sudo apt-get install unzip
sudo apt-get install wget

# install depedencies
cd Padma
pip3 install -r requirements.txt

# run (for development)
FLASK_APP=app.py FLASK_ENV=development flask run
