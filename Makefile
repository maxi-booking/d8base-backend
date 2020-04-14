include .docker/.env

.DEFAULT_GOAL := all
.PHONY := docker_stop docker_start docker_down django_manage django_migration check_env test coverage

dockerc := docker-compose -f .docker/docker-compose.yml
pgsql_env := pgsql-variables.env
rmq_env := rmq_variables.env
env := .env
env_test := .env_test
manage := manage.py

all: check_env docker_build docker_start

update: django_update django_migration docker_restart

check_env: .docker/pgsql-variables.env.dist .docker/rmq/rmq_variables.env.dist
	@echo "Check docker env files..."
	@test ! -f '.docker/${pgsql_env}' && (echo 'Copy file ...'; cp -v .docker/${pgsql_env}.dist .docker/${pgsql_env}) || echo 'File '${pgsql_env} 'exists.'
	@test ! -f '.docker/rmq/${rmq_env}' && (echo 'Copy file ...'; cp -v .docker/rmq/${rmq_env}.dist .docker/rmq/${rmq_env}) || echo 'File '${rmq_env} 'exists.'
	@test ! -f '.docker/${env}' && (echo 'Copy file ...'; cp -v .docker/${env}_dist .docker/${env}) || echo 'Docker file '${env} 'exists.'
	@test ! -f 'd8b/settings/${env}' && (echo 'Copy file ...'; cp -v d8b/settings/${env}_dist d8b/settings/${env}) || echo 'File '${env} 'exists.'
	@test ! -f 'd8b/settings/${env_test}' && (echo 'Copy file ...'; cp -v d8b/settings/${env_test}_dist d8b/settings/${env_test}) || echo 'File '${env_test} 'exists.'

docker_restart: docker_stop docker_start

docker_build:
	@echo "Build docker services..."
	$(dockerc) build

docker_start:
	@echo "Start docker services..."
	$(dockerc) up -d

docker_stop:
	@echo "Stop docker services..."
	$(dockerc) stop

docker_down:
	@echo "Stop docker services..."
	$(dockerc) down

django_manage:
	$(dockerc) exec web python ${manage}

django_update:
	$(dockerc) exec web pip install -e .
	$(dockerc) exec web pip install --no-cache-dir -r ./requirements/dev.txt

django_migration:
	@echo 'Do migrations'
	$(dockerc) exec web python ${manage} migrate

django_setup: django_superuser

django_superuser:
	@$(dockerc) exec web python ${manage} createsuperuser --no-input  -email ${DJANGO_SUPERUSER_EMAIL}
	@$(dockerc) exec web python ${manage} changepassword --no-input  -email ${DJANGO_SUPERUSER_EMAIL}

#RUN python manage.py migrate && python manage.py createsuperuser --no-input --email $SUPERUSER_EMAIL --password $SUPERUSER_PASSWORD

coverage:
	pytest  --cov=./ --cov-report html
	${BROWSER} htmlcov/index.html
test:
	@echo 'Start tests'
	tox
