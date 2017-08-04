# -*- coding: UTF-8 -*-

from pyactivemodel.base import ActiveModelBase


class CallbacksMixin(metaclass=ActiveModelBase):
    @classmethod
    def classinit_include(cls):
        cls._callbacks = {}

    @classmethod
    def define_model_callbacks(cls, *args):
        for arg in args:
            cls._define_model_callbacks(arg)

    @classmethod
    def _define_model_callbacks(cls, cbname):
        cls._callbacks[cbname] = ([], [])

        @staticmethod
        def before_cbname(func):
            cls._callbacks[cbname][0].append(func)
        before_cbname.__name__ = 'before_' + cbname
        setattr(cls, before_cbname.__name__, before_cbname)

        @staticmethod
        def after_cbname(func):
            cls._callbacks[cbname][0].append(func)
        after_cbname.__name__ = 'after_' + cbname
        setattr(cls, after_cbname.__name__, after_cbname)

    @classmethod
    def run_callbacks(cls, *args):
        def wrapper_inner(block):
            for arg in args:
                for cb in cls._callbacks[arg][0]:
                    cb()
                ret = block()
                for cb in cls._callbacks[arg][1]:
                    cb()
                return ret
        return wrapper_inner
