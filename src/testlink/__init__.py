import os

from testlink.exception.base import TestLinkException
from testlink.resource.project import Projects
from testlink.resource.cases import TestCaseAccess
from testlink.resource.builds import TestBuildAccess
from testlink.resource.suites import TestSuiteAccess
from testlink.resource.plans import TestPlanAccess
from testlink.resource.platform import TestPlatformAccess
from testlink.resource.sundry import MethodResult
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


class TestLinkClient(TestCaseAccess, TestPlanAccess,
                     TestBuildAccess, TestSuiteAccess, TestPlatformAccess):
    DELETE_EXECUTION = 'deleteExecution'
    
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
        self.projects = Projects(self)
        #Making itself the connection is a bit of a 'hack', but allows a clean
        #interface for getting objects        
        self.connection = self 


    def request(self, method, params={}):
        """
        Make a request to a method on the server
        """
        params[args.DEVKEY] = self.key
        try:
            return getattr(self.server.tl, method)(params)
        except TypeError:
            raise TestLinkException("Call failed with parameters: {}".format(str(params)))
            

    def delete_execution_result(self, execution_id):
        """
        Delete's an execution result from the server. Useful in conjunction
        with the Testcase.latest_execution_result method
        """
        params = {
            args.EXECUTION_ID: execution_id
            }
        results = self.request(self.DELETE_EXECUTION, params=params)
        return MethodResult(**results)
