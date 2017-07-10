"""
Provides a mock database connection by intercepting calls to MySQLdb.connect() and returning
a fake class.

So far not very exhaustive mocking, but this will be expanded as the test cases are expanded.
"""

import collections

class MockDBCursor(object):
    mock_results = collections.deque([[1]])
    description = []

    def __init__(self, parentDB):
        super(MockDBCursor,self).__init__()
        self._parentDB = parentDB
    
    def __iter__(self):
        return self

    def next(self):
        if len(MockDBCursor.mock_results) == 0:
            raise StopIteration
        return MockDBCursor.mock_results.popleft()

    def execute(self,command):
        pass


class MockDBConnection(object):
    def __init__(self,**kwargs):
        super(MockDBConnection,self).__init__()
        self._kwargs = kwargs
    
    def cursor(self):
        return MockDBCursor(self)
    
    def close(self):
        pass

def connect(**kwargs):
    return MockDBConnection(**kwargs)

# Overwrite the connect function in MySQLdb so that the mock classes are
# used instead.
import MySQLdb
MySQLdb.connect = connect