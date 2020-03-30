# requests-openapi

[![image](https://img.shields.io/pypi/v/requests-openapi.svg)](https://pypi.org/project/requests-openapi/)
[![image](https://img.shields.io/pypi/l/requests-openapi.svg)](https://pypi.org/project/requests-openapi/)
[![image](https://img.shields.io/pypi/pyversions/requests-openapi.svg)](https://pypi.org/project/requests-openapi/)

RequestsOpenAPI is a python client library for OpenAPI 3.0

## Usage

```python
import requests_openapi

c = requests_openapi.Client()
c.load_spec_from_url("https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml")
resp = c.listPets() # resp: requests.Response
resp.json()
```

## Installation

```
pip install requests-openapi
```

## Licennse

MIT
