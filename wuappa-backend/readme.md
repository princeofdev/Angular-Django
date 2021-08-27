# Development Setup

1. Install [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
2. Install Python 3.5.2 using `pyenv install 3.5.2`
3. Create a virtualenv using `pyenv virtualenv 3.5.2 wuappa`
4. Activate virtualenv using `pyenv activate wuappa`
5. Install requirements using `pip install -r requirements.txt`
6. Apply migrations using `python manage.py migrate`
7. Install cities info using `python manage.py loaddata geo_staging`
8. Run dev server using `python manage.py runserver`

# Production Setup

The production deployment is based on this guide: [https://gist.github.com/kasappeal/b54ecf22ca302223fa914d3e355c7c21][https://gist.github.com/kasappeal/b54ecf22ca302223fa914d3e355c7c21]

# Push notificacions

To send push notificacions, you need to add a cron task to execute the script `send_push_notifications.sh`.

It's needed to have a `.env` file that exports, at least, the following environment variables (example):

```
export SECRET_KEY=xxxxxxxxxxxxxxxxxxxxx
export POSTGRES_DB=xxxxxxxxxxxxxxxxxxxxx
export POSTGRES_USER=xxxxxxxxxxxxxxxxxxxxx
export DJANGO_SETTINGS_MODULE=xxxxxxxxxxxxxxxxxxxxx

export STRIPE_TEST_PUBLIC_KEY=xxxxxxxxxxxxxxxxxxxxx
export STRIPE_TEST_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxx
export STRIPE_LIVE_PUBLIC_KEY=xxxxxxxxxxxxxxxxxxxxx
export STRIPE_LIVE_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxx
export STRIPE_LIVE_MODE=True
```

# Configuration variables

| Variable name | Description | 
| ------------- | ------------- | 
| DEFAULT_PROFESSIONAL_FEE | % of professional fee for every service |

# Environment variables

| Variable name | Description | 
| ------------- | ------------- | 
| SECRET_KEY | Secret key to encrypt passwords |
| POSTGRES_DB | Postgres database name |
| POSTGRES_USER | Postgres database user |
| DJANGO_SETTINGS_MODULE | Settings module to be used |
| DEFAULT_FROM_EMAIL | System default from email |
| EMAIL_HOST | SMTP host |
| EMAIL_PORT | SMTP port |
| EMAIL_HOST_USER | SMTP user |
| EMAIL_HOST_PASSWORD | SMTP password |
| EMAIL_USE_TLS | SMTP use TLS (True) or not (False) |
| SMS_USER | SMS gateway user |
| SMS_PASSWORD | SMS gateway password |
| STATIC_URL | Static files URL |
| MANAGER_EMAIL | Platform manager's e-mail |
| ADMIN_EMAIL | Platform admin's e-mail |
| STRIPE_TEST_PUBLIC_KEY | Stripe test public key |
| STRIPE_TEST_SECRET_KEY | Stripe test secret key |
| STRIPE_LIVE_PUBLIC_KEY | Stripe live public key |
| STRIPE_LIVE_SECRET_KEY | Stripe live public key |