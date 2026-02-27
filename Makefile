PORT ?= 8000
SERVICE ?= pin

.PHONY: prep install demo-reset update health

prep:
	bash ./scripts/pin-git-push-prep.sh

install:
	sudo bash ./scripts/install.sh

demo-reset:
	sudo bash ./scripts/pin-reset-bootstrap.sh

update:
	@echo "Updating Pin..."
	@git pull || { echo "Git pull failed"; exit 1; }

	@if [ ! -d ".venv" ]; then \
		echo "No virtual environment found. Run 'make install' first."; \
		exit 1; \
	fi

	@echo "Installing requirements..."
	@. .venv/bin/activate && pip install -r requirements.txt || { echo "pip install failed"; exit 1; }

	@echo "Restarting service..."
	@sudo systemctl restart $(SERVICE) || { echo "Service restart failed"; exit 1; }

	$(MAKE) health

health:
	@echo "Checking health on port $(PORT)..."
	@curl -fsS http://localhost:$(PORT)/health && echo "\nOK" || { echo "Health check failed"; exit 1; }