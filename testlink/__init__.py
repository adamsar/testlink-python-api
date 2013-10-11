import os

from testlink.exception.base import TestLinkException
from testlink.resource.project import Projects
from testlink.common import args

import xmlrpclib

URL_ENV_VAR = "TESTLINK_URL"
KEY_ENV_VAR = "TESTLINK_KEY"

def find_creds():
    """
    Searches the user's environment for TestLink credentials and urls
    """
    try:
        url = os.environ[URL_ENV_VAR]
        key = os.environ[KEY_ENV_VAR]
        return (url, key)
    except KeyError:
        return (None, None)


class TestLinkClient(object):

    def __init__(self, url=None, key=None):
        """
        Create a TestLinkClient
        """
        invalid = lambda: not url or not key
        if invalid():
            url, key = find_creds()
            if invalid():
                raise TestLinkException("Could not find url or key to connect to the TestLinkAPI")
        self.url = url
        self.key = key
        self.server = xmlrpclib.Server(url)

        #Add in base resources
        self.projects = Projects(self)
        

    def request(self, method, params={}):
        """
        Make a request to a method on the server
        """
        params[args.DEVKEY] = self.key
        return getattr(self.server.tl, method)(params)
