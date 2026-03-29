run:
	python3 manage.py makemigrations business
	python3 manage.py makemigrations
	python3 manage.py migrate