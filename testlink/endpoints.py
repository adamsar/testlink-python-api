"""
All valid end points for the api
"""


class Endpoints(object):

    def _request(self, endpoint, method='GET', params={}):
        raise NotImplemented("Requires a request implementor")
