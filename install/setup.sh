echo Installing required packages for Hectormon
echo
sudo apt-get install mysql-server libmysqlclient-dev
sudo pip install virtualenv
cd ..
virtualenv venv
. venv/bin/activate
sudo pip install -r install/requirements.txt
echo
echo Installation complete!
