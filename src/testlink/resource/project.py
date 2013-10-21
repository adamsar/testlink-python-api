from testlink.resource.base import ResourceCollection, ResourceInstance
from testlink.resource.plans import TestPlanAccess
from testlink.resource.suites import TestSuiteAccess
from testlink.resource.sundry import Options, MethodResult
from testlink.common import args

class Projects(ResourceCollection):

    COLLECTION = "getProjects"
    SINGLE = "getTestProjectByName"
    CREATE = 'createTestProject'

    def _make_cursor(self):
        
        return map(lambda result: Project(self.connection, **result),
                   self.connection.request(self.COLLECTION))
    
    def get(self, name):
        """
        Get a project by name
        """
        for project in self.cursor:
            if project.name == name:
                return project
        raise KeyError("Project {} does not exist".format(name))

    def create(self, name, prefix, notes):
        """
        Creates a new TestProject. Note this has no results for some reason
        """
        params = {
            args.PROJECT_NAME: name,
            args.PREFIX: prefix,
            args.NOTES: notes
            }            
        results = self.connection.request(self.CREATE, params=params)
        return MethodResult(**results.pop())


class Project(ResourceInstance, TestPlanAccess, TestSuiteAccess):
    """
    The most basic block the api, a single Project
    Fields are:
    [
    'active',
    'color',
    'id',
    'is_public',
    'issue_tracker_enabled',
    'name',
    'notes',
    'opt',
    'option_automation',
    'option_priority',
    'option_reqs',
    'options',
    'prefix',
    'reqmgr_integration_enabled',
    'tc_counter'
    ]
    """
    

    __flags__ = [
        'active',
        'is_public',
        'issue_tracker_enabled',
        'option_automation',
        'option_priority',
        'option_reqs'
        ]

    def __init__(self, connection, **data):
        super(Project, self).__init__(connection, **data)
        if "id" in self.data:
            self.project_id = self.data['id']
            
    def __getattr__(self, attr):
        if attr == 'project_name':
            return self.__getattr__('name')
        if attr == "tc_counter":
            return self._parse_and_update(attr, int)
        if attr in ['opt', 'options']:
            return self._parse_and_update('opt', Options.create)
        return super(Project, self).__getattr__(attr)
    
