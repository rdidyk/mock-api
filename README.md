# mock-api
Web requests mocking service (Prototype)

#### launch development version of web service:
* Create (or activate) virtualenv with python3.6
* Install app requirements: `$ pip install -r requirements.txt -r requirements_dev.txt`
* Set Flask env. variables: 
    * `$ export FLASK_APP=mockapi/app.py`
    * `$ export FLASK_ENV=development`
* Run DB migrations: `$ flask db upgrade`
* Run service: `$ flask run`

### TODO:
* Add tests
* Add swagger schema validation
* Add mocked URL hits, counters and other useful metrics
* Add more features =)
