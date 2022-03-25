ssh:
	docker-compose run --rm -p 8000:8000 web bash

up:
	docker-compose up

migrations:
	docker-compose run --rm web python manage.py makemigrations

migrate:
	docker-compose run --rm web python manage.py migrate

createsuperuser:
	docker-compose run --rm web python manage.py createsuperuser

test:
	docker-compose run --rm web python manage.py test

startapp:
	docker-compose run --rm web python manage.py startapp $(app)
