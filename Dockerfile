FROM python:3.11

RUN apt-get update && apt-get install -y \
    libgl1-mesa-dev

WORKDIR /

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]