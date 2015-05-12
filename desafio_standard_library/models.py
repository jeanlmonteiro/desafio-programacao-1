# -*- coding: utf-8 -*-

class Merchant(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.address = kwargs.get('address')

    def __repr__(self):
        return 'Merchant {id}: {name}'.format(id=self.id, name=self.name)


class Sale(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.upload = kwargs.get('upload')
        self.merchant = kwargs.get('merchant')
        self.purchaser_name = kwargs.get('purchaser_name')
        self.description = kwargs.get('description')
        self.unit_price = kwargs.get('unit_price')
        self.count = kwargs.get('count')

    def __repr__(self):
        return 'Sale {id}: {total}'.format(id=self.id, total=self.total)

    @property
    def total(self):
        return round(float(self.unit_price) * int(self.count), 2)


class Upload(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.created_at = kwargs.get('created_at')
        self.total = 0.0
        self.__sales = []

    def __repr__(self):
        return 'Upload {id}: {total}'.format(id=self.id, total=self.total)

    def get_absolute_url(self):
        if self.id:
            return '/upload/{id}'.format(id=self.id)

    def add_sale(self, sale):
        self.__sales.append(sale)
        self.total += sale.total

    @property
    def sales(self):
        self.__sales
