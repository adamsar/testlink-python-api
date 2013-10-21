"""
Basic test link exceptions
"""

class TestLinkException(Exception):

    def __init__(self, msg):
        super(TestLinkException, self).__init__(msg)
