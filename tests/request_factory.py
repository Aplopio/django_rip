from rip.request import Request


def get_request(data=None, user=None, request_params=None,
                context_params=None, crud_action=None):
    request_params = request_params or {}
    context_params = context_params or {
        'protocol': 'http',
        'timezone': 'Asia/Calcutta',
        'crud_action': crud_action}
    return Request(user=user, request_params=request_params,
                   context_params=context_params, data=data)
