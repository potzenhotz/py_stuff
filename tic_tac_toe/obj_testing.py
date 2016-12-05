#!/bin/env python3

class first_obj(object):
    def __init__(self):
        self.var=5

    def change_var(self):
        self.var=6

class sec_obj(object):
    def __init__(self,an_object):
        self.test = an_object


x=first_obj()
x2=first_obj()

print(x.var, x2.var)

y=sec_obj(x)

print(y.test.var)

y.test.change_var()

print(x.var, x2.var)

