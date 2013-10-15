from tests.base import TestLinkTest

class SuitesTestCase(TestLinkTest):

    def setUp(self):
        super(SuitesTestCase, self).setUp()
        self.plan = self.api.projects.get('Testlink Api').plans.get(name='test plan')

    def test_can_create(self):
        self.plan.suites.create('test suite 1', 'This is an automated test')

    def test_can_list_api(self):
        for suite in self.api.get_suites(plan_id=self.plan.id).cursor:
            self.assertIsInstance(suite.id, basestring)            

    def test_can_list_plans(self):
        for suite in self.plan.suites.cursor:
            self.assertIsInstance(suite.id, basestring)

    def test_can_list_suites(self):
        suite = self.plan.suites.cursor[0]
        for s in suite.suites.cursor:
            print s

    def test_can_get(self):
        suite = self.plan.suites.cursor[0]
        print self.plan.suites.get(suite.id)
