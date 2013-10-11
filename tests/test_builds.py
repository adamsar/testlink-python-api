from tests.base import TestLinkTest

class TestPlans(TestLinkTest):

    def test_can_list_plans(self):
        for project in self.api.projects.cursor():
            for plan in project.plans.cursor():
                for build in plan.builds.cursor():
                    print build

        self.assertTrue(False)


    def test_get_latest(self):
        for project in self.api.projects.cursor():
            for plan in project.plans.cursor():
                print plan.builds.latest()

        self.assertTrue(False)        
