# -*- coding: UTF-8 -*-

from pyactivemodel.base import ActiveModelBase
from pyactivemodel.attribute_methods import AttributeMethodsMixin


class DirtyMixin(AttributeMethodsMixin, metaclass=ActiveModelBase):
    @classmethod
    def classinit_include(cls):
        cls.attribute_method_suffix(
            '_has_changed', '_change', '_will_change', '_was')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.changes_applied()

    def changes_applied(self):
        self.changed_attributes = {}

    @property
    def has_changed(self):
        return bool(self.changed_attributes)

    @property
    def changed(self):
        return list(self.changed_attributes)

    @property
    def changes(self):
        return {key: (val, getattr(self, key))
                for key, val in self.changed_attributes.items()}

    @property
    def attribute_has_changed(self, attribute):
        return attribute in self.changed_attributes

    @property
    def attribute_was(self, attribute):
        return self.changed_attributes[attribute]

    @property
    def attribute_change(self, attribute):
        if attribute in self.changed_attributes:
            return self.changed_attributes[attribute], getattr(self, attribute)
        else:
            return None

    def attribute_will_change(self, attribute):
        if attribute not in self.changed_attributes:
            self.changed_attributes[attribute] = getattr(self, attribute, None)
