# -*- coding: utf-8 -*-
import unittest

import helps


class TestHelps(unittest.TestCase):

    def test_show_price(self):
        value = helps.show_price(12345.67)
        self.assertEqual(value, 'R$ 12.345,67')


    def test_headers(self):
        headers = [('Accept', 'application/json')]
        headers = helps.headers('Hello', headers)
        result = [
            ('Accept', 'application/json'),
            ('Content-Type', 'application/json'),
            ('Content-Length', '5'),
        ]
        self.assertEqual(headers, result)

    def test_get_absolute_url_with_ssl(self):
        for environ in [{'HTTPS': 'on'}, {'HTTPS': '1'}]:
            environ.update({'HTTP_HOST': 'localhost:8000'})
            url = helps.get_absolute_url(environ, url='/upload')
            self.assertEqual(url, 'https://localhost:8000/upload')

    def test_get_absolute_url_less_ssl(self):
        for environ in [{}, {'HTTPS': 'off'}, {'HTTPS': '0'}]:
            environ.update({'HTTP_HOST': 'localhost:8000'})
            url = helps.get_absolute_url(environ, url='/upload')
            self.assertEqual(url, 'http://localhost:8000/upload')
