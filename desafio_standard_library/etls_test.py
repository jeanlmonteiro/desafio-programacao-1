# -*- coding: utf-8 -*-
import repositories_test
import etls


class TestUploadV1(repositories_test.DBTestCase):

    def test_upload(self):
        def _create_fs(filename):
            import cgi
            from mimetypes import MimeTypes

            with open(filename, 'r') as f:
                content = f.read()

            fs = cgi.FieldStorage()
            fs.file = fs.make_file()
            fs.type = MimeTypes().read(filename)
            fs.file.write(content)
            fs.file.seek(0)
            return fs

        fileitem = _create_fs('../example_input.tab')
        upload = etls.upload_v1(self.conn, fileitem)
        self.assertEqual(upload.total, 95.0)
