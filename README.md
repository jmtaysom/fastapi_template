# Fastapi Template
This is a template for creating a FastAPI application with 
logging and a database connection setup.


## Running the server
1. Run `uvicorn main:app --reload` from the app directory
1. Use the pycharm runtime `uvicorn` to start up the application


## Installation
1. Ensure you have python3.9 installed `python3 --version` or
`python3.9 --version`
1. Install pipenv (preferably with pipx)
    1. `python3 -m pip install pipx`
    1. `pipx install pipenv`
1. `pipenv install --dev` from the mercury directory
1. `pre-commit install`
1. `pre-commit run --all-files`
1. (Optional) in Pycharm -> Preferences -> Project add the venv (found at
`pipenv --venv`)


## Testing
1. Run `pytest` for a basic check
1. Run `pytest --cov=app` to get a coverage report
1. Run `pytest --cov=app --cov-report html` to get a html version of the
report that is navigable.


## Parsing Logs
The logs are stored as json in order to be able to parse them with jq
or pass them to another system in the future. Below are several examples
of how you can parse the logs.
1. Get all logs that are created with the `app.logger.log` functions
`cat logs/app.log | jq 'select(.request_id | contains("None"))`
1. The same as above but get just the message `cat logs/app.log | jq
'select(.request_id | contains("None")) | .message' | jq -r`
1. Get all the http responses created by uvicorn
`tail logs/app.log | jq -r 'select(.name | contains("h11_impl")) | .message'`
