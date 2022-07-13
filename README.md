# mock-api
Web requests mocking-api

Web mocking-api can be used for mocking any system you integrate with via HTTP or HTTPS (i.e. services, web sites, etc).  
When mocking-api receives a requests it matches the request against preconfigured  "Mock Endpoints" that have been configured.  
A preconfigured "Mock Endpoint" defines the response which should be returned for specific uri.

----

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
    ```bash
    $ curl -X POST \
        http://localhost:5000/v1/mocks/ \
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
    ```bash
    $ curl -X GET http://localhost:5000/v1/mocks/
    ```

* Get mock by id: 
    ```bash
    $ curl -X GET http://localhost:5000/v1/mocks/1
    ```

* Update existing mock: 
    ```bash
    $ curl -X PUT \
        http://localhost:5000/v1/mocks/2 \
        -H 'content-type: application/json' \
        -d '{
            "response_body": "<h1>Hi!</h1>"
        }'
    ```

* Delete mock: 
    ```bash
    $ curl -X DELETE http://localhost:5000/v1/mocks/2
    ```

* Test mocks:
    ```bash
    $ curl -X GET http://localhost:5000/greeting
    ...
    ...
    $ curl -X GET http://localhost:5000/v1/users/42
    ```

----

#### Example usage inside of pytest:
```python
    import pytest
    import requests


    @pytest.fixture
    def service_url():
        return 'http://localhost:5000'


    @pytest.fixture
    def mock_users_endpoint(service_url):
        resp = requests.post(
            f'{service_url}/v1/mocks/',
            json={
                "items": [
                    {
                        "uri": "/v1/users/42",
                        "title": "get user id: 42",
                        "response_body": {
                            "name": "John Doe",
                            "age": 42
                        }
                    }
                ]
            },
        )
        resp.raise_for_status()
        data = resp.json()
        yield data
        # delete record after tests
        requests.delete(
            f'{service_url}/v1/mocks/{data["created_items"][0]["id"]}'
        )


    def test_get_user_by_id(service_url, mock_users_endpoint):
        user_id = 42
        resp = requests.get(f'{service_url}/v1/users/{user_id}')
        resp.raise_for_status()
        resp_data = resp.json()
        assert resp_data['name'] == 'John Doe'
        assert resp_data['age'] == 42

```
----

### TODO:
* ~Add admin panel~
* Add tests
* Add swagger schema validation
* Add mocked URL hits, counters and other useful metrics
* Add more features =)
