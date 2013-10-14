from testlink.resource.base import ResourceCollection, ResourceInstance
from testlink.resource.cases import TestCaseAccess
from testlink.common import args


class TestBuilds(ResourceCollection):
    COLLECTION = 'getBuildsForTestPlan'
    LATEST = 'getLatestBuildForTestPlan'

    def __init__(self, connection, plan_id):
        super(TestBuilds, self).__init__(connection)
        self.plan_id = plan_id

    def _make_build(self, **results):
        return TestBuild(self.connection, plan_id=self.plan_id, **results)
        
    def _make_cursor(self):
        return map(lambda results: self._make_build(**results),
                    self.connection.request(self.COLLECTION, params={
                        args.PLAN_ID: self.plan_id
                        })
                    )

    def get(self, _id):
        for build in self.cursor:
            if build.id == _id:
                return build
        raise KeyError("No build with id {}".format(_id))

    
    def latest(self):
        params = {args.PLAN_ID: self.plan_id}
        results = self.connection.request(self.LATEST, params=params)
        return self._make_build(**results)
    


class TestBuild(ResourceInstance, TestCaseAccess):
    """
    A build in a plan to run test cases against
    keys are:
    ['active',
    'closed_on_date',
    'id',
    'is_open',
    'name',
    'notes',
    'release_date',
    'testplan_id']
    """

    __flags__ = [
        'active',
        'is_open'
        ]

    def __init__(self, connection, plan_id=None, **data):
        super(TestBuild, self).__init__(connection, **data)
        self.plan_id = plan_id
        if 'id' in data:
            self.build_id = data['id']
            

    def create(self):
        raise NotImplemented("TODO")

    
class TestBuildAccess(object):
    
    @property
    def _should_build_builds(self):
        _builds = getattr(self, '_builds', None)
        if not _builds:
            return True
        return _builds.plan_id != getattr(self, 'plan_id', None)

    
    @property
    def builds(self):
        if self._should_build_builds:
            self._builds = self.get_builds(getattr(self, 'plan_id'))
        return self._builds

    
    def get_builds(self, plan_id):
        return TestBuilds(self.connection, plan_id)
