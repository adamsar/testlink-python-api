"""Test retrieving projects"""

from testlink.resource.sundry import Options
from tests.base import TestLinkTest

class ProjectTestCase(TestLinkTest):

    def test_can_list(self):
        for project in self.api.projects.cursor:
            self.assertIsInstance(project.active, bool)
            self.assertIsInstance(project.options, Options)

    def test_can_get(self):
        project = self.api.projects.cursor[0]
        self.api.projects.get(project.name)


    def test_can_create(self):
        self.api.projects.create('Testlink', 'tapi', 'This is generated from a python script')
