# -*- coding: utf-8 -*-

from copy import deepcopy
from error.errors import BaseError


class ModuleBaseMethod:
    typeof = None

    def __init__(self, name, data, null=False, empty=False, option=None):
        self.key = name
        self.data = data
        self.null = null
        self.empty = empty
        self.option = option

    def is_null(self):
        if not self.null:
            if self.data is None:
                return False
            else:
                return True
        else:
            return True

    def is_empty(self):
        pass

    def is_instance(self):
        return isinstance(self.data, self.typeof)

    def validate(self):
        if not self.is_null and not self.is_instance():
            return False
        if not self.is_null():
            return False
        if not self.is_empty():
            return False
        if callable(self.option) and self.option(self.key, self.data):
            return False

        return True

    def check(self):
        if not self.validate():
            code = 'InvalidParameter.{key}'.format(key=self.key)
            message = 'The parameter "{key}" do not match the specification'.format(key=self.key)
            raise BaseError(code=code, message=message)

    @property
    def value(self):
        return self.data


class StringModule(ModuleBaseMethod):
    typeof = str

    def is_empty(self):
        if not self.empty and len(self.data) == 0:
            return False
        else:
            return True


class IntModule(ModuleBaseMethod):
    typeof = int

    def is_empty(self):
        if not self.empty and self.data == 0:
            return False
        else:
            return True


class DictModule(ModuleBaseMethod):
    typeof = dict

    def is_empty(self):
        if not self.empty and self.data == {}:
            return False
        else:
            return True


class ListModule(ModuleBaseMethod):
    typeof = list

    def is_empty(self):
        if not self.empty and len(self.data) == 0:
            return False
        else:
            return True


class ObjectIterableModule(ModuleBaseMethod):
    typeof = dict

    def __init__(self, name, data, is_copy=False, null=False, empty=False, option=None):
        self.is_copy = is_copy
        super(ObjectIterableModule, self).__init__(name, data, null, empty, option)

    def is_empty(self):
        if not self.empty and self.data == {}:
            return False
        else:
            return True

    def check(self):
        super(ObjectIterableModule, self).check()
        for _, v in self.data.items():
            v.check()

        return True

    @property
    def value(self):
        data = {}
        for _, v in self.data.items():
            data[v.key] = v.value
        if self.is_copy:
            data = deepcopy(data)
        return data


class ListIterableModule(ModuleBaseMethod):
    typeof = list

    def __init__(self, name, data, is_copy=False, null=False, empty=False, option=None):
        self.is_copy = is_copy
        super(ListIterableModule, self).__init__(name, data, null, empty, option)

    def is_empty(self):
        if not self.empty and len(self.data) == 0:
            return False
        else:
            return True

    def check(self):
        super(ListIterableModule, self).check()
        for v in self.data:
            v.check()

        return True

    @property
    def value(self):
        data = []
        for v in self.data:
            data.append(v.value)
        if self.is_copy:
            data = deepcopy(data)
        return data


if __name__ == "__main__":
    import pprint
    k2 = ObjectIterableModule(name='K2', data={
        'SourceType': StringModule(name='SourceType', data='dasfasdf'),
        'Duration': IntModule(name='Duration', data=0, empty=True),
        'TargetUrls': ListModule(name='TargetUrls', data=[], empty=True),
        'List': ListIterableModule(name='List', data=[
            StringModule(name='SourceType', data='dasfasdf'),
            IntModule(name='Duration', data=3600, empty=True),
            ListModule(name='TargetUrls', data=[1, 2, 3, 4]),
            ObjectIterableModule(name='K2', data={
                'SourceType': StringModule(name='SourceType', data='dasfasdf'),
                'Duration': IntModule(name='Duration', data=0, empty=True),
                'TargetUrls': ListModule(name='TargetUrls', data=[], empty=True),
                'List': ListIterableModule(name='List', data=[
                    StringModule(name='SourceType', data='dasfasdf'),
                    IntModule(name='Duration', data=3600, empty=True),
                    ListModule(name='TargetUrls', data=[1, 2, 3, 4])
                ])
            })
        ])
    })
    try:
        print(k2.check())
    except Exception as e:
        print(e.message)
    pprint.pprint(k2.value)

    k3 = ListIterableModule(name='K3', data=[
        StringModule(name='SourceType', data='dasfasdf'),
        IntModule(name='Duration', data=3600, empty=True),
        ListModule(name='TargetUrls', data=[1, 2, 3, 4]),
        ObjectIterableModule(name='K3_2', data={})
    ])
    try:
        print(k3.check())
    except Exception as e:
        print(e.code, e.message)
    # print(k3.check())
    print(k3.value)
    import time
    print(time.time())



