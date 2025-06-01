import json
import os

import responses
import yaml

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


OPENAPI_WITH_PARAMS = """
openapi: 3.0.2
info:
  title: openapi-with-params
  version: 1.0.0
paths:
  /users:
    get:
      summary: Gets a list of users.
      parameters:
        - in: query
          name: offset
        - in: header
          name: X-Request-ID
      operationId: ListUsers
      responses:
        "200":
          description: OK
  /users-with-cookie:
    get:
      summary: Gets a list of users.
      parameters:
        - in: cookie
          name: csrftoken
      operationId: ListUsersWithCookie
      responses:
        "200":
          description: OK
  /users/{userId}:
    get:
      summary: Gets a list of users.
      parameters:
        - in: path
          name: userId
      operationId: GetUser
      responses:
        "200":
          description: OK
"""


@responses.activate
def test_openapi_with_params():
    # mock
    url = "http://fake.com/api"
    responses.add(
        responses.GET, url + "/users/1", json={"in": "path", "name": "userId"}
    )
    responses.add(
        responses.GET,
        url + "/users",
        json={"in": "query", "name": "offset"},
        match=[responses.matchers.query_param_matcher({"offset": 1})],
    )
    responses.add(
        responses.GET,
        url + "/users",
        json={"in": "header", "name": "X-Request-ID"},
        match=[responses.matchers.header_matcher({"X-Request-ID": "1"})],
    )

    def cookie_callback(req):
        assert req._cookies["csrftoken"] == "1"
        return 200, [], json.dumps({"in": "cookie", "name": "csrftoken"})

    responses.add_callback(
        responses.GET, url + "/users-with-cookie", callback=cookie_callback
    )

    c = requests_openapi.Client()
    c.load_spec(yaml.load(OPENAPI_WITH_PARAMS, Loader=yaml.CLoader))
    c.set_server(requests_openapi.Server(url=url))
    # path
    resp = c.GetUser(userId=1)
    assert resp.ok
    assert resp.json() == {"in": "path", "name": "userId"}
    # query
    resp = c.ListUsers(offset=1)
    assert resp.ok
    assert resp.json() == {"in": "query", "name": "offset"}
    # header
    resp = c.ListUsers(**{"X-Request-ID": "1"})
    assert resp.ok
    assert resp.json() == {"in": "header", "name": "X-Request-ID"}
    # cookie
    resp = c.ListUsersWithCookie(csrftoken="1")
    assert resp.ok
    assert resp.json() == {"in": "cookie", "name": "csrftoken"}
    # path_params
    resp = c.GetUser(_path_params = {"userId": 1})
    assert resp.ok
    assert resp.json() == {"in": "path", "name": "userId"}
