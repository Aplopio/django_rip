"""
defines list of error response types the api may return. The value of each of
the responses should be unique but the value itself does not matter
"""

ObjectNotFound = 'ObjectNotFound'
ActionForbidden = 'ActionForbidden'
AuthenticationFailed = 'AuthenticationFailed'
InvalidData = 'InvalidData'
MethodNotAllowed = 'MethodNotAllowed'


class MultipleObjectsFound(Exception):
    pass
