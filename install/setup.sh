echo Installing required packages for Hectormon
echo
sudo apt-get install mysql-server libmysqlclient-dev
sudo pip install virtualenv
cd ..
virtualenv venv
. venv/bin/activate
sudo pip install -r install/requirements.txt
mysql -u root -p
CREATE DATABASE hectormon;
USE hectormon;
CREATE TABLE users(id INT(11) AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), username VARCHAR(50), password VARCHAR(100), email VARCHAR(100));
INSERT INTO users(name, username, password, email) VALUES("pi", "pi", "$5$rounds=535000$.DcUjnndDkb/7cuu$.unepNcvNr5G5MPEK9uMf2xsNOXR.I/OieQWmIH9zg3","");
exit
echo
echo Installation complete; created default website login: user pi  password: hectormon123!
