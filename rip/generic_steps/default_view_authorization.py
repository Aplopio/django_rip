class DefaultViewAuthorization(object):
    def authorize_read(self, request):
        return request
