# mock-api
Web requests mocking service (Prototype)

#### launch development version of web service:
* Create (or activate) virtualenv with python3.6

* Install app requirements:  
    `$ pip install -r requirements.txt -r requirements_dev.txt`

* Set Flask env. variables: 
    * `$ export FLASK_APP=mockapi/app.py`
    * `$ export FLASK_ENV=development`

* Run DB migrations: `$ flask db upgrade`

* Run service: `$ flask run`

#### Using API:
* Creating of mocks example:
    ```
    curl -X POST \
        http://localhost:5000/v1/mocks/ \
        -H 'cache-control: no-cache' \
        -H 'content-type: application/json' \
        -d '{
            "items": [
                {
                    "uri": "/greeting",
                    "title": "Hi!",
                    "response_body": "<h1>Hello, World!</h1>",
                    "response_type": "text/html"
                },
                {
                    "uri": "/v1/users/42",
                    "title": "User id: 42",
                    "response_body": {
                        "name": "John Doe",
                        "age": 42
                    }
                }
            ]
        }'
    ```
* Get defined mocks collection:
    `curl -X GET http://localhost:5000/v1/mocks/`

* Get mock by id: `curl -X GET http://localhost:5000/v1/mocks/1`

* Update existing mock: 
    ```
    curl -X PUT \
        http://localhost:5000/v1/mocks/2 \
        -H 'content-type: application/json' \
        -d '{
            "response_body": "<h1>Hi!</h1>"
        }'
    ```

* Delete mock: `curl -X DELETE http://localhost:5000/v1/mocks/2`

* Test mocks:
    * `curl -X GET http://localhost:5000/greeting`
    * `curl -X GET http://localhost:5000/v1/users/42`

----

### TODO:
* ~Add admin panel~
* Add tests
* Add swagger schema validation
* Add mocked URL hits, counters and other useful metrics
* Add more features =)
