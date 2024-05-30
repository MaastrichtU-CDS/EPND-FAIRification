from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .file_service import determine_encoding

class FileServiceTestCase(TestCase):
    def test_determine_encoding(self):
        upload_file = open('dummydata.csv', 'rb')
        file = SimpleUploadedFile(upload_file.name, upload_file.read())
        encoding = determine_encoding(file.read())
        self.assertEqual(encoding, 'UTF-8-SIG')

