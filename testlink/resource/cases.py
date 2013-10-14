from testlink.resource.base import ResourceCollection, ResourceInstance
from testlink.exception.base import TestLinkException
from testlink.exception.lookup import TestLinkNotFound
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
    COLLECTION_BY_SUITE = 'getTestCasesForTestSuite'
    GET_ID_BY_NAME = 'getTestCaseIDByName'
    GET = 'getTestCase'

    def __init__(self, connection, plan_id, suite_id=None):
        super(TestCases, self).__init__(connection)
        self.plan_id = plan_id
        self.suite_id = suite_id

        
    def _build_case(self, **data):
        """
        Quick access for generating an associated TestCase ResourceInstance
        """
        return TestCase(self.connection, plan_id = self.plan_id, **data)

    
    def _make_cursor(self):
        if self.suite_id:
            klass = TestSuiteTestCase
            results = self.connection.request(self.COLLECTION_BY_SUITE,
                                              params = {args.SUITE_ID: self.suite_id})
        elif self.plan_id:
            klass = TestCase
            results = itertools.chain.from_iterable(
                self.connection.request(self.COLLECTION, params=self.filters).values()
                )
            
        else:
            raise TestLinkException("Must have at least a plan id to query test cases")
        return map(lambda result: klass(self.connection, plan_id=self.plan_id, **result),
                   results)

    
    @property
    def filters(self):
        base = { args.PLAN_ID: self.plan_id }
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

    
    def filter(self, **filters):
        for attr, value in filters.iteritems(): setattr(self, attr, value)
        return self


    @classmethod
    def get_by_name(cls, connection, name):
        query = { args.TESTCASE_NAME: name }
        results = connection.request(cls.GET_ID_BY_NAME, params=query)
        return TestCase(connection, **results)

            
    def get(self, external_id=None, _id=None, name=None, version=None):
        if not external_id and not _id and not name:
            raise TestLinkException("Requires an id, external id, or name to get a Test Case")
        
        if name:
            return self.get_by_name(self.connection, name)
            
        query = {
            
            }
        def update_if_exists(value, key):
            if value: query[key] = value
        update_if_exists(external_id, args.EXTERNAL_ID)
        update_if_exists(_id, args.TESTCASE_ID)
        update_if_exists(version, args.VERSION)
        results = self.connection.request(self.GET, params=query).pop()
        return self._build_case(**results)


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

    CREATE = 'createTestCase'
    ADD_TO_PLAN = 'addTestCaseToTestPlan'
    ATTACHMENTS = 'getTestCaseAttachments'        

    def __init__(self, connection, plan_id=None, **data):
        super(TestCase, self).__init__(connection, **data)
        self.plan_id = plan_id
        if 'tcase_id' in data:
            self.id = data['tcase_id']

        
    def report(self, plan_id=None, **results):
        raise NotImplemented("TODO")

    
    def last_execution_result(self):
        raise NotImplemented("TODO")


    def retrieve(self):
        raise NotImplemented("TODO")


class TestSuiteTestCase(ResourceInstance):
    """
    The returns for querying test cases by a test suite
    Keys:[
    'external_id',
    'id',
    'name',
    'node_order',
    'node_table',
    'node_type_id',
    'parent_id'
    ]    
    """

    def __init__(self, connection, **data):
        super(TestSuiteTestCase, self).__init__(connection, **data)
        
    
class TestCaseAccess(object):

    @property
    def _should_build_cases(self):
        _cases = getattr(self, '_cases', None)
        if not _cases:
            return True
        return False
    
    @property
    def cases(self):  
        if self._should_build_cases:
            self._cases = self.get_cases(plan_id=getattr(self, 'plan_id', None),
                                         suite_id=getattr(self, 'suite_id', None),
                                         build_id=getattr(self, 'build_id', None))
        return self._cases

    
    def get_cases(self, plan_id=None, suite_id=None, build_id=None):
        cases = TestCases(self.connection, plan_id=plan_id, suite_id=suite_id)
        if build_id:
            cases.filter(build_id=build_id)
        return cases
            
