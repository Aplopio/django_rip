from django_adapter.view.view_actions import ViewActions
from rip.generic_steps import error_types
from rip.response import Response


def validate_view_action(func):
    def wrapper(self, request):
        action = ViewActions.resolve_action(func.__name__)
        request.context_params['view_action'] = action

        if not self.is_action_allowed(action):
            return Response(
                is_success=False, reason=error_types.MethodNotAllowed)
        return func(self, request=request)

    return wrapper
