import os

import pytest

import requests_openapi

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

OPENAPI_V3_PETSTORE = os.path.join(THIS_DIR, "openapi/v3.0-petstore.yaml")


@pytest.fixture
def v3_petstore():
    return requests_openapi.Client().load_spec_from_file(OPENAPI_V3_PETSTORE)
