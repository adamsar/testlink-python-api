class ApiReturn(object):
    """
    Your basic return from the the API
    """    
    
    __flags__ = []
    
    def __init__(self, **data):
        self.data = data
        self._parsed = []

        
    def __getattr__(self, attr):
        if attr in self.__flags__:
            return self._parse_and_update(attr, bool)
        return self.data.get(attr)

    
    def _parse_and_update(self, attr, parser):
        """
        Parses an attr associate with the resource
        and saves it to the data
        """
        if attr not in self._parsed:
            value = parser(self.data.get(attr))
            self.data[attr] = value
            self._parsed.append(attr)
            
        return self.data[attr]

    
class Resource(object):
    
    def __init__(self, connection):
        self.connection = connection


class ResourceCollection(Resource):

    def __init__(self, connection):
        self.connection = connection
        self._cursor = None

        
    def _make_cursor(self):
        raise NotImplemented()


    @property
    def cursor(self):
        if not self._cursor:
            self._cursor = self._make_cursor()
        return self._cursor
    
    
class ResourceInstance(Resource, ApiReturn):

    def __init__(self, connection, **data):
        Resource.__init__(self, connection)
        ApiReturn.__init__(self, **data)
