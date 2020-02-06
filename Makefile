.DEFAULT_GOAL := all
.PHONY := docker_stop docker_start docker_down django_manage django_migration check_env

dockerc := docker-compose -f docker/docker-compose.yml
pgsql_env := pgsql-variables.env
rmq_env := rmq_variables.env
manage := manage.py

all: check_env docker_start django_migration

check_env: docker/pgsql-variables.env.dist docker/rmq/rmq_variables.env.dist
	@echo "Check docker env files..."
	@test ! -f 'docker/${pgsql_env}' && (echo 'Copy file ...'; cp -v docker/${pgsql_env}.dist docker/${pgsql_env}) || echo 'File '${pgsql_env} 'exists.'
	@test ! -f 'docker/rmq/${rmq_env}' && (echo 'Copy file ...'; cp -v docker/rmq/${rmq_env}.dist docker/rmq/${rmq_env}) || echo 'File '${rmq_env} 'exists.'

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
	$(dockerrc) exec web python ${manage}

django_migration:
	@echo 'Do migrations'
	$(dockerc) exec web python ${manage} migrate

