### Instalation

```pip install poetry```

Then activate virtual environment and install dependencies
```poetry init```
```poetry install```
```poetry shell```

### Run Django aplications and init cronjob task

```python bbcscraper/manage.py migrate```
```python bbcscraper/manage.py createsuperuser```

#### Run crontab task
```python bbcscraper/manage.py crontab add```

#### Run Django dev server
```python bbcscrapper/manage.py runserver```