from typing import List

from django.db import models
from typing import List

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor
from transitions.extensions import HierarchicalMachine as Machine


class StateMachineModel(models.Model):
    __states__ = (
        ('initial', "Initial"),
    )

    __transitions__ = []  # transitions
    __state_children_mapping__ = dict()  # state name, rel
    __initial_state__ = 'pending'  # init state

    status = models.CharField(max_length=32, verbose_name="Status", default='initial', choices=__states__)

    class Meta:
        abstract = True

    @property
    def state(self):
        return self.status

    @state.setter
    def state(self, value):
        self.status = value

    def __init__(self, *args, **kwargs):
        super(StateMachineModel, self).__init__(*args, **kwargs)
        machine = Machine(model=self,
                          states=self._get_init_states(),
                          transitions=self._get_init_transitions(),
                          initial=self.get_initial_state())
        setattr(self, 'fsm', machine)
        setattr(self, "fsm", machine)

    def get_initial_state(self):
        if self.status not in self._get_states():
            return self.__initial_state__
        return self.status

    @classmethod
    def get_states(cls) -> List:
        return list(dict(cls.__states__).keys())[:]

    @classmethod
    def _get_states(cls):
        states = cls.get_states()
        for state, rel_name in cls.__state_children_mapping__.items():
            _descriptor = getattr(cls, rel_name)
            assert isinstance(_descriptor, ReverseOneToOneDescriptor), '%s must be onetoone field' % rel_name
            child_model = _descriptor.related.field.model
            for child_state in child_model.get_states():
                states.append("%s_%s" % (state, child_state))
        return states

    def _get_init_states(self):
        states = self.get_states()
        _cls = type(self)
        for state, rel_name in self.__state_children_mapping__.items():
            states.remove(state)
            try:
                obj = getattr(self, rel_name)
            except ObjectDoesNotExist as e:
                relation = getattr(_cls, rel_name)
                assert isinstance(relation, ReverseOneToOneDescriptor), '%s must be onetoone field' % rel_name
                remote_model = relation.related.field.model
                assert issubclass(remote_model,
                                  StateMachineModel), "%s must be an StateMachineModel" % remote_model.__name__
                obj = remote_model()
                setattr(obj, _cls.__name__, self)
            state_dict = {"name": state, "children": obj.fsm}
            states.append(state_dict)
        return states

    def _get_init_transitions(self):
        return self.__transitions__
