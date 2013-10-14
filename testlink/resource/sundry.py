from testlink.resource.base import ApiReturn, ResourceInstance
from testlink.resource import parser

class Options(ApiReturn):

    __flags__ = [
        'automationEnabled',
        'inventoryEnabled',
        'requirementsEnabled',
        'testPriorityEnabled'
        ]

    @classmethod
    def create(cls, data):
        return Options(**data)

class Attachment(ApiReturn):

    def __getattr__(self, attr):
        if attr == 'date_added':
            return self._parse_and_update(attr, parser.format_date)
        return super(Attachment, self).__getattr__(attr)
        
    
class ExecutionResult(ResourceInstance):
    """
    A single execution of a test case
    Keys: ['build_id',
    'execution_ts',
    'execution_type',
    'id',
    'notes',
    'platform_id',
    'status',
    'tcversion_id',
    'tcversion_number',
    'tester_id',
    'testplan_id']
    """
    CREATE = 'setTestCaseExecutionResult'
    DELETE = 'deleteExecution'

    def __init__(self, connection, testcase_id=None, **data):
        super(ExecutionResult, self).__init__(connection, **data)
        self.testcase_id = testcase_id

    def create(self):
        raise NotImplemented()

    def delete(self):
        raise NotImplemented()
