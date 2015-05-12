#! /usr/bin/env python
import views


urls = [
    (r'^$', views.index),
    (r'^upload$', views.upload_list),
    (r'^upload/([0-9]+)$', views.upload_detail),
]


def app(environ, start_response):
    import re
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, callback in urls:
        match = re.search(regex, path)
        if match is not None:
            return callback(environ, start_response, *match.groups())
    return views.not_found(environ, start_response)


class DBInjection(object):
    def __init__(self, app):
        import sqlite3
        import decimal
        import repositories

        self.app = app

        def adapt_decimal(val):
            return float(str(val))
        sqlite3.register_adapter(decimal.Decimal, adapt_decimal)

        def convert_decimal(s):
            return decimal.Decimal(s)
        sqlite3.register_converter('decimal', convert_decimal)

        self.database = sqlite3.connect('desafio1.db',
                            detect_types=sqlite3.PARSE_DECLTYPES)
        repositories.init_db(self.database)

    def __call__(self, environ, start_response):
        import helps
        environ['uri'] = helps.get_absolute_url(environ)
        environ['database'] = self.database

        appiter = self.app(environ, start_response)
        for item in appiter:
            yield item

    def close(self):
        self.database.close()


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    application = DBInjection(app)

    try:
        httpd = make_server('', 8000, application)
        print "Serving on port 8000..."
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print '\nExit...'
        application.close()
