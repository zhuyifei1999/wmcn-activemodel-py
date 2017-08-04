# -*- coding: UTF-8 -*-

from pyactivemodel.dirty import DirtyMixin


class Person(DirtyMixin):
    @classmethod
    def classinit_include(cls):
        cls.define_attribute_methods('first_name', 'last_name')

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self.first_name_will_change()
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self.last_name_will_change()
        self._last_name = value

    def save(self):
        # do save work...
        self.changes_applied()


person = Person()
assert person.has_changed is False

person.first_name = 'First Name'
assert person.first_name == 'First Name'

assert person.has_changed is True

assert person.changed == ['first_name']

assert person.changed_attributes == {'first_name': None}

assert person.changes == {'first_name': (None, 'First Name')}

assert person.first_name == 'First Name'
assert person.first_name_has_changed is True

assert person.first_name_was is None

assert person.first_name_change == (None, 'First Name')
assert person.last_name_change is None
