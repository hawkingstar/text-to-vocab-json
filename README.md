# linear-regression

for comparison, you will have to use pip or conda to install rapidfuzz. You can find out how to online, though you may need to install conda first if you're using it. 

https://github.com/rapidfuzz/RapidFuzz?tab=readme-ov-file#installation

For audio making, you need to get coqui.

https://github.com/rapidfuzz/RapidFuzz?tab=readme-ov-file#installation

You may need to first install 3.11 python because 3.12 doesn't work for TTS. In codepsaces it's like:

sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-distutils -y

And then you make the environment venv

python3.11 -m venv coqui-env
source coqui-env/bin/activate
pip install --upgrade pip
pip install TTS