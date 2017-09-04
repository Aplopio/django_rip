from rip.schema.sub_resource_field import \
    SubResourceField


class ListSubResourceField(SubResourceField):
    """`ListSubResourceField` inherits from `SubResourceField`.
    This field enables one to many relationship between the parent
    resource and the
    """

    def __init__(self, resource_cls, related_filter, required=False,
                 nullable=True, entity_attribute='id', show_in_list=True):
        super(ListSubResourceField, self).__init__(
            resource_cls, related_filter, required, nullable,
            entity_attribute, show_in_list=show_in_list)
        self.null_return_value = []

    def get_data(self, resource_obj, request):
        return resource_obj.read_list(request)

    def get_data_from_response(self, response):
        return response.data['objects']
