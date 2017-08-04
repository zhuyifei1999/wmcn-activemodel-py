# -*- coding: UTF-8 -*-

import functools

from pyactivemodel.base import ActiveModelBase


def _make_wrapper(target, attr):
    if isinstance(target, property):
        fget = _make_wrapper(target.fget, attr) if target.fget else None
        fset = _make_wrapper(target.fset, attr) if target.fset else None
        fdel = _make_wrapper(target.fdel, attr) if target.fdel else None
        return property(fget, fset, fdel, target.__doc__)
    else:
        @functools.wraps(target)
        def wrapper_inner(self, *args, **kwargs):
            return target(self, attr, *args, **kwargs)
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
            cls.attribute_method_matchers.append(
                functools.partial(lambda a, b: a+b, a=arg))

    @classmethod
    def attribute_method_suffix(cls, *args):
        for arg in args:
            cls.attribute_method_matchers.append(
                functools.partial(lambda a, b: a+b, b=arg))

    @classmethod
    def define_attribute_methods(cls, *args):
        for matcher in cls.attribute_method_matchers:
            target = getattr(cls, matcher('attribute'))
            for attribute in args:
                setattr(cls, matcher(attribute),
                        _make_wrapper(target, attribute))

        cls.attribute_method_matchers = []
