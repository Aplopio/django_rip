from rip.generic_steps import error_types


class Response(object):
    def __init__(self, is_success=True, reason=None, data=None):
        """
        :param is_success:
        :param reason: required if is_success is False
        :param data: supporting data. In case of success, this can be the
            data to be returned. For error responses, data contains additional
            details about the failure
        :return:
        """
        self.is_success = is_success
        self.reason = reason
        self.data = data


class NotFoundResponse(Response):
    def __init__(self, data=None):
        super(NotFoundResponse, self).__init__(
            is_success=False, reason=error_types.ObjectNotFound, data=data)


class ActionForbiddenResponse(Response):
    def __init__(self, data=None):
        super(ActionForbiddenResponse, self).__init__(
            is_success=False, reason=error_types.ActionForbidden, data=data)
