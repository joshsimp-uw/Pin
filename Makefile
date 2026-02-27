PORT ?= 8000
SERVICE ?= pin

.PHONY: prep install demo-reset update health rotate-master-key

prep:
	bash ./scripts/pin-git-push-prep.sh

install:
	sudo bash ./scripts/install.sh

demo-reset:
	sudo bash ./scripts/pin-reset-bootstrap.sh

update:
	@echo "Updating Pin..."
	@git pull || { echo "Git pull failed"; exit 1; }

	@if [ -f "/etc/pin/pin.env" ]; then \
		sudo grep -qE '^\s*TIER1_SECRET_KEY=' /etc/pin/pin.env || echo "WARNING: /etc/pin/pin.env missing TIER1_SECRET_KEY (provider key decryption may fail). Run 'make install' or add it."; \
	fi

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

rotate-master-key:
	@if [ ! -d ".venv" ]; then \
		echo "No virtual environment found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "Rotating TIER1_SECRET_KEY (master encryption key) and re-encrypting stored provider keys..."
	@sudo .venv/bin/python scripts/rotate_master_key.py --env-file /etc/pin/pin.env --sqlite-path data/pin.db