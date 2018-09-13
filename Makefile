clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "*.DS_Store" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name "*.cache" -type d | xargs rm -rf
	@find . -name "*htmlcov" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -f coverage.xml

 test: clean
	nosetests -s --rednose

 coverage: clean
	nosetests --with-coverage --cover-package=pxa

 requirements-dev:
	pip install -r requirements-dev.txt

 run:
	FLASK_ENV=development flask run --reload

 lint: flake8 check-python-import

 flake8:
	@flake8 --show-source .

 check-python-import:
	@isort --check

 isort:
	@isort

 outdated:
	pip list --outdated