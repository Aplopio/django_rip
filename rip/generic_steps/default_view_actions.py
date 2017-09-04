class DefaultViewActions(object):
    request_filters_property = 'request_filters'

    def read(self, request):
        request_filters = request.context_params.get(self.request_filters_property, {})
        view_data = self.view(request, **request_filters)
        request.context_params['entity'] = view_data
        return request

    def view(self, request, **filters):
        raise NotImplementedError('You need to override the view method on actions')
