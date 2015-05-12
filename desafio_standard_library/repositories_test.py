# -*- coding: utf-8 -*-
import unittest
import sqlite3

import models
import repositories


class DBTestCase(unittest.TestCase):
    def setUp(self):
        import decimal

        def adapt_decimal(val):
            return float(str(val))
        sqlite3.register_adapter(decimal.Decimal, adapt_decimal)

        def convert_decimal(s):
            return decimal.Decimal(s)
        sqlite3.register_converter('decimal', convert_decimal)

        self.conn = sqlite3.connect('desafio1_test.db',
                            detect_types=sqlite3.PARSE_DECLTYPES)
        repositories.init_db(self.conn)


class TestMerchantRepository(DBTestCase):

    def test_create(self):
        merchant = models.Merchant(name='Jack', address='123 Fake St')
        self.assertIsNone(merchant.id)
        merchant = repositories.MerchantRepository(self.conn).create(merchant)
        self.assertIsNotNone(merchant.id)


class TestUploadRepository(DBTestCase):

    def test_create(self):
        upload = models.Upload()
        self.assertIsNone(upload.id)
        upload = repositories.UploadRepository(self.conn).create(upload)
        self.assertIsNotNone(upload.id)

    def test_save(self):
        upload = models.Upload()
        upload = repositories.UploadRepository(self.conn).create(upload)
        upload.total = 34.5
        self.assertTrue(repositories.UploadRepository(self.conn).save(upload))


class TestSaleRepository(DBTestCase):

    def test_create(self):
        merchant = models.Merchant(id=1)
        upload = models.Upload(id=1)
        sale = models.Sale(
            upload=upload,
            merchant=merchant,
            purchaser_name='Snake Plissken',
            description='R$20 Sneakers for R$5',
            unit_price=1.25,
            count=1
        )
        self.assertIsNone(sale.id)
        sale = repositories.SaleRepository(self.conn).create(sale)
        self.assertIsNotNone(sale.id)
