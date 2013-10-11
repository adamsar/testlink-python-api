"""
All code concerning test plans in the database
"""

from testlink.resource.base import ResourceCollection, ResourceInstance
from testlink.resource.builds import TestBuilds
from testlink.resource.cases import TestCases
from testlink.exception.base import TestLinkException
from testlink.common import args

class TestPlans(ResourceCollection):
    COLLECTION = "getProjectTestPlans"

    def __init__(self, connection, project_id):
        super(TestPlans, self).__init__(connection)
        self.project_id = project_id

    def _make_cursor(self):
        return map(lambda results: TestPlan(self.connection,
                                           project_id=self.project_id,
                                           **results),
                   self.connection.request(self.COLLECTION, {
                       args.PROJECT_ID: self.project_id
                       }))

    def get(self, _id=None, name=None , project_id=None):
        if not _id and not name:
            raise TestLinkException("Looking up a plan requires an id or name")
        if not project_id and not self.project_id:
            raise TestLinkException("Need a project id to look up a plan")

        if _id:
            predicate = lambda x: x.id == _id
        else:
            predicate = lambda x: x.name == name
            
        self.project_id = project_id or self.project_id
        refresh = bool(project_id)
        for plan in self.cursor(refresh=refresh):
            if predicate(plan):
                return plan
        raise KeyError("No such plan {} for project {}".format(name,
                                                               project_id))


class TestPlan(ResourceInstance):
    """
    A plan within a project. Fields are:
    ['active',
    'id',
    'is_public',
    'name',
    'notes',
    'testproject_id']
    """

    __flags__ = [
        'active',
        'is_public'
        ]

    def __init__(self, connection, project_id=None, **data):
        super(TestPlan, self).__init__(connection, **data)        
        self.project_id = project_id
        if 'id' in data:
            self.builds = TestBuilds(connection, plan_id=data['id'])
            self.cases = TestCases(connection, plan_id=data['id'])
    

    def create(self):
        raise NotImplemented("TODO")
