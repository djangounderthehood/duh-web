build: build-npm
	pip install -r requirements.txt

build-npm:
	npm install

test:
	OPBEAT_DISABLE_SEND=true ./manage.py test

runserver:
	OPBEAT_DISABLE_SEND=true ./manage.py runserver
