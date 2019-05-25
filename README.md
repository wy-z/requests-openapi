# oai-request

OAIRequest is a python client library for OpenAPI 3.0

## Usage

```python
import oai_request

c = oai_request.Client()
c.load_from_url("http://petstore.swagger.io/v2/swagger.json")
c.requestor.auth = (user, password) # requests.Session
resp = c.getPetById(petId=1) # requests.Response
resp.json()
```

## Installation

```
pip install oai-request
```

## Licennse

MIT
