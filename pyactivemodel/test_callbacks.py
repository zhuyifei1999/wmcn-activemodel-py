# -*- coding: UTF-8 -*-

from pyactivemodel.callbacks import CallbacksMixin


class Person(CallbacksMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.define_model_callbacks('update')
        self.before_update(self.reset_me)

    def update(self):
        @self.run_callbacks('update')
        def inner():
            print('inner executed')

    def reset_me(self):
        print('reset_me executed')


person = Person()
person.update()
