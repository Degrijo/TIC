FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install  --no-cache-dir -r requirements.txt
COPY . /code/
RUN python manage.py makemigrations \
	&& python manage.py migrate \
	&& python manage.py createsuperuser --noinput