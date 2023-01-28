FROM python:3.9.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt update -y && apt install -y build-essential libpq-dev
RUN pip install --upgrade pip 

RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

CMD ["uvicorn" , "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
