# Lunch-roulette

The application comes with two configurations: a development configuration (which corresponds to the `docker-compose.yml` file) and a deployment configuration (which corresponds to the `docker-compose-deploy.yml` file).

The application consists of the following folders:
- `app` contains the back-end and the front-end;
- `demons` contains the cron job for the random event generator and emails sending;
- `proxy` contains a reverse-proxy used in the deployment configuration to more efficiently serve static files.

## Random event generator and emails sending

The configuration and the interval of the execution of the demon is placed in the `demons/app/config/settings.py` file and for the development configuration the emails are not sent but printed in the console as show as follow:
```
CRONJOBS = [
    ('0 15 * * 0', 'core.demons.random_event')
]
if DEBUG:
    CRONJOBS = [
        ('*/15 * * * *', 'core.demons.random_event')
    ]

EMAIL_BACKEND = (
    'django.core.mail.backends.console.EmailBackend'
    if DEBUG else
    'django.core.mail.backends.smtp.EmailBackend'
)
```
The `core.demons.random_event` code is placed in the `demons/app/core/demons.py` file.

## `.env` file

The file `.env` is required for the deployment configuration in order to be able to access the database and to send email. An example of this file can be found in the project root directory and is called `.env.sample`.

## Build, run and access

To build and run the application run the command `docker-compose up --build`. The application has three URLs:

- `http://localhost:8000` is the front end;
- `http://localhost:8000/api/docs` is the api documentation;
- `http://localhost:8000/admin` is the administrative panel.

In the front-end it's possible to register to access the application but it's not possible to access the admin panel. To access the admin panel is required a user created with the command `docker-compose run --rm app sh -c "python manage.py createsuperuser"`. After this user it's possibile to enable other users to access the admin panel from the user manager inside the admin panel itself.

The parameters: days of the week, lunch break time and number of colleagues can be set in the Settings section of the admin panel. The default settings is set to:

- days of the week: wednesday
- lunch break time: 13:00-14:00
- number of colleagues: 5

## Good to know

It's possibile to run unit test with the command `docker-compose run --rm app sh -c "python manage.py test"` and it's also possible to run linting tool with the command `docker-compose run --rm app sh -c "flake8"`.

## Improvements

- Try to find a way to not use root user in demons service or improve security using user roles offered by Django.
- Add a bunch of logs.