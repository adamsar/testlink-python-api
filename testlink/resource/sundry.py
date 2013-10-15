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
        
    
class ExecutionResult(ApiReturn):
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
    pass
    
class MethodResult(ApiReturn):
    """
    A return from creating an object or performing most "PUT" functions
    keys:
    ['status', 'additionalInfo', 'operation', 'message', 'id']
    """

    def __getattr__(self, attr):
        if attr == 'additionalInfo':
            return self._parse_and_update(attr, lambda x: Info(**x))
        return super(MethodResult, self).__getattr__(attr)

    
class Info(ApiReturn):
    """
    Additional information returned with a method result
    keys: ['new_name',
    'version_number',
    'tcversion_id',
    'msg',
    'status_ok',
    'external_id'
    'has_duplicate'
    ]
    """
    
    __flags__ = ['status_ok']
