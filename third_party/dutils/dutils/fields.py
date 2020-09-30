from django.http import Http404
from rest_framework.fields import empty
from rest_framework.utils import html

from rest_framework.fields import Field


class NestedModelField(Field):
    """
    Usage::
        from django.db import models
        from rest_framework.serializers import ModelSerializer
        class User(models.Model):
            username = models.CharField(_('username'),max_length=150,unique=True)

        class Email(models.Model):
            user = models.ForeignKey(User, on_delete=models.PROTECT)

        class EmailSerializer(ModelSerializer):
            username = models.CharField(_('email'),max_length=150,unique=True)
            user = NestedModelField(model=User, lookup_field="id", lookup_field_name="user_id")
            class Meta:
                model = "user", "username"
        data = {"user_id": 1, "email": "someone@email.com"}
        ss = EmailSerializer(data)
        ss.is_valid()
        email = ss.save()
        >> email, email.user
        <Email "someone@email.com">, <User 1>
    """
    def __init__(self, model, lookup_field, lookup_field_name=None, many=False, read_only=False, write_only=False,
                 required=None, default=empty, initial=empty, source=None,
                 label=None, help_text=None, style=None,
                 error_messages=None, validators=None, allow_null=False):
        # if not found, raise 404
        """
        :param lookup_field:
        :param lookup_field_name: file name in serializer data
        :param many: set many True to receive  a list
        """
        assert hasattr(model, lookup_field)
        self._model = model
        self._lookup_field = lookup_field
        self._many = many
        self.lookup_field_name = lookup_field_name
        super(NestedModelField, self).__init__(read_only=read_only, write_only=write_only,
                                               required=required, default=default, initial=initial, source=source,
                                               label=label, help_text=help_text, style=style,
                                               error_messages=error_messages, validators=validators,
                                               allow_null=allow_null)

    def get_model(self):
        return self._model

    def is_many(self):
        return self._many

    def get_lookup_field(self):
        return self._lookup_field

    def to_internal_value(self, data):
        if self.is_many():
            res = []
            for x in data:
                filter_condition = {
                    self.get_lookup_field(): x
                }
                obj = self.get_model().objects.filter(**filter_condition).first()
                if not obj:
                    raise Http404
                res.append(obj)
            return res
        filter_condition = {self.get_lookup_field(): data}
        res = self.get_model().objects.filter(**filter_condition).first()
        if not res:
            raise Http404
        return res

    def to_representation(self, value):
        if self.is_many():
            return [getattr(x, self.get_lookup_field()) for x in value]
        return getattr(value, self.get_lookup_field())

    def get_value(self, dictionary):
        if self.is_many():
            dictionary = dict(dictionary)
        if html.is_html_input(dictionary):
            # HTML forms will represent empty fields as '', and cannot
            # represent None or False values directly.
            if self.field_name not in dictionary:
                if getattr(self.root, 'partial', False):
                    return empty
                return self.default_empty_html
            ret = dictionary[self.field_name]
            if ret == '' and self.allow_null:
                # If the field is blank, and null is a valid value then
                # determine if we should use null instead.
                return '' if getattr(self, 'allow_blank', False) else None
            elif ret == '' and not self.required:
                # If the field is blank, and emptiness is valid then
                # determine if we should use emptiness instead.
                return '' if getattr(self, 'allow_blank', False) else empty
            return ret
        query_name = self.lookup_field_name or self.field_name
        return dictionary.get(query_name, empty)
