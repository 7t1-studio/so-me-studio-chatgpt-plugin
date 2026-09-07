import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

spec = importlib.util.spec_from_file_location('upload_media', Path(__file__).parents[1] / 'scripts/upload_media.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class UploadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.file = Path(self.temp.name) / 'photo.png'
        self.file.write_bytes(b'actual-image-bytes')
        self.plan = [{
            'filePath': str(self.file), 'fileId': 'media-1',
            'uploadUrl': 'https://storage.example/object?signature=private',
            'mimetype': 'image/png', 'size': self.file.stat().st_size,
        }]

    def test_puts_real_bytes_with_exact_headers_and_no_oauth(self):
        connection = Mock()
        captured = {}
        def request(method, target, body, headers):
            captured.update(method=method, target=target, body=body.read(), headers=headers)
        connection.request.side_effect = request
        connection.getresponse.return_value.status = 200
        with patch.object(module.http.client, 'HTTPSConnection', return_value=connection), patch('builtins.print') as output:
            module.upload(self.plan)
        self.assertEqual(captured['method'], 'PUT')
        self.assertEqual(captured['body'], self.file.read_bytes())
        self.assertEqual(captured['headers'], {'Content-Type': 'image/png', 'Content-Length': str(self.file.stat().st_size)})
        self.assertNotIn('private', str(output.call_args))
        self.assertTrue(json.loads(output.call_args.args[0])['verificationRequired'])
        connection.close.assert_called_once()

    def test_validates_all_file_sizes_before_uploading_anything(self):
        self.plan.append({**self.plan[0], 'size': 999})
        with patch.object(module.http.client, 'HTTPSConnection') as connection:
            with self.assertRaises(ValueError):
                module.upload(self.plan)
            connection.assert_not_called()

    def test_does_not_follow_upload_redirects(self):
        connection = Mock()
        connection.getresponse.return_value.status = 302
        with patch.object(module.http.client, 'HTTPSConnection', return_value=connection):
            with self.assertRaises(RuntimeError):
                module.upload(self.plan)
        connection.request.assert_called_once()
        connection.close.assert_called_once()

    def test_rejects_plaintext_upload_url(self):
        self.plan[0]['uploadUrl'] = 'http://storage.example/object'
        with self.assertRaises(ValueError):
            module.upload(self.plan)


if __name__ == '__main__':
    unittest.main()
