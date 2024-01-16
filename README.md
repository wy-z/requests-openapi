# requests-openapi

[![image](https://img.shields.io/pypi/v/requests-openapi.svg)](https://pypi.org/project/requests-openapi/)
[![image](https://img.shields.io/pypi/l/requests-openapi.svg)](https://pypi.org/project/requests-openapi/)
[![image](https://img.shields.io/pypi/pyversions/requests-openapi.svg)](https://pypi.org/project/requests-openapi/)
[![image](https://raw.githubusercontent.com/wy-z/requests-openapi/master/tests/coverage-badge.svg)](https://github.com/wy-z/requests-openapi)

A lightweight but powerful and easy-to-use Python client library for OpenAPI v3.

## Key Features

- **Lightweight Design**: Experience a minimalistic interface.
- **Focus on Essentials**: Helps you simplify the handling of Paths, Parameters, Headers, Cookies, etc., while inheriting all the capabilities of Requests.
- **Testing and Integration Made Easy**: Whether you're running tests or integrating with other systems, the client simplifies these tasks.

## Usage

```python
import requests_openapi

# load spec from url
c = requests_openapi.Client().load_spec_from_url("https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml")
# or load from file
c = requests_openapi.Client().load_spec_from_file("openapi.json")
# set server
c.set_server(requests_openapi.Server(url="https://fake.com/api"))

# custom session for auth or others
c.requestor # a instance of requests.Session, see https://requests.readthedocs.io/en/latest/user/advanced/#session-objects
# set update token
c.requestor.headers.update({"Authorization": "token"})

# call api by operation id
resp = c.listPets() # resp: requests.Response
resp.json()
# get by path id
resp = c.showPetById(petId=1)
resp.json()
# post
resp = c.createPets(json={})
resp.json()

#
# Advanced Usage
#

# set req options, 'req_opts' param to custom request options
requests_openapi.Client(req_opts={"timeout": 60}).load_spec_from_file("xx")

# parameters starts with '_' or not found in openapi spec, will be passed through to the requesting
c.createPets(json={}, _headers={}, _params={}, _cookies={})

# parameters
# in: cookie, name: csrftoken
c.createPets(csrftoken="***")
# in: header, name: x-foo
c.createPets(**{"x-foo": "***"})
# in: path, name: userId
c.getUser(userId=1)
# in: query, name: offset
c.listUsers(offset=1)

# http body, just like requests.Session
c.createPets(json={}) or c.createPets(data={})
```

## Installation

```
pip install requests-openapi
```

## License

MIT
