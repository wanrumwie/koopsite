from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from folders.functions import get_full_named_path
from folders.templatetags.folder_template_filters import fileext, filename, iconpath, full_named_path, file_media_type
from folders.tests.test_base import DummyFolder
from koopsite.functions import get_iconPathForFolder, get_iconPathByFileExt


class TemplateFiltersTest(TestCase):

    def setUp(self):
        self.root = DummyFolder().create_dummy_root_folder()
        self.file = SimpleUploadedFile("file.txt", b"file_content")
        self.report = DummyFolder().create_dummy_report(self.root, file=self.file)

    def tearDown(self):
        self.report.file.delete()

    def test_filename(self):
        self.assertEqual(filename(self.report), 'file.txt')
        self.assertEqual(filename(''), '')

    def test_fileext(self):
        self.assertEqual(fileext(self.report), '.txt')
        self.assertEqual(fileext(''), '')

    def test_file_media_type(self):
        self.assertEqual(file_media_type(self.report), 'text/plain')
        self.assertEqual(file_media_type(''), '')

    def test_iconpath(self):
        r0 = DummyFolder().create_dummy_report(self.root)
        self.assertEqual(iconpath(self.root), get_iconPathForFolder())
        self.assertEqual(iconpath(self.report), get_iconPathByFileExt('.txt'))
        self.assertEqual(iconpath(r0), "")
        self.assertEqual(fileext(''), '')

    def test_full_named_path(self):
        r0 = DummyFolder().create_dummy_report(self.root)
        self.assertEqual(full_named_path(self.root), get_full_named_path(self.root))
        self.assertEqual(full_named_path(r0), get_full_named_path(r0))

