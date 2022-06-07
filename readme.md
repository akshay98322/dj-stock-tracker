docker run -p 6379:6379 --name redis-service redis
celery -A stock_project.celery worker --pool=solo -l info
celery -A stock_project beat -l INFO

pip install -r /requirements.txt