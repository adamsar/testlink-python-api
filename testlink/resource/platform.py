"""
Platforms for reporting test executions in
"""
from testlink.resource.base import ResourceCollection, ResourceInstance
from testlink.exception.base import TestLinkException
from testlink.common import args

class TestPlatforms(ResourceCollection):
    COLLECTION = 'getTestPlanPlatforms'
    
    def __init__(self, collection, plan_id):
        super(TestPlatforms, self).__init__(collection)
        self.plan_id = plan_id

    def _make_cursor(self):
        if not self.plan_id:
            raise TestLinkException("plan_id required for looking up platforms")
        results = self.connection.request(self.COLLECTION,
                                          params={args.PLAN_ID: self.plan_id})
        return map(lambda data: TestPlatform(self.connection, self.plan_id, **data),
                   results)
        

class TestPlatform(ResourceInstance):
    """
    A platform to test against.
    Contains keys:
    ['id', 'name', 'notes']
    """

    def __init__(self, connection, plan_id = None, **data):
        super(TestPlatform, self).__init__(connection, **data)
        self.plan_id = plan_id
        if 'id' in data:
            self.platform_id = data['id']

class TestPlatformAccess(object):

    def _should_build_platforms(self):
        _platforms = getattr(self, '_platforms', None)
        if not _platforms:
            return True
        return _platforms.plan_id != self.plan_id

    @property
    def platforms(self):
        if self._should_build_platforms:
            self._platforms = self.get_platforms(getattr(self, 'plan_id'))
        return self._platforms

    def get_platforms(self, plan_id):
        return TestPlatforms(self.connection, plan_id)
