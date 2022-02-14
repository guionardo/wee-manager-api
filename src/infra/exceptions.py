class StartupException(Exception):
    """Exception for missing startup setup"""
    ...


class MissingIdInModelException(Exception):
    """Not informed id field in model"""
    ...
