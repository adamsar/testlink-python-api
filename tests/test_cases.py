from tests.base import TestLinkTest
from testlink.exception.base import TestLinkException
from testlink.common import status

class TestCaseTestCase(TestLinkTest):

    def setUp(self):
        super(TestCaseTestCase, self).setUp()
        self.plan = self.api.projects.cursor[0].plans.cursor[1]
        self.build = self.plan.builds.cursor[0]
        self.suite = self.plan.suites.cursor[0]

    def _cases_bootstrap(self):
        cases = self.plan.cases
        case = cases.cursor[0]
        return cases, case
        

    def test_full_list_api(self):
        for case in self.api.get_cases(plan_id=self.plan.id).cursor:
            print case
            
        for case in self.api.get_cases(plan_id=self.plan.id, build_id=self.build.id).cursor:
            print case
            
        for case in self.api.get_cases(suite_id=self.suite.id).cursor:
            print case
        

    def test_list_plan(self):
        for case in self.plan.cases.cursor:
            print case
            

    def test_list_build(self):
        for case in self.build.cases.cursor:
            print case
            

    def test_list_suite(self):
        for case in self.suite.cases.cursor:
            print case

    def test_filter(self):
        pass

    def test_get(self):
        cases, case = self._cases_bootstrap()
        print case.data
        print cases.get(_id=case.id)
        print cases.get(external_id=case.full_external_id)
        self.assertRaises(TestLinkException, cases.get)        

        
    def test_get_by_name(self):
        cases, case = self._cases_bootstrap()
        print cases.get(name=case.name)


    def test_latest_execution_result(self):
        case = self.api.get_cases(plan_id=self.plan.id).get(external_id='bp-68')
        print case.last_execution_result()

    def test_get_attachments(self):
        case = self.api.get_cases().get(external_id='bp-3')
        print [attachment.date_added for attachment in case.attachments]


    def test_send_report(self):
        case = self.api.get_cases(self.plan.id).get(external_id='bp-3')
        result = case.report(status.FAILED, build_id=self.build.id,
                    notes='This is automated',
                    overwrite=False)
