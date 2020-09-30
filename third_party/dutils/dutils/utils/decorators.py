import time
from functools import wraps

from dutils.exceptions import RequestQueryParamsMissing


def class_method_retry(times, errors=(Exception,), delay=None):
    """when specific error occurs, retry specific times after sleep seconds
    :param times: retry times
    :param errors: errors when raise, will retry
    :param delay: delay seconds
    :return: func after decratored
    """

    def deco(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            is_error = True
            retry_times = times
            while retry_times > 0 and is_error:
                try:
                    ret = func(self, *args, **kwargs)
                    return ret
                except errors as e:
                    retry_times -= 1
                    if retry_times == 0:
                        raise e
                    hook = getattr(self, "retry_hook", None)
                    if hook and callable(hook):
                        hook(*args, **kwargs)
                    if delay and isinstance(delay, int):
                        time.sleep(delay)
            return None

        return wrapper

    return deco


def viewset_url_params_require(mandatory_params: list):
    """
    :param mandatory_params: mandatory params
    :return: func after decratored
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            for args_name in mandatory_params:
                mandatory = dict()
                value = self.request.query_params.get(args_name, None)
                if value is None:
                    raise RequestQueryParamsMissing(format_kwargs=dict(param=args_name))
                else:
                    mandatory[args_name] = value
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
