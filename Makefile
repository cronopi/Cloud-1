.PHONY: all setup deploy clean re

all: setup deploy

setup:
	@bash setup_env.sh

deploy:
	@if [ ! -f .env ]; then echo "❌ Falta .env. Ejecuta 'make setup' primero."; exit 1; fi
	sudo ansible-playbook -i ansible/hosts ansible/site.yml

clean:
	sudo docker-compose down -v 2>/dev/null || true
	rm -f .env

re: clean all
