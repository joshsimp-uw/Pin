.PHONY: prep demo-reset install nightly health

prep:
	./scripts/pin-git-push-prep.sh

demo-reset:
	sudo ./scripts/pin-reset-bootstrap.sh

install:
	sudo ./scripts/install.sh

nightly:
	sudo ./scripts/pin-nightly-update.sh

health:
	curl -fsS http://127.0.0.1:8000/health && echo "OK"