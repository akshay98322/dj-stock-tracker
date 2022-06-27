
## Run Locally

Clone the project

```bash
  git clone https://github.com/akshay98322/dj-stock-tracker.git
```

Go to the project directory

```bash
  cd stock-project
```
#1. Basic checks to get started with the project

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python manage.py runserver
```
Check if you are able to see the homepage at localhost:8000. Press ctrl+c to stop the server.

#2. Start the core project

Create DB and Tables
```bash
  python manage.py makemigrations
  python manage.py migrate
```
Create superuser
```bash
  python manage.py createsuperuser
```
Start the server
```bash
  python manage.py runserver
```
#3. Set up Redis

Download and run docker desktop in your pc.

Start the redis service in a new terminal
```bash
  docker run -p 6379:6379 --name redis redis
```

#4. Start Celery worker

Start the Celery worker in a new terminal
```bash
  celery -A stock_project.celery worker --pool=solo -l info
```
#5. Start Celery beat

Start the Celery beat in a new terminal
```bash
  celery -A stock_project beat -l INFO
```



