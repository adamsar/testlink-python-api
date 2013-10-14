"""
All code concerning test plans in the database
"""

from testlink.resource.base import ResourceCollection, ResourceInstance
from testlink.resource.builds import TestBuildAccess
from testlink.resource.cases import TestCaseAccess
from testlink.resource.suites import TestSuiteAccess
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

    def get(self, _id=None, name=None):
        if not _id and not name:
            raise TestLinkException("Looking up a plan requires an id or name")

        if _id:
            predicate = lambda x: x.id == _id
        else:
            predicate = lambda x: x.name == name
            
        for plan in self.cursor:
            if predicate(plan):
                return plan
        raise KeyError("No such plan {} for project {}".format(name,
                                                               self.project_id))


class TestPlan(ResourceInstance, TestCaseAccess, TestBuildAccess, TestSuiteAccess):
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
            self.plan_id = data['id']
    

    def create(self):
        raise NotImplemented("TODO")

class TestPlanAccess(object):

    @property
    def _should_build_plans(self):
        _plans = getattr(self, '_plans', None)
        if not _plans:
            return True
        return _plans.project_id != getattr(self, 'project_id', None)


    @property
    def plans(self):
        if self._should_build_plans:
            self._plans = self.get_plans(getattr(self, 'project_id', None))
        return self._plans


    def get_plans(self, project_id):
        return TestPlans(self.connection, project_id)
