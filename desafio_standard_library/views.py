# -*- coding: utf-8 -*-
import cgi
import json

import helps


def index(environ, start_response):
    if environ['REQUEST_METHOD'] != 'GET':
        return method_not_allowed(environ, start_response)

    body = open('templates/index.html').read()
    start_response('200 OK', [
        ('Content-type', 'text/html'),
        ('Content-Length', str(len(body)))
    ])
    return [body]


def upload_list(environ, start_response):
    if environ['REQUEST_METHOD'] != 'POST':
        return method_not_allowed(environ, start_response)

    del environ['QUERY_STRING']
    form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

    try:
        fileitem = form['filename']
    except KeyError:
        fileitem = None

    if not hasattr(fileitem, 'filename'):
        body = json.dumps({'error': 'filename is required'})
        start_response('400 BAD REQUEST', helps.headers(body))
        return [body]

    try:
        import etls
        upload = etls.upload_v1(environ['database'], fileitem)
    except Exception:
        body = json.dumps({'error': 'INTERNAL SERVER ERROR'})
        start_response('500 INTERNAL SERVER ERROR', helps.headers(body))
        return [body]

    body = json.dumps({'total': helps.show_price(upload.total)})

    url = '{}{}'.format(environ['uri'], upload.get_absolute_url())
    headers = helps.headers(body, [('Location', url)])
    start_response('201 CREATED', headers)
    return [body]


def upload_detail(environ, start_response, id):
    return method_not_allowed(environ, start_response)


def not_found(environ, start_response):
    body = json.dumps({'error': 'NOT FOUND'})
    start_response('404 NOT FOUND', helps.headers(body))
    return [body]


def method_not_allowed(environ, start_response):
    body = json.dumps({'error': 'METHOD NOT ALLOWED'})
    start_response('405 BAD REQUEST', helps.headers(body))
    return [body]
