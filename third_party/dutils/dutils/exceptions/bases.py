from django.utils.translation import gettext_lazy as _
from rest_framework.utils import json

jsonify = json.dump


def api_response(rs, status=400):
    return (jsonify(rs), status) if rs['code'] != 1000 else jsonify(
        rs.get("data", ''))


class HMTBaseException(Exception):
    code = 1001
    status = 400
    message = ''
    translate_format_keys = True

    def __init__(self, message=None, format_kwargs=None, *args, **kwargs):
        if not format_kwargs:
            format_kwargs = dict()
        if message is not None:
            self.message = message

        self._message = self.message
        self.message = self.message % format_kwargs

        self.format_params = format_kwargs

    def __str__(self):
        return self.message

    def __unicode__(self):
        return self.as_text()

    def json_response(self):

        return {
            'code': self.code,
            'message': self.as_text()
        }

    def as_text(self):
        if not self.format_params or not isinstance(self.format_params, dict):
            format_kwargs = {}
        else:
            if self.translate_format_keys:
                format_kwargs = dict((key, _(value)) for key, value in self.format_params.items())
            else:
                format_kwargs = self.format_params
        return _(self._message, **format_kwargs)


class SystemException(HMTBaseException):
    code = 3000
    message = "System error"


