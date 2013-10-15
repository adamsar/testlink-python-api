from testlink.resource.base import ResourceCollection, ResourceInstance
from testlink.resource.cases import TestCaseAccess
from testlink.resource.sundry import MethodResult
from testlink.exception.base import TestLinkException
from testlink.common import args

class TestSuites(ResourceCollection):
    COLLECTION = 'getTestSuitesForTestPlan'
    BASE_COLLECTION = 'getFirstLevelTestSuitesForTestProject'
    BY_ID = 'getTestSuiteByID'
    BY_SUITE = 'getTestSuitesForTestSuite'
    CREATE = 'createTestSuite'    

    def __init__(self, connection, plan_id=None, suite_id=None, project_id=None):
        super(TestSuites, self).__init__(connection)
        self.plan_id = plan_id
        self.suite_id = suite_id        
        self.project_id = project_id

        
    def _build_suite(self, **data):
        return TestSuite(self.connection, plan_id = self.plan_id,
                         project_id = self.project_id, **data)

    
    def _make_cursor(self):
        if not self.plan_id and not self.suite_id:
            if not self.project_id:
                raise TestLinkException("Need a suite or plan id to get suites")
            else:
                return self.first_level
        method = self.COLLECTION if self.plan_id else self.BY_SUITE
        params = {}
        def check_and_add(value, arg):
            if value: params[arg] = value
        check_and_add(self.plan_id, args.PLAN_ID)
        check_and_add(self.suite_id, args.SUITE_ID)        
        results = self.connection.request(method, params = params)
        return map(lambda result: self._build_suite(**result), results)

    
    @property
    def first_level(self):
        if not self.plan_id:
            raise TestLinkException("Need a plan_id in order to get first level suites")
        results = self.connection.request(self.BASE_COLLECTION,
                                          params={args.PROJECT_ID: self.project_id})
        return map(lambda result: self._build_suite(**result), results)
    

    def get(self , _id=None, name=None):
        if _id:
            results = self.connection.request(self.BY_ID, params = {args.SUITE_ID: _id})
            return self._build_suite(**results)
        elif name:
            return filter(lambda suite: suite.name == name, self.first_level + self.cursor).pop()
        else:
            raise TestLinkException("Requires an id or name to look up a test suite")

    
    def create(self, name, details, parent_id=None, order=None, check_duplicated_name=None,
               action_on_duplicated_name=None):
        params = {
            args.PROJECT_ID: self.project_id,
            args.TESTSUITE_NAME: name,
            args.DETAILS: details
            }
        def check_and_add(value, arg):
            if value: params[arg] = value
        map(lambda t: check_and_add(t[0], t[1]), [
            (parent_id, args.PARENT_ID),
            (order, args.ORDER),
            (check_duplicated_name, args.CHECK_DUPLICATE_NAME),
            (action_on_duplicated_name, args.ACTION_ON_DUPLICATED_NAME)
            ])
        results = self.connection.request(self.CREATE, params=params)
        return MethodResult(**results[0])
    
        
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
            params = dict((k, getattr(self, k, None)) for k in ['plan_id',
                                                               'suite_id',
                                                               'project_id'])
            self._suites = self.get_suites(**params)
        return self._suites

    
    def get_suites(self, plan_id=None, suite_id=None, project_id=None):
        return TestSuites(self.connection, plan_id=plan_id, suite_id=suite_id,
                          project_id=project_id)

    
class TestSuite(ResourceInstance, TestSuiteAccess, TestCaseAccess):
    """
    A suite of tests in the system
    keys: [
    'id',
    'name',
    'parent_id'
    ]
    """

    def __init__(self, connection, plan_id=None, project_id=None, **data):
        super(TestSuite, self).__init__(connection, **data)
        self.plan_id = plan_id
        self.project_id = project_id
        if 'id' in data:
            self.suite_id = data['id']

