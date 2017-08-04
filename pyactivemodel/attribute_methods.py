# -*- coding: UTF-8 -*-

from functools import wraps
from pyactivemodel.base import ActiveModelBase


def _make_wrapper(target, attribute):
    @wraps(target)
    def wrapper_inner(self, *args, **kwargs):
        return target(self, attribute, *args, **kwargs)
    return wrapper_inner


class AttributeMethodsMixin(metaclass=ActiveModelBase):
    @classmethod
    def classinit_include(cls):
        cls.attribute_method_matchers = []

    @classmethod
    def classinit_include_post(cls):
        del cls.attribute_method_matchers

    @classmethod
    def attribute_method_prefix(cls, *args):
        for arg in args:
            cls.attribute_method_matchers.append(lambda attr: arg+attr)

    @classmethod
    def attribute_method_suffix(cls, *args):
        for arg in args:
            cls.attribute_method_matchers.append(lambda attr: attr+arg)

    @classmethod
    def define_attribute_methods(cls, *args):
        for matcher in cls.attribute_method_matchers:
            target = getattr(cls, matcher('attribute'))
            for attribute in args:
                setattr(cls, matcher(attribute),
                        _make_wrapper(target, attribute))

        cls.attribute_method_matchers = []
