echo Installing required packages for Hectormon
echo
pip install virtualenv
cd ..
virtualenv venv
. venv/bin/activate
pip install -r install/requirements.txt
echo
echo Installation complete!
