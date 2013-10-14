from testlink.resource.base import ApiReturn, ResourceInstance

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

class ExecutionResult(ResourceInstance):
    CREATE = 'setTestCaseExecutionResult'
    DELETE = 'deleteExecution'
    REPORT = 'reportTCResult'

    def __init__(self, connection, testcase_id=None, **data):
        super(ExecutionResult, self).__init__(connection, **data)
        self.testcase_id = testcase_id

    def create(self):
        raise NotImplemented()

    def delete(self):
        raise NotImplemented()
