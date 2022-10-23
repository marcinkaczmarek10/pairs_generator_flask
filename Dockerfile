FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /pairs_generator_flask

RUN apt update -y && apt install -y build-essential libpq-dev

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./entrypoint.sh .

COPY . .

ENTRYPOINT ["sh", "/pairs_generator_flask/entrypoint.sh"]
