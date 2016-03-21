from datetime import timedelta
import os
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils.timezone import now
from folders.models import Folder, Report, get_report_path
from folders.tests.test_base import DummyFolder


class DifferentFunctionsTest(TestCase):

    def test_get_report_path(self):
        # patt = 'uploads\\folders\\%s\\%s.data'
        patt = os.path.join('uploads',
                            'folders',
                            '%s',
                            '%s.data')

        self.assertEqual(get_report_path(1), patt % (0, 1))
        self.assertEqual(get_report_path(511), patt % (0, 511))
        self.assertEqual(get_report_path(512), patt % (1, 512))
        self.assertEqual(get_report_path(1024), patt % (2, 1024))


class FolderModelTest(TestCase):

    def test_get_absolute_url(self):
        folder = Folder.objects.create()
        expected = reverse('folders:folder-detail', kwargs={'pk': folder.pk})
        self.assertEqual(folder.get_absolute_url(), expected)

    def test_Meta(self):
        self.assertEqual(Folder._meta.verbose_name, ('тека'))
        self.assertEqual(Folder._meta.verbose_name_plural, ('теки'))
        self.assertEqual(Folder._meta.unique_together, (("parent", "name"),))
        self.assertEqual(Folder._meta.permissions, (
                        ('view_folder', 'Can view folder'),
                        ('download_folder', 'Can download folder'),
                        ))

    def test_unique_together_gives_error(self):
        root = DummyFolder().create_dummy_root_folder()
        DummyFolder().create_dummy_folder(parent=root, name='f')
        with self.assertRaises(IntegrityError):
            DummyFolder().create_dummy_folder(parent=root, name='f')

    def test_no_name_gives_error(self):
        f = Folder(name=None)
        with self.assertRaises(IntegrityError):
            f.save()

    # Тест save() з name="" не працює, бо Django не перевіряє
    # порожніх текстових полів!
    # full_clean заставить провести валідацію.
    def test_empty_name_gives_error(self):
        f = Folder(name="")
        with self.assertRaises(ValidationError):
            f.full_clean()


class ReportModelTest(TestCase):

    def tearDown(self):
        # Видалення створенго файла, якщо він залишився внаслідок помилки в тесті
        file_path = os.path.join('uploads',
                            'folders',      # підтека з назвою аплікації
                            '0',            # тека для кожних 512 файлів
                            str(1)          # id файла
                            + ".data")      # фіктивне розширення файла
        try:
            os.unlink(file_path)
        except:
            pass

    def test_saving_and_retrieving_files(self):
        root = DummyFolder().create_dummy_root_folder()
        file = SimpleUploadedFile("file.txt", b"file_content")
        expected = file.read()
        DummyFolder().create_dummy_report(root, file=file)
        saved_report = Report.objects.first()
        # Перевіряємо, чи збереглася первинна назва файла
        self.assertEqual(saved_report.filename, "file.txt")
        # Чи правильний фактичний шлях до файла
        basename = os.path.basename(saved_report.file.path)
        self.assertEqual(basename, "1.data")
        # Час створення (до секунди) співпадає з поточним?
        self.assertAlmostEqual(saved_report.uploaded_on, now(), delta=timedelta(minutes=1))
        # Вмісти збереженого файда і первинного співпадають?
        self.assertEqual(saved_report.file.read(), expected)
        # Видляємо з диска (бо файл по-чесному записався в /uploads/folders/0/1.data)
        saved_report.file.delete()
        # self.client.post(reverse('app:some_view'), {'video': video})

    def test_saving_and_retrieving_reports(self):
        folder = Folder()
        folder.save()

        first_report = Report()
        first_report.filename = 'The first (ever) folder report'
        first_report.parent = folder
        first_report.save()

        second_report = Report()
        second_report.filename = 'Report the second'
        second_report.parent = folder
        second_report.save()

        saved_folder = Folder.objects.first()
        self.assertEqual(saved_folder, folder)

        saved_reports = Report.objects.all()
        self.assertEqual(saved_reports.count(), 2)

        first_saved_report = saved_reports[0]
        second_saved_report = saved_reports[1]

        self.assertEqual(first_saved_report.filename, 'The first (ever) folder report')
        self.assertEqual(first_saved_report.parent, folder)
        self.assertEqual(second_saved_report.filename, 'Report the second')
        self.assertEqual(second_saved_report.parent, folder)

    def test_empty_parent_gives_error(self):
        r = Report()
        with self.assertRaises(IntegrityError):
            r.save()

    def test_no_filename_gives_error(self):
        r = Report(filename=None)
        with self.assertRaises(IntegrityError):
            r.save()

    def test_empty_filename_gives_error(self):
        r = Report(filename="")
        with self.assertRaises(ValidationError):
            r.full_clean()

    def test_no_file_gives_error(self):
        root = DummyFolder().create_dummy_root_folder()
        r = Report(parent=root, file=None)
        with self.assertRaises(ValidationError):
            r.full_clean()

    def test_get_absolute_url_viewable(self):
        folder = Folder.objects.create()
        report = Report(parent=folder, filename='example.jpg')
        report.save()
        expected = reverse('folders:report-preview', kwargs={'pk': report.pk})
        self.assertEqual(report.get_absolute_url(), expected)

    def test_get_absolute_url_not_viewable(self):
        folder = Folder.objects.create()
        report = Report(parent=folder)
        report.save()
        expected = reverse('folders:report-detail', kwargs={'pk': report.pk})
        self.assertEqual(report.get_absolute_url(), expected)

    def test_get_absolute_url_not_viewable_2(self):
        folder = Folder.objects.create()
        report = Report(parent=folder, filename="example.mdb")
        report.save()
        expected = reverse('folders:report-detail', kwargs={'pk': report.pk})
        self.assertEqual(report.get_absolute_url(), expected)

    def test_Meta(self):
        self.assertEqual(Report._meta.verbose_name, ('файл'))
        self.assertEqual(Report._meta.verbose_name_plural, ('файли'))
        self.assertEqual(Report._meta.permissions, (
                        ('view_report', 'Can view report'),
                        ('download_report', 'Can download report'),
                        ))



