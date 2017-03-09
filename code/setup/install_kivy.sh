# Install Kivy environment on Vanilla Linux Mint 17.2 x64
sudo apt-get update
# install python/pip
sudo apt-get install python -y
sudo apt-get install python-pip -y
sudo pip install --upgrade pip
#sudo pip uninstall Cython
sudo pip install -I Cython==0.23
sudo add-apt-repository ppa:kivy-team/kivy -y
sudo apt-get update
#python2
sudo apt-get install python-kivy -y
#python3
# sudo apt-get install python3-kivy -y
#Optional Examples
# sudo apt-get install kivy-examples -y
