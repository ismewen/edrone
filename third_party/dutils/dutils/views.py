import copy

from django.http import Http404
from rest_framework.viewsets import ModelViewSet
from . import exceptions


class ViewSet(ModelViewSet):
    # name, detail, description, suffix  被征用字段
    path = None
    custom_name = None
    detail_suffix = "pk"
    nested_viewsets = []
    allow_actions = ['list', 'retrieve', 'create', 'update', 'destroy']
    serializer_mapping = {}
    registry = dict()
    model = None
    enable_filter = True
    dutils_filter_fields = []

    @classmethod
    def registry_name(cls):
        return cls.__name__

    def __init_subclass__(cls, **kwargs):
        super(ModelViewSet, cls).__init_subclass__(**kwargs)
        if cls.registry_name() in cls.registry:
            raise exceptions.DuplicateViewsetRegistryName(format_kwargs=dict(registry_name=cls.registry_name()))
        cls.registry[cls.registry_name()] = cls

    # def _set_client_credentials_user(self):
    #     if isinstance(self.request.auth, AccessToken):
    #         self.request.user = self.request.auth.application.user
    #         self.request.auth = self.request.user

    def _is_method_allowed(self):
        default_actions = ['list', 'retrieve', 'create', 'update', 'destroy']
        if self.action in default_actions and self.action not in self.allow_actions:
            raise exceptions.MethodNotAllowedException()

    def initial(self, request, *args, **kwargs):
        self._is_method_allowed()
        # self._set_client_credentials_user()
        return super(ViewSet, self).initial(request, *args, **kwargs)

    def get_viewset_cls_or_404(self, registry_name):
        if registry_name not in self.registry:
            raise exceptions.SpecificViewsetNotFound(format_kwargs=dict(registry_name=registry_name))
        return self.registry.get(registry_name)

    def get_viewset_obj(self, viewset):
        if isinstance(viewset, str):
            viewset = self.get_viewset_cls_or_404(viewset)
        viewset_instance = viewset()
        viewset_instance.request = self.request
        viewset_instance.args = copy.copy(self.args)
        viewset_instance.kwargs = copy.copy(self.kwargs)
        viewset_instance.kwargs.update({"pk": self.kwargs.get("{}_pk".format(viewset_instance.custom_name))})
        return viewset_instance.get_object()

    def get_serializer_class(self):
        serializer_class = self.serializer_mapping.get(self.action)
        return serializer_class if serializer_class else super(ViewSet, self).get_serializer_class()

    def before_serializer_many(self, queryset):
        return queryset

    def get_queryset(self):
        queryset = self.model.objects.all()
        if hasattr(self, "action") and self.action == 'list':
            queryset = self.before_serializer_many(queryset)
        return queryset

    def get_object(self):
        try:
            return super(ViewSet, self).get_object()
        except Http404:
            raise exceptions.SpecificObjectNotFound()



