"""
Errors with looking up information in TestLink
"""

from testlink.exception.base import TestLinkException

class TestLinkNotFound(TestLinkException):
    """
    Denotes the object that was searched for was not
    found
    """

    def __init__(self, msg="Not found"):
        super(TestLinkNotFound, self).__init__(self, msg)
        
