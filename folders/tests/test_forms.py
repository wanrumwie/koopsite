from unittest.case import skip
from django.test import TestCase
from folders.forms import FolderForm, FolderFormInFolder, ReportUpdateForm, ReportForm, ReportFormInFolder, \
    FolderFormBase, FolderDeleteForm, ReportFormBase
from folders.models import Folder, Report
from folders.tests.test_base import DummyFolder


class FolderFormBaseTest(TestCase):

    def setUp(self):
        self.cls_form = FolderFormBase
        self.parent_folder = DummyFolder().create_dummy_root_folder()
        self.initial_data = {'parent': self.parent_folder}
        self.empty_data = {'parent': "", 'name': "", 'created_on': ""}

    def test_form_attributes(self):
        form = self.cls_form
        self.assertEqual(form.required_css_class, 'required')
        self.assertEqual(form.error_css_class   , 'error')
        self.assertEqual(form.READONLY_FIELDS   , ())
        self.assertEqual(form.Meta.model, Folder)
        self.assertEqual(form.Meta.fields, ('parent', 'name', 'created_on'))

    def test_init(self):
        form = self.cls_form()
        for field in form.READONLY_FIELDS:
            self.assertTrue(form.fields[field].widget.attrs['readonly'])
            self.assertTrue(form.fields[field].widget.attrs['disabled'])

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertIn('Материнська тека:', form.as_p())
        self.assertIn('Тека:', form.as_p())
        self.assertIn('Дата створення:', form.as_p())
        self.assertIn('option value="" selected="selected"', form.as_p())

    def test_form_renders_values(self):
        form = self.cls_form(data=self.initial_data)
        self.assertIn('option value="1" selected="selected">dummy_root_folder', form.as_p())

    def test_form_validation_for_blank_fields(self):
        form = self.cls_form(data=self.empty_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], ["Це поле обов'язкове."])

    def test_form_validation_for_duplicate_fields(self):
        DummyFolder().create_dummy_folder(parent=self.parent_folder,
                                          name='dummy-1')
        # Передаємо у форму такі ж значення parent і name:
        data = {'parent': str(self.parent_folder.id), 'name': "dummy-1"}
        form = self.cls_form(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], ['Тека з таким Материнська тека та Тека вже існує.'])

    # TODO-2015 12 22 умова unique_together = (("parent", "name"),) не перевіряється при parent==None
    @skip
    def test_form_validation_for_duplicate_fields_with_empty_parent(self):
        f1 = DummyFolder().create_dummy_folder(name='dummy-1')
        # Передаємо у форму такі ж значення parent і name:
        data = {'name': "dummy-1"}
        form = self.cls_form(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], ['Тека з таким Материнська тека та Тека вже існує.'])

    def test_form_save(self):
        # Передаємо у форму значення parent і name:
        data = {'parent': str(self.parent_folder.id), 'name': "dummy"}
        form = self.cls_form(data=data)
        new_folder = form.save()
        self.assertEqual(new_folder, Folder.objects.all()[1])


class FolderFormTest(TestCase):

    def setUp(self):
        self.cls_form = FolderForm

    def test_form_attributes(self):
        form = self.cls_form
        self.assertEqual(form.Meta.model, Folder)
        self.assertEqual(form.Meta.fields, ('parent', 'name', 'created_on'))


class FolderFormInFolderTest(TestCase):
    def setUp(self):
        self.cls_form = FolderFormInFolder

    def test_form_attributes(self):
        form = self.cls_form
        self.assertEqual(form.READONLY_FIELDS   , ('parent',))
        self.assertEqual(form.Meta.model, Folder)
        self.assertEqual(form.Meta.fields, ('parent', 'name',))


class FolderDeleteFormTest(TestCase):
    def setUp(self):
        self.cls_form = FolderDeleteForm

    def test_form_attributes(self):
        form = self.cls_form
        self.assertEqual(form.READONLY_FIELDS, ('parent', 'name', 'created_on'))


class ReportFormBaseTest(TestCase):
    # save не перевіряю, бо це зроблено у test_model

    def setUp(self):
        self.cls_form = ReportFormBase
        self.parent_folder = DummyFolder().create_dummy_root_folder()
        self.initial_data = {'parent': self.parent_folder}
        self.empty_data = {'parent': "", 'filename': "", 'file': ""}

    def test_form_attributes(self):
        form = self.cls_form
        self.assertEqual(form.required_css_class, 'required')
        self.assertEqual(form.error_css_class   , 'error')
        self.assertEqual(form.READONLY_FIELDS   , [])
        self.assertEqual(form.Meta.model, Report)
        self.assertEqual(form.Meta.fields, ('parent', 'filename', 'file'))

    def test_init(self):
        form = self.cls_form()
        for field in form.READONLY_FIELDS:
            self.assertTrue(form.fields[field].widget.attrs['readonly'])
            self.assertTrue(form.fields[field].widget.attrs['disabled'])

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertIn('Тека:', form.as_p())
        self.assertIn('Назва файлу:', form.as_p())
        self.assertIn('Файл:', form.as_p())
        self.assertIn('option value="" selected="selected"', form.as_p())

    def test_form_renders_values(self):
        form = self.cls_form(data=self.initial_data)
        self.assertIn('option value="1" selected="selected">dummy_root_folder', form.as_p())

    def test_form_validation_for_blank_fields(self):
        form = self.cls_form(data=self.empty_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['parent'], ["Це поле обов'язкове."])


class ReportUpdateFormTest(TestCase):

    def setUp(self):
        self.cls_form = ReportUpdateForm

    def test_form_attributes(self):
        form = self.cls_form
        self.assertEqual(form.READONLY_FIELDS, ())
        self.assertEqual(form.Meta.model, Report)
        self.assertEqual(form.Meta.fields, ('parent', 'filename', 'file'))

class ReportFormTest(TestCase):

    def setUp(self):
        self.cls_form = ReportForm

    def test_form_attributes(self):
        form = self.cls_form
        self.assertEqual(form.READONLY_FIELDS, ())
        self.assertEqual(form.Meta.model, Report)
        self.assertEqual(form.Meta.fields, ('parent', 'file'))


class ReportFormInFolderTest(TestCase):

    def setUp(self):
        self.cls_form = ReportFormInFolder

    def test_form_attributes(self):
        form = self.cls_form
        self.assertEqual(form.READONLY_FIELDS, ('parent',))
        self.assertEqual(form.Meta.model, Report)
        self.assertEqual(form.Meta.fields, ('parent', 'file',))

