

class ValidationResult(object):
    def __init__(self, is_success, reason=None):
        self.is_success = is_success
        self.reason = reason
