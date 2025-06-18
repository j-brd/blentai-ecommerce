class InvalidTokenError(Exception):
    """Le token est invalide (format, signature, exp...)."""
    pass

class UserNotFoundError(Exception):
    """L'utilisateur du token n'existe plus en base."""
    pass