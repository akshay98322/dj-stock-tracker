docker run -p 6379:6379 --name redis redis
celery -A stock_project.celery worker --pool=solo -l info
celery -A stock_project beat -l INFO
python manage.py runserver
pip install -r requirements.txt