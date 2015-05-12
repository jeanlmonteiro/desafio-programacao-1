# -*- coding: utf-8 -*-
import unittest

import models


class TestModelMerchant(unittest.TestCase):

    def test_repr(self):
        merchant = models.Merchant(id=1, name='Xpto')
        self.assertEqual(str(merchant), 'Merchant 1: Xpto')


class TestModelSale(unittest.TestCase):

    def test_repr(self):
        sale = models.Sale(id=1, unit_price=1, count=1)
        self.assertEqual(str(sale), 'Sale 1: 1.0')

    def test_total(self):
        sale = models.Sale(id=1, unit_price=1.25, count=2)
        self.assertEqual(sale.total, 2.5)


class TestModelUpload(unittest.TestCase):

    def test_repr(self):
        upload = models.Upload(id=1, name='Xpto')
        self.assertEqual(str(upload), 'Upload 1: 0.0')

    def test_add_sale(self):
        upload = models.Upload(id=1, name='Xpto')
        
        sale1 = models.Sale(id=1, unit_price=1.25, count=2)
        upload.add_sale(sale1)
        
        sale2 = models.Sale(id=2, unit_price=1.25, count=2)
        upload.add_sale(sale2)
        
        self.assertEqual(upload.total, 5.0)


if __name__ == '__main__':
    unittest.main()
