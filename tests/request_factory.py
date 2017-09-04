from rip.request import Request


def get_request(data=None,
                user=None,
                request_params=None,
                context_params= None):
    request_params = request_params or {}
    context_params = context_params or {'api_name': 'api',
                                        'api_version': 'v2',
                                        'url':'asdf/1212',
                                        'endpoint': 'test_endpoint',
                                        'timezone': 'Asia/Calcutta'}
    return Request(user=user,
                   request_params=request_params,
                   context_params=context_params,
                   data=data)
