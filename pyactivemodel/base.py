# -*- coding: UTF-8 -*-

noop = lambda *args, **kwargs: None  # noqa: E731


class ActiveModelBase(type):
    def __new__(metacls, name, bases, namespace, **kwargs):
        """Create the new class, run classinit_includes."""
        cls = super().__new__(metacls, name, bases, namespace)

        for classes in reversed(cls.__mro__):
            classes.__dict__.get('classinit_include', noop).__get__(None, cls)()
        for classes in cls.__mro__:
            classes.__dict__.get('classinit_include_post', noop).__get__(None, cls)()

        return cls
