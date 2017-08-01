from rip.crud.crud_actions import CrudActions
from rip.generic_steps import error_types
from rip.response import Response


def validate_action(func):
    def wrapper(self, request):
        action = CrudActions.resolve_action(func.__name__)
        request.context_params['crud_action'] = action

        if not self.is_action_allowed(action):
            return Response(
                is_success=False, reason=error_types.MethodNotAllowed)
        return func(self, request=request)

    return wrapper