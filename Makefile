.PHONY: all setup deploy clean re ssh

# Cargar configuración de cloud.cfg si existe
-include cloud.cfg
export

all: setup deploy

setup:
	@bash update_hosts.sh
	@bash setup_env.sh

deploy:
	@if [ ! -f .env ]; then echo "❌ Falta .env. Ejecuta 'make setup' primero."; exit 1; fi
	@if [ ! -f cloud.cfg ]; then echo "❌ Falta cloud.cfg. Copia cloud.cfg.example y rellena tus datos."; exit 1; fi
	ansible-playbook -i ansible/hosts ansible/site.yml

ssh:
	@if [ ! -f cloud.cfg ]; then echo "❌ Falta cloud.cfg. Copia cloud.cfg.example y rellena tus datos."; exit 1; fi
	@. ./cloud.cfg && gcloud compute ssh "$${SSH_USER}@$${GCP_INSTANCE}" --project="$${GCP_PROJECT}" --zone="$${GCP_ZONE}"

clean:
	sudo docker-compose down -v 2>/dev/null || true
	rm -f .env

re: clean all
