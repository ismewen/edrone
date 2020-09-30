import traceback

from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer, raise_errors_on_nested_writes
from rest_framework.utils import model_meta


class Serializer(ModelSerializer):
    """
    add a process_initial_data method to process init data, so we can format data in serializer
    """

    def __init__(self, instance=None, data=empty, **kwarg):
        super(Serializer, self).__init__(instance=instance, data=data, **kwarg)
        if hasattr(self, "initial_data"):
            self.process_initial_data()

    def process_initial_data(self):
        pass

