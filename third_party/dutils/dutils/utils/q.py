import arrow


from urllib import parse
from django.db.models.fields import DateField, BooleanField, NullBooleanField
from rest_framework.exceptions import ValidationError
from rest_framework.filters import BaseFilterBackend
from django.conf import settings


class DutilFilterBackend(BaseFilterBackend):
    identifier_filed = "q"
    list_operation = ("in",)
    all_operations = "lt", "lte", "gt", "gte", "contains", "icontains", "startswith", "endswith", "in", "date"

    def _init(self, request, queryset, view):
        self.request = request
        self.query = queryset
        self.view = view

    @property
    def filter_fields(self):
        return self.view.dutils_filter_fields if hasattr(self.view, "dutils_filter_fields") else []

    @property
    def order_by(self):
        if hasattr(self.view, 'ordering_fields'):
            return ','.join(self.view.ordering_fields)
        return self.request.query_params.get("order_by", "-pk")

    @property
    def query_params(self):
        query_params = dict()
        pre_field = None
        for raw in self.request.query_params.getlist(self.identifier_filed):
            operations = [x for x in raw.split(",") if len(x) != 0]
            for operation in operations:
                r = operation.split("=")
                if len(r) != 2:
                    query_params[pre_field] += ",{}".format(operation)
                    continue
                pre_field = r[0].strip()
                query_params[r[0].strip()] = r[1].strip()
        if hasattr(self.view, "process_query_params"):
            func = getattr(self.view, "process_query_params")
            if func and callable(func):
                query_params = func(query_params)
        return query_params

    def is_list_operation(self, param):
        return param.split("__")[-1] in self.list_operation

    @classmethod
    def get_query_kwargs(cls, param):
        """
        >>>"id__get=3"
        >>>{"id_get": 3}
        """
        left, right = param.split("=")
        return {left: right}

    def filter_queryset(self, request, queryset, view):
        self._init(request, queryset, view)
        return self.get_filter_queryset()

    def is_valid_param(self, param):
        field = "__".join(param.split("__")[:-1]).strip("^").strip("__")
        field = field or param
        may_op = param.split("__")[-1]
        if may_op in self.all_operations:
            tem = field
            field = "__".join(field.split("__")[:-1]).strip("^").strip("__")
            field = field or tem
        return field.strip() in self.filter_fields or field.split("__")[0] in self.filter_fields

    def get_model(self):
        return self.query.model

    def get_model_field(self, field_name, model):
        return model._meta.get_field(field_name)

    def get_last_field(self, field):
        res = field.split("__")
        cur_model = self.get_model()
        last_field = None
        if res[-1] in self.all_operations:
            res = res[:-1]
        for index, name in enumerate(res):
            print(index, name, last_field)
            try:
                if isinstance(last_field, DateField) and name == 'date':
                    last_field = last_field
                else:
                    last_field = self.get_model_field(name, cur_model)
                if hasattr(last_field, "related_model") and last_field.related_model:
                    cur_model = last_field.related_model
            except Exception as e:
                print(e)
                last_field = None
        return last_field

    def _validate_value(self, model_field, value):
        try:
            model_field.to_python(value)
        except Exception as e:
            raise ValidationError(str(e))


    def _process_value(self, field_name, value):
        model_field = self.get_last_field(field_name)
        if not model_field:
            return parse.unquote(parse.unquote(value)) if isinstance(value, str) else value
        if isinstance(model_field, (BooleanField, NullBooleanField)):
            if value == 'true':
                value = True
            elif value == 'false':
                value = False
        elif isinstance(model_field, DateField):
            to_date = "__date" in field_name
            try:
                time_value = arrow.get(value).replace(tzinfo=settings.TIME_ZONE).to("utc")
                value = time_value.date() if to_date else time_value.datetime
            except Exception as e:
                raise Exception("%s is an valid time format" % value)
        value = parse.unquote(parse.unquote(value)) if isinstance(value, str) else value
        self._validate_value(model_field, value)
        return value

    def get_filter_queryset(self):
        query = self.query
        query_params = self.query_params
        filter_fields = dict()
        for field, value in query_params.items():
            if not str(field).startswith("^") and self.is_valid_param(field):
                filter_fields[field] = self._process_value(field, value)
        exclude_fields = {field.strip("^"): self._process_value(field, value) for field, value in query_params.items()
                          if
                          str(field).startswith("^") and self.is_valid_param(field)}
        order_bys = self.order_by.split(",")

        # filter
        for field, value in filter_fields.items():
            if self.is_list_operation(field):
                value = value.split("|")
            query = query.filter(**{field: value})

        # exclude filter
        for field, value in exclude_fields.items():
            if self.is_list_operation(field):
                value = value.split("|")
            query = query.exclude(**{field: value})

        # order_by
        query = query.order_by(*order_bys)
        func = getattr(self.view, "custom_filter") if hasattr(self.view, "custom_filter") else None
        if func and callable(func):
            query = func(query, query_params)
        try:
            print(query.query)
        except Exception as e:
            pass
        return query


