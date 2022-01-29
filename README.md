# wallstreet-chatbot

**Team Name**: Array of Hope

## Team members:

- [Mufaddal Diwan](https://github.com/mufaddal12)
- [Kirti Palve](https://github.com/kirtipalve)
- [Ilyas Ali](https://github.com/ilyas-ali)

## Running the app:

### Terminal 1

- `virtualenv env -p python3.8`
- `source env/bin/activate`
- `pip install -r requirements.txt`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py shell`
  - `from trading.utility import add_company`
  - `add_company("")`
  - `exit()`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py collectstatic`
- `python manage.py runserver`

### Terminal 2

- `redis-server`

### Terminal 3

- `celery -A wallstreet_chatbot worker --pool=eventlet -l info`

### Terminal 4

- `celery -A wallstreet_chatbot beat -l info`
