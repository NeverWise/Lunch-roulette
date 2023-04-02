# Lunch-roulette

The application comes with two configurations: a development configuration (which corresponds to the `docker-compose.yml` file) and a deploy configuration (which corresponds to the `docker-compose-deploy.yml` file).

app -> back-end and front-end
demons -> demon for sending email
proxy -> deploy static files nginx

demons email settings

The deployment configuration requires a file called `.env` containing the environment variables needed to access the database and to send email. An example of this file can be found in the project root directory and is called `.env.sample`.

To build and run the application it necessary to run the command `docker-compose up --build` or `docker-compose -f docker-compose-deploy.yml up --build` depend of which configuration you want to run.

`docker-compose run --rm app sh -c "python manage.py createsuperuser"`

`http://localhost:8000/api/docs`

Settings in the amministration panel

`.env.sample`

## Good to know

## Improvements

- Try to find a way to not use root user in demons service or improve security using user roles offered by Django.
- Add a bunch of logs.