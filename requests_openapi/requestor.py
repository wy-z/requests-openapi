import abc

import requests


class Requestor(abc.ABC):
    @abc.abstractmethod
    def request(self, method, url, params={}, headers={}, cookies={}, **kwargs):
        pass


Requestor.register(requests.Session)
