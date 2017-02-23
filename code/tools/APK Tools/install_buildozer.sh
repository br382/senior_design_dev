# Install Buildozer enviroment on Vanilla Mint 18.1 x64
sudo apt-get install python-pip -y
sudo pip install --upgrade pip
sudo pip install setuptools
sudo pip install --upgrade setuptools
sudo pip install buildozer
# Required for Buildozer's compiling/packaging sequence:
sudo apt-get install python-pip python-dev libxml2-dev libxslt1-dev zlib1g-dev -y
#sudo pip uninstall Cython -y
sudo pip install -I Cython==0.23
sudo apt-get install build-essential -y
sudo apt-get install default-jdk -y
