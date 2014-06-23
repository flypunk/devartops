# Execute as user test from his home directory
```
sudo apt-get install -y python-pip git-core
git clone https://github.com/flypunk/devartops.git
cd devartops
sudo pip install -r requirements.txt
sudo cp log_analyzer.py /etc/init/
sudo service log_analyzer start
```
