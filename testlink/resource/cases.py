from testlink.resource.base import ResourceCollection, ResourceInstance
from testlink.exception.base import TestLinkException
from testlink.common import args

import itertools

class TestCases(ResourceCollection):
    """
    	 * @param struct $args
	 * @param string $args["devKey"]
	 * @param int $args["testplanid"]
	 * @param int $args["testcaseid"] - optional
	 * @param int $args["buildid"] - optional
	 * @param int $args["keywordid"] - optional mutual exclusive with $args["keywordname"]
	 * @param int $args["keywords"] - optional  mutual exclusive with $args["keywordid"]
	 *
	 * @param boolean $args["executed"] - optional
	 * @param int $args["$assignedto"] - optional
	 * @param string $args["executestatus"] - optional
	 * @param array $args["executiontype"] - optional
	 * @param array $args["getstepinfo"] - optional - default false
   """
    COLLECTION = 'getTestCasesForTestPlan'

    def __init__(self, connection, plan_id, build_id=None):
        super(TestCases, self).__init__(connection)
        self.plan_id = plan_id

        
    @property
    def filters(self):
        base = {
            args.PLAN_ID: self.plan_id
            }
        def check_and_add(attr, arg_name):
            value = getattr(self, attr, None)
            if value:
                base[arg_name] = value
        filters = [
            ("build_id", args.BUILD_ID),
            ("testcase_id", args.TESTCASE_ID),
            ("keyword_id", args.KEYWORD_ID),
            ("keywords", args.KEYWORDS),
            ("executed", args.EXECUTED),
            ("assigned_to", args.ASSIGNED_TO),
            ("status", args.STATUS),
            ("execution_type", args.EXECUTION_TYPE),
            ("get_step_info", args.GET_STEP_INFO)
            ]
        for attr, arg_name in filters: check_and_add(attr, arg_name)
        return base
    

    def _make_cursor(self):
        results = self.connection.request(self.COLLECTION, params=self.filters).values()
        return map(lambda result: TestCase(self.connection, plan_id=self.plan_id, **result),
                   itertools.chain.from_iterable(results))

    
    def filter(self, **filters):
        for attr, value in filters.iteritems():
            setattr(self, attr, value)
        return self

    def get(self, external_id=None, _id=None, name=None):
        raise NotImplemented


class TestCase(ResourceInstance):
    """
    Something that needs testing within the system
    Valid keys are (small):
    ['exec_status',
    'execution_order',
    'execution_type',
    'external_id',
    'feature_id',
    'full_external_id',
    'platform_id',
    'platform_name',
    'tc_id',
    'tcase_id',
    'tcase_name',
    'tcversion_id',
    'version']
    """
    

    def __init__(self, connection, plan_id=None, **data):
        super(TestCase, self).__init__(connection, **data)
        print sorted(data.keys())
        self.plan_id = plan_id

        
    def report(self, **results):
        raise NotImplemented("TODO")

    
    def last_execution_result(self):
        raise NotImplemented("TODO")


    def retrieve(self):
        raise NotImplemented("TODO")
