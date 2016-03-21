from asyncio.tasks import sleep
from datetime import timedelta
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.timezone import now
from folders.forms import FolderForm, FolderFormInFolder, \
                        ReportForm, ReportUpdateForm, \
                        ReportFormInFolder, FolderDeleteForm
from folders.models import Folder, Report
from folders.tests.test_base import DummyFolder
from folders.views import FolderCreate, FolderList, FolderDetail, \
                        ReportList, ReportDetail, ReportPreview, \
                        FolderCreateInFolder, FolderDelete, \
                        ReportDelete, FolderUpdate, ReportUpdate, \
                        ReportUpload, ReportUploadInFolder, \
                        reportDownload, folderDownload, \
                        FolderParentList, FolderReportList
from koopsite.fileExtIconPath import get_viewable_extension_list
from koopsite.settings import LOGIN_URL
from koopsite.tests.test_base import DummyUser
from koopsite.tests.test_views import setup_view


class FolderListTest(TestCase):

    def setUp(self):
        self.cls_view = FolderList
        self.path = '/folders/list/'
        self.template = 'folders/folder_list.html'

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Folder)
        self.assertIsNone(view.paginate_by)
        self.assertEqual(view.ordering, 'name')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_view_renders_proper_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_200(self):
        request = RequestFactory().get(self.path)
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)


class FolderDetailTest(TestCase):

    def setUp(self):
        self.cls_view = FolderDetail
        self.path = '/folders/1/'
        self.template = 'folders/folder_detail.html'

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Folder)
        self.assertEqual(view.paginate_by, 12)
        self.assertEqual(view.context_self_object_name, 'folder')
        self.assertEqual(view.context_object_name, 'obj_details')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_view_renders_no_template_AnonymousUser(self):
        DummyFolder().create_dummy_root_folder()
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_proper_template(self):
        DummyFolder().create_dummy_root_folder()
        DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))
        # Перевіряємо response.url.startswith(), бо перевірка:
        # self.assertRedirects(response, LOGIN_URL)
        # дає помилку:
        # AttributeError: 'HttpResponseRedirect' object has no attribute 'client'

    def test_view_gives_response_status_code_200(self):
        DummyFolder().create_dummy_root_folder()
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)


class ReportListTest(TestCase):

    def setUp(self):
        self.cls_view = ReportList
        self.path = '/folders/report/list/'
        self.template = 'folders/report_list.html'

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Report)
        self.assertEqual(view.ordering, 'filename')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_proper_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_200(self):
        request = RequestFactory().get(self.path)
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)


class ReportDetailTest(TestCase):

    def setUp(self):
        self.cls_view = ReportDetail
        self.path = '/folders/report/1/'
        self.template = 'folders/report_detail.html'

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Report)
        self.assertEqual(view.paginate_by, 12)
        self.assertEqual(view.context_self_object_name, 'report')
        self.assertEqual(view.context_object_name, 'obj_details')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_no_template_AnonymousUser(self):
        root = DummyFolder().create_dummy_root_folder()
        DummyFolder().create_dummy_report(root)
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_proper_template(self):
        root = DummyFolder().create_dummy_root_folder()
        DummyFolder().create_dummy_report(root)
        DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200(self):
        root = DummyFolder().create_dummy_root_folder()
        DummyFolder().create_dummy_report(root)
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)


class ReportPreviewTest(TestCase):

    def setUp(self):
        self.cls_view = ReportPreview
        self.path = '/folders/report/1/preview/'
        self.template = 'folders/report_preview.html'

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Report)

    def test_get_context_data(self):
        root = DummyFolder().create_dummy_root_folder()
        report = DummyFolder().create_dummy_report(root, id=1)
        request = RequestFactory().get('/folders/report/1/preview/')
        kwargs = {'pk': 1}
        view = self.cls_view()
        view = setup_view(view, request, **kwargs)
        view.model = Report
        view.object = report
        expected = get_viewable_extension_list()
        context = view.get_context_data()
        self.assertEqual(context['viewable_extension_list'], expected)

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_no_template_AnonymousUser(self):
        root = DummyFolder().create_dummy_root_folder()
        DummyFolder().create_dummy_report(root)
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_proper_template(self):
        root = DummyFolder().create_dummy_root_folder()
        DummyFolder().create_dummy_report(root)
        dummy_user = DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'view_report')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_302_Authorized_w_o_permission(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200(self):
        root = DummyFolder().create_dummy_root_folder()
        DummyFolder().create_dummy_report(root)
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'view_report')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)


class FolderCreateTest(TestCase):

    def setUp(self):
        self.cls_view = FolderCreate
        self.path = '/folders/create/'
        self.template = 'folders/folder_create.html'

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Folder)
        self.assertEqual(view.form_class, FolderForm)

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_no_template_AnonymousUser(self):
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_no_template_simple_user(self):
        DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_proper_template(self):
        dummy_user = DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'add_folder')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_302_user_w_o_permission(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'add_folder')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)


class FolderCreateInFolderTest(TestCase):

    def setUp(self):
        self.cls_view = FolderCreateInFolder
        self.path = '/folders/1/create/'
        self.template = 'folders/folder_create.html'
        self.parent_folder = DummyFolder().create_dummy_root_folder()

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Folder)
        self.assertEqual(view.form_class, FolderFormInFolder)
        self.assertEqual(view.kwargs, {})

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_no_template_AnonymousUser(self):
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_no_template_simple_user(self):
        DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_proper_template(self):
        dummy_user = DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'add_folder')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_302_user_w_o_permission(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'add_folder')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'add_folder')
        data = {
            'name' : 'dummy_folder_post'
        }
        request = RequestFactory().post(self.path, data)
        request.user = dummy_user
        kwargs = {'parent': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(response.url, "/folders/1/contents/")
        # Витягаємо з бази щойно створений запис:
        f = self.cls_view.model.objects.last()
        # Перевіряємо поля:
        self.assertEqual(f.name, data['name'])
        self.assertEqual(f.parent, self.parent_folder)
        # Час створення (до секунди) співпадає з поточним?
        self.assertAlmostEqual(f.created_on, now(), delta=timedelta(minutes=1))
        expected_url = f.get_absolute_url()
        self.assertEqual(response.url, expected_url)

    def test_post_name_parent_not_unique(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'add_folder')
        DummyFolder().create_dummy_folder(parent=self.parent_folder, name='double')
        expected = len(self.cls_view.model.objects.all())

        data = {
            'name' : 'double'
        }
        request = RequestFactory().post(self.path, data)
        request.user = dummy_user
        kwargs = {'parent': 1}
        response = self.cls_view.as_view()(request, **kwargs)

        # Новий запис не має бути створено:
        self.assertEqual(len(self.cls_view.model.objects.all()), expected)

        # Через помилку залишаємося на тій же сторінці
        self.assertEqual(response.status_code, 200)
        # expected_url = self.path
        # self.assertEqual(response.url, expected_url)


class FolderDeleteTest(TestCase):

    def setUp(self):
        self.cls_view = FolderDelete
        self.path = '/folders/1/delete/'
        self.template = 'folders/folder_delete.html'
        self.root = DummyFolder().create_dummy_root_folder()

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Folder)
        self.assertEqual(view.form_class, FolderDeleteForm)

    def test_view_success_url(self):
        view = self.cls_view()
        self.assertEqual(view.get_success_url(), reverse('folders:folder-list-all'))

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_no_template_AnonymousUser(self):
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_no_template_simple_user(self):
        DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_proper_template(self):
        dummy_user = DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'delete_folder')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        kwargs = {'pk': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_302_user_w_o_permission(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        kwargs = {'pk': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'delete_folder')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        kwargs = {'pk': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'delete_folder')
        request = RequestFactory().post(self.path)
        request.user = dummy_user
        kwargs = {'pk': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        expected_url = self.cls_view(pk=1).get_success_url()
        self.assertEqual(response.url, expected_url)
        # Перевіряємо чи видалено з бази запис
        ff = self.cls_view.model.objects.all()
        # Перевіряємо поля:
        self.assertEqual(len(ff), 0)

    def test_post_redirect_if_folder_not_empty(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'delete_folder')
        # Створюємо теку в тій, яку хочемо видалити
        DummyFolder().create_dummy_folder(parent=self.root)
        request = RequestFactory().post(self.path)
        request.user = dummy_user
        kwargs = {'pk': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        expected_url = reverse('folders:folder-not-empty')
        self.assertEqual(response.url, expected_url)
        # Перевіряємо чи не видалено з бази запис
        ff = self.cls_view.model.objects.all()
        # Перевіряємо поля:
        self.assertEqual(len(ff), 1+1)

    def test_post_redirect_if_folder_not_empty_2(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'delete_folder')
        # Створюємо файл в теці, яку хочемо видалити
        DummyFolder().create_dummy_report(parent=self.root)
        request = RequestFactory().post(self.path)
        request.user = dummy_user
        kwargs = {'pk': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        expected_url = reverse('folders:folder-not-empty')
        self.assertEqual(response.url, expected_url)
        # Перевіряємо чи не видалено з бази запис
        ff = self.cls_view.model.objects.all()
        # Перевіряємо поля:
        self.assertEqual(len(ff), 1+0)


class ReportDeleteTest(TestCase):

    def setUp(self):
        self.cls_view = ReportDelete
        self.path = '/folders/report/1/delete/'
        self.author = DummyUser().create_dummy_user(username='author', password='secret')
        self.template = 'folders/report_delete.html'
        self.root = DummyFolder().create_dummy_root_folder()
        self.report = DummyFolder().create_dummy_report(parent=self.root, user=self.author)

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model,   Report)
        self.assertEqual(view.form_class, ReportForm)

    def test_view_success_url(self):
        view = self.cls_view()
        self.assertEqual(view.get_success_url(), reverse('folders:folder-list-all'))

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_no_template_AnonymousUser(self):
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_no_template_simple_user(self):
        DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_proper_template(self):
        dummy_user = DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'delete_report')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        kwargs = {'pk': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_302_user_w_o_permission(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        kwargs = {'pk': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200_user_with_permission(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'delete_report')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        kwargs = {'pk': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_view_gives_response_status_code_200_user_is_author(self):
        self.client.login(username='author', password='secret')
        request = RequestFactory().get(self.path)
        request.user = self.author
        kwargs = {'pk': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'delete_report')
        request = RequestFactory().post(self.path)
        request.user = dummy_user
        kwargs = {'pk': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        expected_url = self.cls_view(pk=1).get_success_url()
        self.assertEqual(response.url, expected_url)
        # Перевіряємо чи видалено з бази запис
        ff = self.cls_view.model.objects.all()
        # Перевіряємо поля:
        self.assertEqual(len(ff), 0)

    def test_post_if_report_has_file(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'delete_report')
        file = SimpleUploadedFile("file.txt", b"file_content")
        report = DummyFolder().create_dummy_report(self.root, file=file)

        request = RequestFactory().post(self.path)
        request.user = dummy_user
        kwargs = {'pk': report.pk}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        expected_url = self.cls_view(pk=report.pk).get_success_url()
        self.assertEqual(response.url, expected_url)
        # Перевіряємо чи видалено з бази запис
        ff = self.cls_view.model.objects.all()
        # Перевіряємо поля:
        self.assertEqual(len(ff), 1) # залишився один файл
        report.file.delete()


class FolderUpdateTest(TestCase):

    def setUp(self):
        self.cls_view = FolderUpdate
        self.path = '/folders/1/update/'
        self.template = 'folders/folder_update.html'
        self.root = DummyFolder().create_dummy_root_folder()

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Folder)
        self.assertEqual(view.form_class, FolderForm)

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_no_template_AnonymousUser(self):
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_no_template_simple_user(self):
        DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_proper_template(self):
        dummy_user = DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'change_folder')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        kwargs = {'pk': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_302_user_w_o_permission(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        kwargs = {'pk': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'change_folder')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        kwargs = {'pk': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)


class ReportUpdateTest(TestCase):

    def setUp(self):
        self.cls_view = ReportUpdate
        self.path = '/folders/report/1/update/'
        self.template = 'folders/report_update.html'
        self.author = DummyUser().create_dummy_user(username='author', password='secret')
        self.root = DummyFolder().create_dummy_root_folder()
        file = SimpleUploadedFile("file.txt", b"file_content")
        self.report = DummyFolder().create_dummy_report(self.root, file=file, user=self.author)

    def tearDown(self):
        self.report.file.delete()

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Report)
        self.assertEqual(view.form_class, ReportUpdateForm)

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_no_template_AnonymousUser(self):
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_no_template_simple_user(self):
        DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_proper_template(self):
        dummy_user = DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'change_report')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        kwargs = {'pk': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_302_user_w_o_permission(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        kwargs = {'pk': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200_with_permission(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'change_report')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        kwargs = {'pk': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_view_gives_response_status_code_200_user_is_author(self):
        self.client.login(username='author', password='secret')
        request = RequestFactory().get(self.path)
        request.user = self.author
        kwargs = {'pk': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)


class ReportUploadTest(TestCase):

    def setUp(self):
        self.cls_view = ReportUpload
        self.path = '/folders/report/upload/'
        self.template = 'folders/report_upload.html'

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Report)
        self.assertEqual(view.form_class, ReportForm)

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_no_template_AnonymousUser(self):
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_no_template_simple_user(self):
        DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_proper_template(self):
        dummy_user = DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'add_report')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_302_user_w_o_permission(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'add_report')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'add_report')
        root = DummyFolder().create_dummy_root_folder()

        # Передаємо у форму значення:
        file = SimpleUploadedFile("file.txt", b"file_content")
        data = {
            'parent' : '1',
            'file': file,
        }
        request = RequestFactory().post(self.path, data)
        request.user = dummy_user
        kwargs = {}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)

        # Витягаємо з бази щойно створений запис:
        f = self.cls_view.model.objects.last()
        fcont = f.file.read()
        self.assertEqual(f.parent, root)
        self.assertEqual(f.filename, "file.txt")
        self.assertEqual(fcont, b"file_content")
        self.assertEqual(f.user, dummy_user)
        expected_url = f.get_absolute_url()
        self.assertEqual(response.url, expected_url)
        f.file.delete()


class ReportUploadInFolderTest(TestCase):

    def setUp(self):
        self.cls_view = ReportUploadInFolder
        self.path = '/folders/1/report/upload/'
        self.template = 'folders/report_upload.html'
        self.parent_folder = DummyFolder().create_dummy_root_folder()

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Report)
        self.assertEqual(view.form_class, ReportFormInFolder)
        self.assertEqual(view.kwargs, {})

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_no_template_AnonymousUser(self):
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_no_template_simple_user(self):
        DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_proper_template(self):
        dummy_user = DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'add_report')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_302_user_w_o_permission(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'add_report')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'add_report')
        root = DummyFolder().create_dummy_root_folder()

        # Передаємо у форму значення:
        file = SimpleUploadedFile("file.txt", b"file_content")
        data = {'file': file}
        request = RequestFactory().post(self.path, data)
        request.user = dummy_user
        kwargs = {'parent': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)

        # Витягаємо з бази щойно створений запис:
        f = self.cls_view.model.objects.last()
        fcont = f.file.read()
        self.assertEqual(f.parent, root)
        self.assertEqual(f.filename, "file.txt")
        self.assertEqual(fcont, b"file_content")
        self.assertEqual(f.user, dummy_user)
        expected_url = f.get_absolute_url()
        self.assertEqual(response.url, expected_url)
        f.file.delete()

class FolderDownloadTest(TestCase):

    def setUp(self):
        self.view = folderDownload
        self.path = '/folders/1/download/'
        self.root = DummyFolder().create_dummy_root_folder()
        file = SimpleUploadedFile("file.txt", b"file_content")
        self.report = DummyFolder().create_dummy_report(self.root, file=file)

    def tearDown(self):
        # Видалення dummy-файла із затримкою на час його завантаження
        deleted = False
        i = 0
        while not deleted and i<30:
            try:
                self.report.file.delete()
                deleted = True
            except:
                sleep(1)
                i += 1
        if not deleted: print('file not deleted in FolderDownloadTest')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_302_user_w_o_permission(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'download_folder')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, 200)


class ReportDownloadTest(TestCase):

    def setUp(self):
        self.view = reportDownload
        self.path = '/folders/report/1/download/'
        self.root = DummyFolder().create_dummy_root_folder()
        file = SimpleUploadedFile("file.txt", b"file_content")
        self.report = DummyFolder().create_dummy_report(self.root, file=file)

    def tearDown(self):
        # Видалення dummy-файла із затримкою на час його завантаження
        deleted = False
        i = 0
        while not deleted and i<30:
            try:
                self.report.file.delete()
                deleted = True
            except:
                sleep(10)
                i += 1
        if not deleted: print('file not deleted in ReportDownloadTest')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_302_user_w_o_permission(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'download_report')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, 200)


class FolderParentListTest(TestCase):

    def setUp(self):
        self.cls_view = FolderParentList
        self.path = '/folders/parents/'
        self.template = 'folders/folder_parents.html'

    def test_view_model_and_attributes(self):
        DummyFolder().create_dummy_root_folder()
        view = self.cls_view()
        self.assertEqual(list(view.queryset), list(Folder.objects.filter(parent=None)))

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_view_renders_proper_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_200(self):
        request = RequestFactory().get(self.path)
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)



class FolderReportListTest(TestCase):

    def setUp(self):
        self.cls_view = FolderReportList
        self.path = '/folders/list-all/'
        self.template = 'folders/folder_list_all.html'

    # def test_view_model_and_attributes(self):
    #     view = self.cls_view()
    #     self.assertEqual(view.paginate_by, 15)

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_view_renders_proper_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_200(self):
        request = RequestFactory().get(self.path)
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_queryset(self):
        f1 = DummyFolder().create_dummy_root_folder(name='f1')
        self.assertEqual(self.cls_view().get_queryset(), [f1])
        f2 = DummyFolder().create_dummy_folder(parent=f1, name="f2")
        self.assertEqual(self.cls_view().get_queryset()[1], f2)
        f3 = DummyFolder().create_dummy_folder(parent=f2, name="f3")
        self.assertEqual(self.cls_view().get_queryset()[2], f3)
        r1 = DummyFolder().create_dummy_report(parent=f1, filename="r1")
        self.assertEqual(self.cls_view().get_queryset()[3], r1)
        r2 = DummyFolder().create_dummy_report(parent=f2, filename="r2")
        self.assertEqual(self.cls_view().get_queryset()[3], r2)
        r3 = DummyFolder().create_dummy_report(parent=f3, filename="r3")
        self.assertEqual(self.cls_view().get_queryset()[3], r3)


