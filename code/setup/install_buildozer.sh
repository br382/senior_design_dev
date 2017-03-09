# Install Buildozer enviroment on Vanilla Mint 17.2 x64
sudo apt-get install git -y
sudo apt-get install python-pip -y
sudo pip install -U pip
sudo pip install -U setuptools
sudo pip install --upgrade buildozer
#my_dir="$(pwd)"
#cd $HOME
#git clone https://github.com/kivy/buildozer.git
#cd buildozer
#sudo python setup.py install
#cd ..
#sudo rm -rf ./buildozer/
#cd $my_dir
#cd ..
# Required for Buildozer's compiling/packaging sequence:
sudo apt-get install python-pip python-dev libxml2-dev libxslt1-dev zlib1g-dev -y
#sudo pip uninstall Cython -y
sudo pip install -I Cython==0.23
sudo apt-get install build-essential -y
sudo apt-get install default-jdk -y

#Fixing Permissions For Buildozer Files
sudo chmod 777 -R $HOME/.buildozer
