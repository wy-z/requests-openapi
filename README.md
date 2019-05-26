# oai-request

[![image](https://img.shields.io/pypi/v/oai-request.svg)](https://pypi.org/project/oai-request/)
[![image](https://img.shields.io/pypi/l/oai-request.svg)](https://pypi.org/project/oai-request/)
[![image](https://img.shields.io/pypi/pyversions/oai-request.svg)](https://pypi.org/project/oai-request/)

OAIRequest is a python client library for OpenAPI 3.0

## Usage

```python
import oai_request

c = oai_request.Client()
c.load_from_url("http://petstore.swagger.io/v2/swagger.json")
c.requestor.auth = (user, password) # c.requestor: requests.Session
resp = c.getPetById(petId=1) # resp: requests.Response
resp.json()
```

## Installation

```
pip install oai-request
```

## Licennse

MIT
