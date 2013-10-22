from testlink.resource.base import ResourceCollection, ResourceInstance
from testlink.resource.cases import TestCaseAccess
from testlink.common import args
from testlink.exception.base import TestLinkException


class TestBuilds(ResourceCollection):
    COLLECTION = 'getBuildsForTestPlan'
    LATEST = 'getLatestBuildForTestPlan'
    CREATE = 'createBuild'

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

    def get(self, _id=None, name=None):
        if not _id and not name:
            raise TestLinkException("An id or name is required to retrieve a build")
        if _id:
            predicate = lambda build: build.id == _id
        else:
            predicate = lambda build: build.name == name
            
        for build in self.cursor:
            if predicate(build):
                return build
            
        raise KeyError("Unable to find build with specified criteria")
    

    
    def latest(self):
        params = {args.PLAN_ID: self.plan_id}
        results = self.connection.request(self.LATEST, params=params)
        return self._make_build(**results)

    
    def create(self, name, notes=None):
        """
        Creates a new test build for the associated
        test plan with the name and notes given
        """
        params = {
            args.PLAN_ID: self.plan_id,
            args.BUILD_NAME: name
            }
        if notes:
            params[args.BUILD_NOTES] = notes
        return self.connection.request(self.CREATE, params=params)
    


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
