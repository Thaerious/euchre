## Start Here
* Use "source ./venv/bin/activate" on new terminals.
* On fresh repos, don't forget to install the local module with 'pip install -e .'

## Running tests
### Run all tests
pytest

### Run specific test with 
pytest tests/test_name.py

## Running tests w/ coverage
### Install pytest and coverage.py
pip install pytest coverage

### Run tests with coverage
coverage run -m pytest

### View a detailed text report
coverage report

### View an HTML report
coverage html

### Handy test flags
-x exit on fail
-k run test names
-v verbose
-s print stdout