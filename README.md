# requests-openapi

[![image](https://img.shields.io/pypi/v/requests-openapi.svg)](https://pypi.org/project/requests-openapi/)
[![image](https://img.shields.io/pypi/l/requests-openapi.svg)](https://pypi.org/project/requests-openapi/)
[![image](https://img.shields.io/pypi/pyversions/requests-openapi.svg)](https://pypi.org/project/requests-openapi/)

RequestsOpenAPI is a python client library for OpenAPI 3.0

## Usage

```python
import requests_openapi

c = requests_openapi.Client()
c.load_from_url("http://petstore.swagger.io/v2/swagger.json")
c.requestor.auth = (user, password) # c.requestor: requests.Session
resp = c.getPetById(petId=1) # resp: requests.Response
resp.json()
```

## Installation

```
pip install requests-openapi
```

## Licennse

MIT
