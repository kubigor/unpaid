FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y \
        libpq-dev \
        gcc

COPY requirements.txt /app/

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

# RUN python manage.py collectstatic --noinput

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
