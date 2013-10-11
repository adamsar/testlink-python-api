from tests.base import TestLinkTest

class TestPlans(TestLinkTest):

    def test_can_list_plans(self):
        for project in self.api.projects.cursor():
            for plan in project.plans.cursor():
                print plan

        self.assertTrue(False)
        
