from unittest import TestCase
from testlink import TestLinkClient

class TestLinkTest(TestCase):

    def setUp(self):
        self.api = TestLinkClient()
        
