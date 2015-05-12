# -*- coding: utf-8 -*-
import decimal


class RepositoryBase(object):
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def session(self):
        return self.cursor

    def commit(self):
        self.conn.commit()

    def create(self, item):
        self.commit()
        item.id = self.session().lastrowid
        return item

    def save(self, item):
        self.commit()
        if self.session().rowcount:
            return True
        return False


class MerchantRepository(RepositoryBase):
    def create(self, merchant):
        self.session().execute('''
            INSERT OR REPLACE INTO merchants (name, address, id)
                VALUES ( ?, ?, (
                    SELECT id FROM merchants WHERE name=? AND address=?
                )
            )
        ''', ( merchant.name, merchant.address,
               merchant.name, merchant.address,))
        return super(MerchantRepository, self).create(merchant)


class SaleRepository(RepositoryBase):
    def create(self, sale):
        self.session().execute(
            'INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?)',
            (None, sale.upload.id, sale.merchant.id, sale.purchaser_name,
             sale.description, decimal.Decimal(sale.unit_price), sale.count)
        )
        return super(SaleRepository, self).create(sale)


class UploadRepository(RepositoryBase):
    def create(self, upload):
        from datetime import datetime
        if not upload.created_at:
            upload.created_at = datetime.now()

        self.session().execute(
            'INSERT INTO uploads VALUES (?, ?, ?)',
            (None, decimal.Decimal(upload.total), upload.created_at)
        )
        return super(UploadRepository, self).create(upload)

    def save(self, upload):
        self.session().execute(
            'UPDATE uploads SET total=?, created_at=? WHERE id=?',
            (decimal.Decimal(upload.total), upload.created_at, upload.id)
        )
        return super(UploadRepository, self).save(upload)


def init_db(conn):
    cur = conn.cursor()

    create_merchants = """
        CREATE TABLE IF NOT EXISTS merchants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            address VARCHAR(200));
    """
    cur.execute(create_merchants)

    create_uploads = """
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total DECIMAL(5,2),
            created_at DATETIME);
    """
    cur.execute(create_uploads)

    create_sales = """
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            upload_id INTEGER,
            merchant_id INTEGER,
            purchaser_name VARCHAR(200),
            description VARCHAR(200),
            unit_price DECIMAL(5,2),
            count INTEGER);
    """
    cur.execute(create_sales)

    conn.commit()
