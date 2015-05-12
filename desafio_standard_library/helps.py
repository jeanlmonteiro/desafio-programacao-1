# -*- coding: utf-8 -*-

def show_price(value):
    import locale
    locale.setlocale(locale.LC_ALL, 'pt_BR')

    symbol = locale.localeconv().get('currency_symbol')
    value = locale.currency(value, grouping=True, symbol=False)
    return '{symbol} {value}'.format(symbol=symbol, value=value)


def headers(body, headers=[]):
    headers.append(('Content-Type','application/json'))
    headers.append(('Content-Length', str(len(body))))
    return headers


def get_absolute_url(environ, url=''):
    scheme = 'https' if environ.get('HTTPS', 'off') in ('on', '1') else 'http'
    return '{}://{}{}'.format(scheme, environ.get('HTTP_HOST'), url)
