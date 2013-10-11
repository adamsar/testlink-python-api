from testlink.resource.base import ResourceCollection, ResourceInstance
from testlink.resource.plans import TestPlans, TestPlan
from testlink.resource.sundry import Options

class Projects(ResourceCollection):

    COLLECTION = "getProjects"
    SINGLE = "getTestProjectByName"

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


class Project(ResourceInstance):
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
            self.plans = TestPlans(self.connection, self.data["id"])

            
    def create(self):
        raise NotImplemented("TODO")
            
    def __getattr__(self, attr):
        if attr == "tc_counter":
            return self._parse_and_update(attr, int)
        if attr in ['opt', 'options']:
            return self._parse_and_update('opt', Options.create)
        return super(Project, self).__getattr__(attr)
