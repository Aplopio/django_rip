class DefaultAuthentication(object):
    def __init__(self, resource):
        self.resource = resource

    def authenticate(self, request):
        return request
