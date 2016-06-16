class DefaultViewActions(object):
    def read(self, request):
        view_data = self.view(request)
        request.context_params['entity'] = view_data
        return request

    def view(self, request):
        raise NotImplementedError('You need to override get on actions')
