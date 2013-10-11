from unittest import TestCase
from testlink import TestLinkClient

class TestLinkTest(TestCase):

    def setUp(self):
        self.api = TestLinkClient(url="http://bptest.ubicast.com/lib/api/xmlrpc/v1/xmlrpc.php",
                                  key="0b7baeeea2c301708a8f39f362dd0ffe")
        
