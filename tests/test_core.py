import requests
import responses

import requests_openapi

from . import conftest


def test_load_from_file():
    c = requests_openapi.Client().load_spec_from_file(conftest.OPENAPI_V3_PETSTORE)
    assert isinstance(c, requests_openapi.Client)
    assert isinstance(c.listPets, requests_openapi.Operation)


@responses.activate
def test_load_from_url():
    url = "http://fake.com/openapi.json"
    with open(conftest.OPENAPI_V3_PETSTORE) as f:
        spec = f.read()
    responses.add(
        responses.GET,
        url,
        body=spec,
        headers={"content-type": "application/vnd.oai.openapi"},
    )

    c = requests_openapi.Client().load_spec_from_url(url)
    assert isinstance(c, requests_openapi.Client)
    assert isinstance(c.listPets, requests_openapi.Operation)


def test_client_class(v3_petstore):
    c = v3_petstore
    assert isinstance(c, requests_openapi.Client)
    assert isinstance(c.operations, dict)
    assert isinstance(c.operations["listPets"], requests_openapi.Operation)
    assert type(c.spec).__name__ == "OpenAPI"
    # set server
    server = requests_openapi.Server(url="http://fake.com")
    c.set_server(server)
    assert c.server == server
    # set requestor
    session = requests.Session()
    c.set_requestor(session)
    assert c.requestor == session


def test_server_class():
    server = requests_openapi.Server(url="http://fake.com")
    # set url
    new_url = "https://new-fake.com"
    server.set_url(new_url)
    assert server.get_url() == new_url
    # get url with variables
    server.set_url("https://fake.{var1}.{var2}.com")
    server.variables = {"var1": 1, "var2": 2}
    assert server.get_url() == "https://fake.1.2.com"


def test_object_class(v3_petstore):
    c = v3_petstore
    assert isinstance(c.listPets, requests_openapi.Operation)
    assert c.listPets.operation_id == "listPets"
    assert c.listPets.gen_url() == "http://petstore.swagger.io/v1/pets"
    assert c.showPetById.gen_url(petId=1) == "http://petstore.swagger.io/v1/pets/1"
