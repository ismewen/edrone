from .bases import SystemException


class DuplicateViewsetRegistryName(SystemException):
    code = 3001
    message = "%(registry_name)s is duplicate"


class MethodNotAllowedException(SystemException):
    code = 3002
    message = "Method is not allowed"


class SpecificViewsetNotFound(SystemException):
    code = 3003
    message = "%(registry_name)s is not found"


class SpecificObjectNotFound(SystemException):
    code = 3004
    message = "Specific object is not found"


class RequestQueryParamsMissing(SystemException):
    code = 3005
    message = "params of %(param) is mandatory"

