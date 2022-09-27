build-env:
	@python3 -m venv .venv && \
	source .venv/bin/activate && \
	python3 -m pip install --upgrade pip setuptools && \
	python3 -m pip install -r requirements/requirements.txt

## Build virtualenv for development with jupyter notebook support
build-env-note:
	@python3 -m venv .venv-note && \
	source .venv-note/bin/activate && \
	python3 -m pip install --upgrade pip setuptools && \
	python3 -m pip install -r requirements/requirements.txt && \
	python3 -m pip install -r requirements/requirements-notebook.txt
