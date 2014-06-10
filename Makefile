all: test

export SQLALCHEMY_DATABASE_URI:=mysql://root@localhost/bong_db_local

test: unit functional

prepare:
	@pip install -q curdling
	@curd install -r development.txt

clean:
	@git clean -Xdf # removing files that match patterns inside .gitignore

unit:
	@python manage.py unit

functional: db
	@python manage.py functional

acceptance:
	@python manage.py acceptance

shell:
	python manage.py shell

run:
	python manage.py run

check:
	python manage.py check


migrate-forward:
	@[ "$(reset)" == "yes" ] && echo "drop database if exists bong_db_local;create database bong_db_local" | mysql -uroot || echo "Running new migrations..."
	@alembic upgrade head

migrate-back:
	@alembic downgrade -1

db:
	echo "drop database if exists bong_db_local;create database bong_db_local" | mysql -uroot
	python manage.py db

docs:
	markment -t .theme spec
	open "`pwd`/_public/index.html"

prod-simulation:
       PYTHONPATH=`pwd` PORT="4000" DOMAIN="0.0.0.0" REDIS_URI="redis://localhost:6379" gunicorn --worker-class bong.upstream.WebsocketsSocketIOWorker bong.server:application

static:
	bower install
	python manage.py assets build
