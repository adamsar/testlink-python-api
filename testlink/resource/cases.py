from testlink.resource.base import ResourceCollection, ResourceInstance
from testlink.resource.sundry import ExecutionResult, Attachment, MethodResult
from testlink.exception.base import TestLinkException
from testlink.common import args, execution_types

import itertools

def make_step(number, actions, expected_results, execution_type=execution_types.AUTOMATED):
    return {
        args.STEP_NUMBER: number,
        args.ACTIONS: actions,
        args.EXPECTED_RESULTS: expected_results,
        args.EXECUTION_TYPE: execution_type
        }
    

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
    CREATE = 'createTestCase'

    def __init__(self, connection, plan_id, project_id = None, suite_id=None):
        super(TestCases, self).__init__(connection)
        self.plan_id = plan_id
        self.suite_id = suite_id
        self.project_id = project_id

        
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

    
    def create(self, name, author, summary, steps,
               **optionals):
        """
        * @param struct $args
  	  * @param string $args["devKey"]
  	  * @param string $args["testcasename"]
  	  * @param int    $args["testsuiteid"]: test case parent test suite id
  	  * @param int    $args["testprojectid"]: test case parent test suite id
  	  *
  	  * @param string $args["authorlogin"]: to set test case author
  	  * @param string $args["summary"]
  	  * @param string $args["steps"]
  	  *
  	  * @param string $args["preconditions"] - optional
      * @param string $args["importance"] - optional - see const.inc.php for domain
      * @param string $args["execution"] - optional - see ... for domain
      * @param string $args["order'] - optional
      * @param string $args["internalid"] - optional - do not use
      * @param string $args["checkduplicatedname"] - optional
      * @param string $args["actiononduplicatedname"] - optional
      *
  	  * @return mixed $resultInfo
      * @return string $resultInfo['operation'] - verbose operation
      * @return boolean $resultInfo['status'] - verbose operation
      * @return int $resultInfo['id'] - test case internal ID (Database ID)
      * @return mixed $resultInfo['additionalInfo'] 
      * @return int $resultInfo['additionalInfo']['id'] same as $resultInfo['id']
      * @return int $resultInfo['additionalInfo']['external_id'] without prefix
      * @return int $resultInfo['additionalInfo']['status_ok'] 1/0
      * @return string $resultInfo['additionalInfo']['msg'] - for debug 
      * @return string $resultInfo['additionalInfo']['new_name'] only present if new name generation was needed
      * @return int $resultInfo['additionalInfo']['version_number']
      * @return boolean $resultInfo['additionalInfo']['has_duplicate'] - for debug 
      * @return string $resultInfo['message']"""
        params = {
            args.TESTCASE_NAME: name,
            args.SUITE_ID: self.suite_id,
            args.PROJECT_ID: self.project_id,
            args.AUTHOR: author,
            args.SUMMARY: summary,
            args.STEPS: steps
            }
        def check_and_add(arg):
            v = optionals.get(arg, None)
            if v: params[arg] = v
        map(check_and_add,
            ['preconditions', 'importance', 'execution', 'order',
             'internalid', 'checkduplicatedname', 'actiononduplicatename'])        
        return self.connection.request(self.CREATE, params=params)    
        
        

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
    
    REPORT_RESULT = 'reportTCResult'
    ADD_TO_PLAN = 'addTestCaseToTestPlan'
    ATTACHMENTS = 'getTestCaseAttachments'
    LAST_EXECUTION = 'getLastExecutionResult'
    

    def __init__(self, connection, plan_id=None, **data):
        super(TestCase, self).__init__(connection, **data)
        self.plan_id = plan_id
        #For some reason 'id' is not the correct id on these
        if 'testcase_id' in data:
            self.id = data['testcase_id']
        if not self.id and 'tcase_id' in data:
            self.id = data['tcase_id']

            
    def report(self, status, build_id=None, build_name=None,
               notes=None, guess=False, bug_id=None, platform_id=None,
               platform_name=None, custom_fields=None, overwrite=True,):
        params = {
            args.PLAN_ID: self.plan_id,
            args.TESTCASE_ID: self.id,
            args.STATUS: status
            }
        def check_and_add(value, arg):
            if value: params[arg] = value
        map(lambda t: check_and_add(t[0], t[1]), [
            (build_id, args.BUILD_ID),
            (build_name, args.BUILD_NAME),
            (notes, args.NOTES),
            (guess, args.GUESS),
            (bug_id, args.BUG_ID),
            (platform_id, args.PLATFORM_ID),
            (platform_name, args.PLATFORM_NAME),
            (custom_fields, args.CUSTOM_FIELDS),
            (overwrite, args.OVERWRITE)
             ])
        results = self.connection.request(self.REPORT_RESULT, params=params)
        return 'True' in results.pop().get('status', '')


    def last_execution_result(self, plan_id=None):
        if plan_id:
            self.plan_id = plan_id
        if not self.plan_id:
            raise TestLinkException("Requires a plan to look up execution history")
        results = self.connection.request(self.LAST_EXECUTION,
                                          params = {
                                              args.TESTCASE_ID: self.id,
                                              args.PLAN_ID: self.plan_id                                              
                                              }).pop()
        return ExecutionResult(testcase_id=self.id, **results)
        

    @property
    def attachments(self):
        results = self.connection.request(self.ATTACHMENTS,
                                          params = {args.EXTERNAL_ID: self.external_id})
        return map(lambda data: Attachment(**data), results.values())

    
    def add(self, plan_id, project_id, version):
        results = self.connection.request(self.ADD_TO_PLAN,
                                          params = {
                                              args.TESTCASE_ID: self.id,
                                              args.PLAN_ID: plan_id,
                                              args.PROJECT_ID: project_id,
                                              args.VERSION: version
                                              })
        return MethodResult(**results[0])

    
    def __getattr__(self, attr):
        if attr == 'external_id':
            return self.__getattr__('full_tc_external_id')
        return super(TestCase, self).__getattr__(attr)
    

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
        return not _cases    
    
    @property
    def cases(self):  
        if self._should_build_cases:
            params = dict((k, getattr(self, k, None)) for k in ['plan_id',
                                                               'suite_id',
                                                               'build_id',
                                                               'project_id'])
            self._cases = self.get_cases(**params)
        return self._cases

    
    def get_cases(self, plan_id=None, suite_id=None,
                  build_id=None, project_id=None):
        cases = TestCases(self.connection, plan_id=plan_id,
                          suite_id=suite_id, project_id=project_id)
        if build_id:
            cases.filter(build_id=build_id)
        return cases
            
