from tests.base import TestLinkTest

class TestPlans(TestLinkTest):

    def setUp(self):
        super(TestPlans, self).setUp()
        self.project = self.api.projects.get('Testlink Api')
        print self.project.data

    def test_can_create(self):
        self.project.plans.create('test plan')

    def test_api_can_list(self):
        for plan in self.api.get_plans(self.project.id).cursor:
            print plan

    def test_project_can_list(self):
        for plan in self.project.plans.cursor:
            print plan

    def test_can_get(self):
        plan = self.project.plans.cursor[0]
        print self.project.plans.get(_id=plan.id)
        print self.project.plans.get(name=plan.name)
