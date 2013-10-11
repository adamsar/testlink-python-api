from tests.base import TestLinkTest

class TestTestCases(TestLinkTest):

    def test_can_list(self):
        for project in self.api.projects.cursor():
            for plan in project.plans.cursor():
                for resource in plan.cases.cursor():
                    self.assertTrue(False)
