# SVANGO


## START SERVER FROM DOCKER
```bash
docker build -t svango .
docker run --name svango -p 8000:8000 -d svango
```

## START LOCALLY
* install [poetry](https://python-poetry.org/docs/#installation) 
```bash
poetry install --with utils
`poetry env activate`
./manage.py migrate
./manage.py runserver 8000
```

## ADD DEMO DATA
```bash
./manage.py populate_db -s admin
```

## LOGIN/TOKEN
* get [jwt token](http://127.0.0.1:8000/api/v1/actors/token-obtain/) 
* session [login](http://localhost:8000/actors/users/login/) 


## REST API
* explore [API](http://localhost:8000/api/v1/) 
* explore [Admin panel](http://localhost:8000/admin/)


## API SCHEMA
* swagger [API](http://localhost:8000/api/v1/schema/swagger-ui) 
* redoc [API](http://localhost:8000/api/v1/schema/redoc) 
* as json [API](http://localhost:8000/api/v1/schema/?format=json) 
* as file [API](http://localhost:8000/api/v1/schema/) 


## LINT
```bash
ruff check .
ruff check --select E301,E305,E303,E501 --preview .
 ```

## TESTS
```bash
DJANGO_ENV=TESTING py.test -s --cov . --cov-report=term-missing --cov-fail-under=100 --no-cov-on-fail --tb long
```
