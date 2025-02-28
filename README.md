PYTHON 3.11 MAXIMO
TENSORFLOW=2.15.0


EN SERVIDOR

sudo apt install npm

sudo npm install pm2 -g

pm2 start "uvicorn src.main:app --host 0.0.0.0" --name api

docker pull postgres:16.0

docker run --name cofradia_db -e POSTGRES_DB=cofradia_db -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16.0