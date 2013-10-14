from tests.base import TestLinkTest

class PlatformsTestCase(TestLinkTest):

    def setUp(self):
        super(PlatformsTestCase, self).setUp()
        self.plan = self.api.projects.cursor[0].plans.cursor[1]

    def test_api_can_list(self):
        for platform in self.api.get_platforms(self.plan.id).cursor:
            print platform

    def test_plan_can_list(self):
        for platform in self.plan.platforms.cursor:
            print platform
