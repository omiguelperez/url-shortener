# shortener

## Start project locally

### Run the project with Docker

```bash
export COMPOSE_FILE=local.yml
docker compose build
docker compose up -d
```

### Apply migrations

```bash
docker compose run --rm django python manage.py migrate
```

We are using Postgres.

### Create a superuser to access swagger and the django-admin

```bash
docker compose run --rm django python manage.py createsuperuser
```

Once created access Django admin:

http://localhost:8000/admin/

There you can view the created Short URLs.


## Use the application

Once you are logged in with your superuser you can access Swagger and use the application.

There are three differnet endpoints:

### 1. Generate a shortened URL

Note: In swagger http://localhost:8000/api/docs/#/

Use the endpoint: `/api/url-shortener/generate/`

Send the payload:

```json
{
  "url": "https://en.wikipedia.org/wiki/Genghis_Khan"
}
```

Response:

```json
{
  "url": "https://en.wikipedia.org/wiki/Genghis_Khan",
  "shortened": "1cad2db7-9e4e-459f-b535-9c979c8d768e"
}
```

### 2. Get the real URL from a shortened URL

It'll count +1 views each time you hit this endpoint

Note: In swagger: http://localhost:8000/api/docs/#/

Use the endpoint: `/api/url-shortener/{shortened}/`

e.g. `/api/url-shortened/1cad2db7-9e4e-459f-b535-9c979c8d768e/`

Fill the "shortened url" 1cad2db7-9e4e-459f-b535-9c979c8d768e in the `shortened` field.

Response

```json
{
  "url": "https://en.wikipedia.org/wiki/Genghis_Khan"
}
```

### 3. Get the top N URL 

The top 100 urls with more views.

You can configure this value via an environment variable:

```bash
TOP_N_URLS=100
```

Update the `./.envs/.local/.django` if you want.

Note: In Swagger http://localhost:8000/api/docs/#/

Use the endpoint `/api/url-shortener/top/`

Response 

```json
[
  {
    "title": "Genghis Khan - Wikipedia",
    "views": 5
  },
  {
    "title": "Jujutsu Kaisen - Wikipedia",
    "views": 1
  }
]
```

### Tests

You can run the tests:

```bash
docker compose run --rm django pytest
```

Result:

```
Test session starts (platform: linux, Python 3.11.8, pytest 8.1.1, pytest-sugar 1.0.0)
django: version: 4.2.11, settings: config.settings.test (from option)
rootdir: /app
configfile: pyproject.toml
plugins: anyio-4.3.0, Faker-24.2.0, django-4.8.0, sugar-1.0.0
collected 35 items                                                                                                                                                                                                         

 shortener/users/tests/test_admin.py ✓✓✓✓✓                                                                                                                                                                    14% █▌        
 shortener/users/tests/test_drf_urls.py ✓✓✓                                                                                                                                                                   77% ███████▊  
 shortener/users/tests/test_drf_views.py ✓✓                                                                                                                                                                   23% ██▍       
 shortener/users/tests/test_forms.py ✓                                                                                                                                                                        26% ██▋       
 shortener/users/tests/test_models.py ✓                                                                                                                                                                       29% ██▉       
 shortener/users/tests/test_swagger.py ✓✓✓                                                                                                                                                                    37% ███▊      
 shortener/users/tests/test_tasks.py ✓                                                                                                                                                                        40% ████      
 shortener/users/tests/test_urls.py ✓✓✓                                                                                                                                                                       83% ████████▍ 
 shortener/users/tests/test_views.py ✓✓✓✓✓✓                                                                                                                                                                   60% ██████    
 shortener/urlshortener/tests/test_utils.py ✓✓✓✓                                                                                                                                                              71% ███████▎  
 tests/test_merge_production_dotenvs_in_dotenv.py ✓✓✓✓✓✓                                                                                                                                                     100% ██████████

Results (1.38s):
      35 passed

```

## Project Structure

### Stack
- Django (with Django REST Framework)
- PostgreSQL
- Celery 
- Redis

### Directories

- `compose`: docker-related files
- `config`: django project configs, settings, urls, etc
- `requirements`: python dependendies per environment
- `shortener`: the project dir containing django apps
  - `urlshortener`: our main django app with exposing the shortener feature


### Docker services

If you check the docker compose file (`local.yml`) you'll see those services:

- `django`: the main django app which expose the three endpoints to interact with the URL Shortener.
- `postgres`: out database
- `redis`: for message queueing 
- `celeryworker`: for async task processing
- `flower`: dashboard to see the Celery tasks

The Django app and the Celery workers are independent so they can be scaling independently based on needs.


### Next steps

- More tests for Celery Tasks and Views
- Use a better URL shortener algorithm

