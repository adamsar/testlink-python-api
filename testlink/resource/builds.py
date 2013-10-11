from testlink.resource.base import ResourceCollection, ResourceInstance
from testlink.exception.base import TestLinkException
from testlink.common import args


class TestBuilds(ResourceCollection):
    COLLECTION = 'getBuildsForTestPlan'
    LATEST = 'getLatestBuildForTestPlan'

    def __init__(self, connection, plan_id):
        super(TestBuilds, self).__init__(connection)
        self.plan_id = plan_id

        
    def _make_cursor(self):
        return map(lambda results: TestBuild(self.connection,
                                             plan_id=self.plan_id,
                                             **results),
                    self.connection.request(self.COLLECTION, params={
                        args.PLAN_ID: self.plan_id
                        })
                    )

    def _exists_or_raise(self, plan_id):
        if not plan_id and not self.plan_id:
            raise TestLinkException("Require plan id to look up test builds")
        self.plan_id = plan_id or self.plan_id
    

    def get(self, _id, plan_id=None):
        self._exists_or_raise(plan_id)
        for build in self.cursor:
            if build.id == _id:
                return build
        raise KeyError("No build with id {}".format(_id))

    
    def latest(self, plan_id=None):
        self._exists_or_raise(plan_id)
        params = {args.PLAN_ID: self.plan_id}
        results = self.connection.request(self.LATEST, params=params)
        return TestBuild(self.connection,
                         plan_id = self.plan_id,
                         **results)
    


class TestBuild(ResourceInstance):
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

    def create(self):
        raise NotImplemented("TODO")
