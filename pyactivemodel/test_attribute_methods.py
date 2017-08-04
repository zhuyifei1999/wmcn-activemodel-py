# -*- coding: UTF-8 -*-

from pyactivemodel.attribute_methods import AttributeMethodsMixin


class Person(AttributeMethodsMixin):
    @classmethod
    def classinit_include(cls):
        cls.attribute_method_prefix('reset_')
        cls.attribute_method_suffix('_is_highest')
        cls.define_attribute_methods('age')

    def reset_attribute(self, attribute):
        setattr(self, attribute, 0)

    def attribute_is_highest(self, attribute):
        return getattr(self, attribute) > 100


person = Person()
person.age = 110
assert person.age_is_highest() is True
person.reset_age()
assert person.age_is_highest() is False
