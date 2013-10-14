from testlink.resource.base import ResourceCollection, ResourceInstance
from testlink.resource.cases import TestCaseAccess
from testlink.exception.base import TestLinkException
from testlink.common import args

class TestSuites(ResourceCollection):
    COLLECTION = 'getTestSuitesForTestPlan'
    BASE_COLLECTION = 'getFirstLevelTestSuitesForTestProject'
    BY_ID = 'getTestSuiteByID'
    BY_SUITE = 'getTestSuitesForTestSuite'
    CREATE = 'createTestSuite'    

    def __init__(self, connection, plan_id=None, suite_id=None):
        super(TestSuites, self).__init__(connection)
        self.plan_id = plan_id
        self.suite_id = suite_id

        
    def _build_suite(self, **data):
        return TestSuite(self.connection, plan_id = self.plan_id, **data)

    
    def _make_cursor(self):
        if not self.plan_id and not self.suite_id:
            raise TestLinkException("Need a suite or plan id to get suites")
        method = self.COLLECTION if self.plan_id else self.BY_SUITE
        params = {}
        def check_and_add(value, arg):
            if value: params[arg] = value
        check_and_add(self.plan_id, args.PLAN_ID)
        check_and_add(self.plan_id, args.SUITE_ID)        
        results = self.connection.request(method, params = params)
        return map(lambda result: self._build_suite(**result), results)

    
    @property
    def first_level(self):
        if not self.plan_id:
            raise TestLinkException("Need a plan_id in order to get first level suites")
        results = self.connection.request(self.BASE_COLLECTION,
                                          params={args.PLAN_ID: self.plans_id})
        return map(lambda result: self._build_suite(**result), results)
    

    def get(self , _id):
        results = self.connection.request(self.BY_ID, params = {args.SUITE_ID: _id})
        return TestSuite(self.connection, **results)

    
    def create(self, **params):
        pass
    
        
class TestSuiteAccess(object):

    @property
    def _should_build_suites(self):
        _suites = getattr(self, '_suites', None)
        if not _suites:
            return True
        same_suite = self._suites.suite_id == getattr(self, 'suite_id', None)
        same_plan = self._suites.plan_id == getattr(self, 'plan_id', None)
        return not same_plan or not same_suite

    
    @property
    def suites(self):
        if self._should_build_suites:
            self._suites = self.get_suites(plan_id=getattr(self, 'plan_id', None),
                                           suite_id=getattr(self, 'suite_id', None))
        return self._suites

    
    def get_suites(self, plan_id=None, suite_id=None):
        return TestSuites(self.connection, plan_id=plan_id, suite_id=suite_id)

    
class TestSuite(ResourceInstance, TestSuiteAccess, TestCaseAccess):
    """
    A suite of tests in the system
    keys: [
    'id',
    'name',
    'parent_id'
    ]
    """

    def __init__(self, connection, plan_id=None, **data):
        super(TestSuite, self).__init__(connection, **data)
        if 'id' in data:
            self.suite_id = data['id']

