test:
	OPBEAT_DISABLE_SEND=true ./manage.py test

runserver:
	OPBEAT_DISABLE_SEND=true ./manage.py runserver
