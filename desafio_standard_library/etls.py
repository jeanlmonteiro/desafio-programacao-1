# -*- coding: utf-8 -*-

def upload_v1(conn, fileitem):
    import csv
    import repositories
    from models import Merchant, Sale, Upload

    upload = Upload()
    upload = repositories.UploadRepository(conn).create(upload)

    for row in csv.DictReader(fileitem.file, delimiter="\t"):
        merchant = Merchant(name=row['merchant name'].decode('utf-8'),
                            address=row['merchant address'].decode('utf-8'))
        merchant = repositories.MerchantRepository(conn).create(merchant)

        sale = Sale(
            upload=upload,
            merchant=merchant,
            purchaser_name=row['purchaser name'].decode('utf-8'),
            description=row['item description'].decode('utf-8'),
            unit_price=row['item price'],
            count=row['purchase count']
        )
        sale = repositories.SaleRepository(conn).create(sale)
        upload.add_sale(sale)

    repositories.UploadRepository(conn).save(upload)

    return upload
