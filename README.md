# requests-oai

[![image](https://img.shields.io/pypi/v/requests-oai.svg)](https://pypi.org/project/requests-oai/)
[![image](https://img.shields.io/pypi/l/requests-oai.svg)](https://pypi.org/project/requests-oai/)
[![image](https://img.shields.io/pypi/pyversions/requests-oai.svg)](https://pypi.org/project/requests-oai/)

RequestsOAI is a python client library for OpenAPI 3.0

## Usage

```python
import requests_oai

c = requests_oai.Client()
c.load_from_url("http://petstore.swagger.io/v2/swagger.json")
c.requestor.auth = (user, password) # c.requestor: requests.Session
resp = c.getPetById(petId=1) # resp: requests.Response
resp.json()
```

## Installation

```
pip install requests-oai
```

## Licennse

MIT
