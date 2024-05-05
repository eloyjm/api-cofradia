PYTHON 3.11 MAXIMO
TENSORFLOW=2.15.0


EN SERVIDOR

sudo apt install npm

sudo npm install pm2 -g

pm2 start "uvicorn src.main:app --host 0.0.0.0" --name api