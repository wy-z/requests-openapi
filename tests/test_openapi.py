import responses
import os

import requests_openapi
from . import conftest


@responses.activate
def test_petstore(v3_petstore):
    # mock
    url = "http://fake.com/api"
    get_resp = {"method": "get"}
    post_resp = {"method": "post"}
    responses.add(responses.GET, url + "/pets", json=get_resp)
    responses.add(responses.POST, url + "/pets", json=post_resp)
    responses.add(responses.GET, url + "/pets/1", json=get_resp)

    c = v3_petstore
    c.set_server(requests_openapi.Server(url=url))
    # get
    resp = c.listPets()
    assert resp.ok
    assert resp.json() == get_resp
    # post
    resp = c.createPets(json={"name": "test"})
    assert resp.ok
    assert resp.json() == post_resp
    # get by id
    resp = c.showPetById(petId=1)
    assert resp.ok
    assert resp.json() == get_resp


@responses.activate
def test_openapi_with_ref():
    # mock
    url = "http://fake.com/api"
    users_resp = {"url": "/users"}
    teams_resp = {"url": "/teams"}
    responses.add(responses.GET, url + "/users", json=users_resp)
    responses.add(responses.GET, url + "/teams", json=teams_resp)

    c = requests_openapi.Client().load_spec_from_file(
        os.path.join(conftest.THIS_DIR, "openapi/v3.0-with-ref.yaml")
    )
    c.set_server(requests_openapi.Server(url=url))
    # get
    resp = c.GetUser()
    assert resp.ok
    assert resp.json() == users_resp
    # post
    resp = c.GetTeam()
    assert resp.ok
    assert resp.json() == teams_resp
