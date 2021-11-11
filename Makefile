
.update-pip:
	@python -m pip install --upgrade pip
	@pip install pip-tools
	@touch .update-pip

.develop: .update-pip
	@pip install -r requirements.dev.txt
	@touch .develop

.PHONY: build
build:
	@python setup.py build

.PHONY: clean
clean:
	@rm -rf `find . -name __pycache__`
	@rm -rf `find . -name .hash`
	@rm -f `find . -type f -name '*.py[co]' `
	@rm -rf build
	@python setup.py clean
	@rm -f .develop
	@rm -rf *.egg-info
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache

.PHONY: compile-deps
compile-deps: .update-pip
	pip-compile --allow-unsafe -q --strip-extras \
		requirements.dev.in

.PHONY: fmt format
fmt format:
	python -m pre_commit run --all-files --show-diff-on-failure

.PHONY: install
install:
	@python setup.py install

.PHONY: lint
lint: fmt mypy

.PHONY: mypy
mypy:
	mypy pysegmenttree

.PHONY: test
test: .develop install
	@pytest -v
