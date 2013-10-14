from tests.base import TestLinkTest

class BuildsTestCase(TestLinkTest):

    def setUp(self):
        super(BuildsTestCase, self).setUp()
        self.plan = self.api.projects.cursor[0].plans.cursor[0]        

    def test_can_list_api(self):
        for build in self.api.get_builds(self.plan.id).cursor:
            print build

    def test_can_list_plans(self):
        for build in self.plan.builds.cursor:
            print build

    def test_can_get_latest(self):
        print self.plan.builds.latest

    def test_can_get(self):
        build = self.plan.builds.cursor[0]
        print self.plan.builds.get(build.id)
