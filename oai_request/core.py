import logging
import pprint
import typing

import requests
import yaml

from .requestor import Requestor


class OAIKeyWord:
    OPENAPI = "openapi"
    INFO = "info"

    SERVERS = "servers"
    URL = "url"
    DESCRIPTION = "description"
    VARIABLES = "variables"

    PATHS = "paths"
    OPERATION_ID = "operationId"
    PARAMETERS = "parameters"
    IN = "in"
    PATH = "path"
    QUERY = "query"
    HEADER = "header"
    COOKIE = "cookie"
    NAME = "name"
    REQUIRED = "required"
    SCHEMA = "schema"
    TYPE = "type"
    STRING = "string"


class Server(object):
    _url: str
    description: str
    variables: typing.Dict[str, typing.Any]

    def __init__(self, url=None, description=None, variables={}):
        self._url = url
        self.description = description
        self.variables = variables

    @property
    def url(self):
        return self._url.format(self.variables)

    def set_url(self, url):
        self._url = url


class Operation(object):
    _internal_param_prefix = "_"
    _path: str
    _method: str
    _spec: typing.Dict[str, typing.Any]
    _requestor: Requestor
    _server: Server

    _call: typing.Optional[typing.Callable] = None

    def __init__(self, path, method, spec, requestor=None, server=None):
        self._path = path
        self._method = method
        self._spec = spec
        self._requestor = requestor
        self._server = server

    @property
    def spec(self):
        return self._spec

    @property
    def operation_id(self):
        return self._spec[OAIKeyWord.OPERATION_ID]

    @property
    def method(self):
        return self.method

    @property
    def path(self):
        return self._path

    def url(self, **kwargs):
        return self._server.url + self._path.format(**kwargs)

    def _gen_call(self):
        def f(**kwargs):
            # collect oai params
            path_params = {}
            params = {}
            headers = {}
            cookies = {}
            for spec in self._spec.get(OAIKeyWord.PARAMETERS, []):
                _in = spec[OAIKeyWord.IN]
                name = spec[OAIKeyWord.NAME]

                if name not in kwargs:
                    if _in == OAIKeyWord.PATH:
                        raise ValueError(f"'{name}' is required")
                    continue

                if _in == OAIKeyWord.PATH:
                    path_params[name] = kwargs.pop(name)
                elif _in == OAIKeyWord.QUERY:
                    params[name] = kwargs.pop(name)
                elif _in == OAIKeyWord.HEADER:
                    headers[name] = kwargs.pop(name)
                elif _in == OAIKeyWord.COOKIE:
                    cookies[name] = kwargs.pop(name)

            # collect internal params
            for k in kwargs:
                if not k.startswith(self._internal_param_prefix):
                    continue
                kwargs[
                    k[len(self._internal_param_prefix) :]  # noqa: E203
                ] = kwargs.pop(k)
            kwargs.setdefault("params", {}).update(params)
            kwargs.setdefault("headers", {}).update(headers)
            kwargs.setdefault("cookies", {}).update(cookies)
            return self._requestor.request(
                self._method, self.url(**path_params), **kwargs
            )

        return f

    def __call__(self, *args, **kwargs):
        if not self._call:
            self._call = self._gen_call()
        return self._call(*args, **kwargs)

    def help(self):
        return pprint.pprint(self.spec, indent=2)

    def __repr__(self):
        return f"<{type(self).__name__}: [{self._method}] {self._path}>"


def load_spec_from_url(url):
    r = requests.get(url)
    r.raise_for_status()

    return yaml.load(r.text, Loader=yaml.Loader)


def load_spec_from_file(file_path):
    with open(file_path) as f:
        spec_str = f.read()

    return yaml.load(spec_str, Loader=yaml.Loader)


class Client(object):
    _requestor: Requestor
    _server: Server
    _operations: typing.Dict[str, typing.Any]
    _spec: typing.Dict[str, typing.Any]

    def __init__(self, requestor=None, server=None):
        self._requestor = requestor or requests.Session()
        self._server = server
        self._operations = {}
        self._spec = {}

    @property
    def spec(self):
        return self._spec

    def load_spec(self, spec: typing.Dict):
        if not all(
            [i in spec for i in [OAIKeyWord.OPENAPI, OAIKeyWord.INFO, OAIKeyWord.PATHS]]
        ):
            raise ValueError("Invaliad openapi document")
        self._spec = spec.copy()
        spec = spec.copy()

        servers = spec.pop(OAIKeyWord.SERVERS, [])
        for key in spec:
            rkey = key.replace("-", "_")
            self.__setattr__(rkey, spec[key])
        self.servers = [
            Server(
                url=s.get(OAIKeyWord.URL),
                description=s.get(OAIKeyWord.DESCRIPTION),
                variables=s.get(OAIKeyWord.VARIABLES),
            )
            for s in servers
        ]
        if not self._server and self.servers:
            self._server = self.servers[0]

        self._collect_operations()

    def _collect_operations(self):
        self._operations = {}
        for path, path_spec in self.paths.items():
            for method, op_spec in path_spec.items():
                operation_id = op_spec.get(OAIKeyWord.OPERATION_ID)
                if not operation_id:
                    logging.warn(
                        f"'{OAIKeyWord.OPERATION_ID}' not found in: '[{method}] {path}'"
                    )
                    continue

                if operation_id not in self._operations:
                    self._operations[operation_id] = Operation(
                        path,
                        method,
                        op_spec,
                        requestor=self._requestor,
                        server=self._server,
                    )
                else:
                    v = self._operations[operation_id]
                    if type(v) is not list:
                        self._operations[operation_id] = [v]
                    self._operations[operation_id].append(
                        Operation(path, method, op_spec, requestor=self._requestor)
                    )

    def load_from_url(self, url):
        spec = load_spec_from_url(url)
        self.load_spec(spec)
        return

    def load_from_file(self, file_path):
        spec = load_spec_from_file(file_path)
        self.load_spec(spec)
        return

    @property
    def requestor(self):
        return self._requestor

    def set_requestor(self, r: Requestor):
        self._requestor = r
        self._collect_operations()

    @property
    def server(self):
        return self._server

    def set_server(self, s):
        self._server = s
        self._collect_operations()

    def __getattr__(self, op_name):
        if op_name in self._operations:
            return self._operations[op_name]
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{op_name}'"
        )
