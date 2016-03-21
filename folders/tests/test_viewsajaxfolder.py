import json
import types
from unittest.case import skipIf
from datetime import timedelta

from django.contrib.auth.models import User, AnonymousUser
from django.core.exceptions import PermissionDenied
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import resolve
from django.http.response import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.timezone import now

from folders.functions import response_for_download, response_for_download_zip, get_folders_tree_HTML
from folders.models import Folder, Report
from folders.tests.test_base import DummyFolder, create_byte_string
from folders.viewsajaxfolder import FolderContentsArray, FolderContents, \
                                    AjaxTableRowViewBase, AjaxFolderCreate, \
                                    AjaxFolderRename, AjaxReportRename, \
                                    AjaxElementMove, AjaxFolderDelete, \
                                    AjaxReportDelete, XHRTableRowView, \
                                    XHRReportDownload, XHRFolderDownload, \
                                    XHRReportUpload, ajaxFoldersTreeFromBase
from functional_tests.koopsite.ft_base import DummyUser
from koopsite.functions import get_or_none, \
                                dict_from_json_str_or_bytes
from koopsite.settings import SKIP_TEST, MAX_FILE_SIZE
from koopsite.tests.test_views import setup_view
from koopsite.tests.test_viewsajax import DummyAjaxRequest, \
                                        DummyXHRrequest
from koopsite.viewsajax import msgType


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderContentsArrayTest(TestCase):

    def setUp(self):
        self.bta_cls = FolderContentsArray
        DummyFolder().create_dummy_catalogue()
        root = Folder.objects.get(id=1)
        file = SimpleUploadedFile("file.txt", b"file_content")
        self.report = DummyFolder().create_dummy_report(root, id=1, file=file)

    def tearDown(self):
        self.report.file.delete()

    def test_get_table_headers(self):
        expected = {
                    0: "",
                    1: "Тип",
                    2: "Найменування",
                    3: "Дата",
                    4: "Розмір",
                    }
        cap = self.bta_cls().get_table_headers()
        self.assertEqual(cap, expected)

    def test_get_row(self):
        folder = get_or_none(Folder, id=1)
        expected = {
            0: {'model': 'folder', 'name': folder.name, 'id': str(folder.id)},
            1: 'folder',
            2: folder.name,
            3: "",
            4: "",
            }
        row = self.bta_cls().get_row(folder)
        self.assertEqual(row, expected)

    def test_get_row_2(self):
        folder = get_or_none(Folder, id=100)
        expected = None
        row = self.bta_cls().get_row(folder)
        self.assertEqual(row, expected)

    def test_get_row3(self):
        report = get_or_none(Report, id=1)
        expected = {
            0: {'model': 'report', 'name': report.filename, 'id': str(report.id)},
            1: 'report',
            2: report.filename,
            3: report.uploaded_on.isoformat(),
            4: 12,
            }
        row = self.bta_cls().get_row(report)
        self.assertEqual(row, expected)

    def test_get_model_id_name(self):
        folder = get_or_none(Folder, id=1)
        expected = {'model': 'folder', 'name': folder.name, 'id': str(folder.id)}
        m_id_n = self.bta_cls().get_model_id_name(folder)
        self.assertEqual(m_id_n, expected)

    def test_get_model_id_name_2(self):
        folder = get_or_none(Folder, id=100)
        expected = {}
        m_id_n = self.bta_cls().get_model_id_name(folder)
        self.assertEqual(m_id_n, expected)

    def test_get_model_id_name_3(self):
        report = get_or_none(Report, id=1)
        expected = {'model': 'report', 'name': report.filename, 'id': str(report.id)}
        m_id_n = self.bta_cls().get_model_id_name(report)
        self.assertEqual(m_id_n, expected)

    def test_get_supplement_data(self):
        folder = get_or_none(Folder, id=1)
        expected = {
                    'iconPath': "/static/img/folder.png",
                    'fileExt' : "",
                    'fileType': "folder",
                    }
        data = self.bta_cls().get_supplement_data(folder)
        self.assertEqual(data, expected)

    def test_get_supplement_data_2(self):
        user = get_or_none(User, id=3)
        expected = None
        data = self.bta_cls().get_supplement_data(user)
        self.assertEqual(data, expected)

    def test_get_supplement_data_3(self):
        report = get_or_none(Report, id=1)
        expected = {
                    'iconPath': "/static/img/file-icons/32px/txt.png",
                    'fileExt' : ".txt",
                    'fileType': "report",
                    }
        data = self.bta_cls().get_supplement_data(report)
        self.assertEqual(data, expected)


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderContentsTest(TestCase):

    def setUp(self):
        self.cls_view = FolderContents
        self.path = '/folders/1/contents/'
        self.template = 'folders/folder_contents.html'
        DummyFolder().create_dummy_catalogue()
        self.root = Folder.objects.get(id=1)
        self.folder1, self.folder2 = Folder.objects.filter(parent=self.root)
        file = SimpleUploadedFile("file.txt", b"file_content")
        self.report = DummyFolder().create_dummy_report(self.root, id=1, file=file)
        self.dummy_user = DummyUser().create_dummy_user()

    def tearDown(self):
        self.report.file.delete()

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_proper_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_200(self):
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.dummy_user
        request.session = {}
        kwargs = {'pk': 1}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_get_queryset_for_anonymous_user(self):
        view = self.cls_view()
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        kwargs = {'pk': 1}
        view = setup_view(view, request, **kwargs)
        view.object = self.root
        expected = [self.folder1, self.folder2, self.report]
        self.assertEqual(view.get_queryset(), expected)

    def test_get_context_data(self):
        view = self.cls_view()
        request = RequestFactory().get(self.path)
        request.user = self.dummy_user
        request.session = {}
        kwargs = {'pk': 1}
        view = setup_view(view, request, **kwargs)
        response = view.dispatch(view.request, *view.args, **view.kwargs)
        context = view.get_context_data(**kwargs)
        expected_cap = {
                    0: "",
                    1: "Тип",
                    2: "Найменування",
                    3: "Дата",
                    4: "Розмір",
                    }
        self.assertEqual(context['browTabName'    ], "folders_contents")
        self.assertEqual(context['cap'            ], expected_cap)
        self.assertEqual(context['selElementID'   ], None)
        self.assertEqual(context['selElementModel'], None)
        self.assertEqual(context['selRowIndex'    ], 0)
        j_arr = {0: {0: {'name': 'dum_f_0_0_0', 'id': '2', 'model': 'folder'}, 1: 'folder', 2: 'dum_f_0_0_0', 3: self.folder1.created_on, 4: ''}, 1: {0: {'name': 'dum_f_0_0_1', 'id': '5', 'model': 'folder'}, 1: 'folder', 2: 'dum_f_0_0_1', 3: self.folder2.created_on, 4: ''}, 2: {0: {'name': 'file.txt', 'id': '1', 'model': 'report'}, 1: 'report', 2: 'file.txt', 3: self.report.uploaded_on, 4: 12}}
        for i in j_arr:
            if j_arr[i][3]:
                j_arr[i][3] = j_arr[i][3].isoformat()
            else:
                j_arr[i][3] = ""
        json_arr = json.dumps(j_arr)
        self.maxDiff = None
        self.assertEqual(json.loads(context['json_arr']), json.loads(json_arr))
        self.assertEqual(request.session['Selections'], {'folders_contents': {'1': {'model': None, 'id': None, 'selRowIndex': 0}}})


# @skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxTableRowTestBase(TestCase):

    def setUp(self):
        self.rqst = types.SimpleNamespace(
                                        parent_id   = None,
                                        model       = None,
                                        id          = None,
                                        name        = None,
                                        target_id   = None,
                                        )
        self.msg = types.SimpleNamespace(title   = "",
                                        type    = "",
                                        message = "",
                                        )

        DummyFolder().create_dummy_catalogue()
        self.root = Folder.objects.get(id=1)
        self.folder1, self.folder2 = Folder.objects.filter(parent=self.root)
        file = SimpleUploadedFile("file.txt", b"file_content")
        self.report = DummyFolder().create_dummy_report(self.root, id=1, file=file)
        self.dummy_user = DummyUser().create_dummy_user()
        self.john   = DummyUser().create_dummy_user(username='john', password='secret')
        self.paul   = DummyUser().create_dummy_user(username='paul', password='secret')
        self.george = DummyUser().create_dummy_user(username='george', password='secret')
        self.ringo  = DummyUser().create_dummy_user(username='ringo', password='secret')
        # DummyUser().add_dummy_permission(self.john, 'folders.add_folder')
        # DummyUser().add_dummy_permission(self.john, 'folders.add_report')
        # DummyUser().add_dummy_permission(self.john, 'folders.change_folder')
        # DummyUser().add_dummy_permission(self.john, 'folders.change_report')
        # DummyUser().add_dummy_permission(self.john, 'folders.delete_folder')
        # DummyUser().add_dummy_permission(self.john, 'folders.delete_report')
        # DummyUser().add_dummy_permission(self.john, 'folders.download_folder')
        # DummyUser().add_dummy_permission(self.john, 'folders.download_report')

    def tearDown(self):
        self.report.file.delete()

    def get_m_id_n(self, f):
        try:
            m = f._meta.model_name
            if   m == 'folder': n = f.name
            elif m == 'report': n = f.filename
            else:               n = ""
            id = str(f.id)
        except:
            m = None
            id = None
            n = None
        return m, id, n

    def get_kwargs_for_ajax_data_one_record(self, record):
        model, id, name = self.get_m_id_n(record)
        if record and record.parent:
            parent_id = record.parent.id
        else:
            parent_id = ""
        kwargs = {
                    'browTabName' :'folders_contents',
                    'parent_id'   :parent_id,
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :model,
                    'id'          :id,
                    'name'        :name,
                }
        return kwargs

    def check_rqst_equal_to_ajax_kwarqs(self, rqst, kwarqs):
        self.assertEqual(rqst.parent_id, kwarqs.get('parent_id'))
        self.assertEqual(rqst.model    , kwarqs.get('model'))
        self.assertEqual(rqst.id       , kwarqs.get('id'))
        self.assertEqual(rqst.name     , kwarqs.get('name'))
        self.assertEqual(rqst.target_id, kwarqs.get('target_id'))


    def check_view_server_response_data(self,
                                            sr=None,
                                            expected_title=None,
                                            expected_type=None,
                                            expected_message=None,
                                            expected_changes=None,
                                            expected_supplement=None
                                           ):
        d = dict_from_json_str_or_bytes(sr)
        # Чи ф-ція повертає правильний response?
        self.assertEqual(d.get('title'     ), expected_title     )
        self.assertEqual(d.get('type'      ), expected_type      )
        self.assertEqual(d.get('message'   ), expected_message   )
        self.assertEqual(d.get('changes'   ), expected_changes   )
        self.assertEqual(d.get('supplement'), expected_supplement)


@skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxTableRowViewTest(AjaxTableRowTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxTableRowViewBase

    # Метод processing тестується у дочірніх класах

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.msg     , self.msg     )
        self.assertEqual(view.rqst    , self.rqst    )

    def test_get_request_data_folder(self):
        view = self.cls_view
        record = self.folder1
        rqst = self.rqst
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        element, rqst = view().get_request_data(request, rqst)
        # Чи метод повертає правильні записи?
        self.assertEqual(element, record)
        self.check_rqst_equal_to_ajax_kwarqs(rqst, kwargs)

    def test_get_request_data_report(self):
        view = self.cls_view
        record = self.report
        rqst = self.rqst
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        element, rqst = view().get_request_data(request, rqst)
        # Чи метод повертає правильні записи?
        self.assertEqual(element, record)
        self.check_rqst_equal_to_ajax_kwarqs(rqst, kwargs)

    def test_get_request_data_3_no_record(self):
        view = self.cls_view
        record = None
        rqst = self.rqst
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        element, rqst = view().get_request_data(request, rqst)
        # Чи метод повертає правильні записи?
        self.assertEqual(element, None)
        self.assertEqual(rqst, None)

    def test_get_request_data_4_no_model(self):
        view = self.cls_view
        record = self.folder1
        rqst = self.rqst
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        kwargs['model']=''
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        element, rqst = view().get_request_data(request, rqst)
        # Чи метод повертає правильні записи?
        self.assertEqual(element, None)
        self.assertEqual(rqst, None)

    def test_get_request_data_5_model_mismatch_table_name(self):
        view = self.cls_view
        record = self.folder1
        rqst = self.rqst
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        kwargs['browTabName'] = 'users_table'
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        element, rqst = view().get_request_data(request, rqst)
        # Чи метод повертає правильні записи?
        self.assertEqual(element, None)
        self.assertEqual(rqst, None)

    def test_get_request_data_5_no_table_name(self):
        view = self.cls_view
        record = self.folder1
        rqst = self.rqst
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        kwargs['browTabName'] = ''
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        element, rqst = view().get_request_data(request, rqst)
        # Чи метод повертає правильні записи?
        self.assertEqual(element, None)
        self.assertEqual(rqst, None)

    def test_get_request_data_6_unknown_table_name(self):
        view = self.cls_view
        record = self.folder1
        rqst = self.rqst
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        kwargs['browTabName'] = 'FOLDER'
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        element, rqst = view().get_request_data(request, rqst)
        # Чи метод повертає правильні записи?
        self.assertEqual(element, None)
        self.assertEqual(rqst, None)

    def test_handler(self):
        view = self.cls_view()
        record = self.folder1
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        kwargs['name'] = 'Нова тека'
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        response = view.handler(request)
        # Очікувані дані з response
        rec = Folder.objects.last()
        expected_title      = rec.name
        expected_type       = "NewRow"
        expected_message    = "Тека створена!"
        expected_changes   = {'0': {'id': str(rec.id),
                                    'name': rec.name,
                                    'model': rec._meta.model_name,
                                    },
                              '1': rec._meta.model_name,
                              '2': rec.name,
                              '3': rec.created_on.isoformat(),
                              '4': '',
                              }
        expected_supplement = {
                            'fileExt'   : '',
                            'fileType'  : 'folder',
                            'iconPath'  : '/static/img/folder.png',
                            }
        self.check_view_server_response_data(response._container[0],
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)
        expected = {'content-type': ('Content-Type', 'application/json')}
        self.assertEqual(response._headers, expected)

    def test_handler_return_empty_response_if_no_client_request(self):
        view = self.cls_view()
        request = self.client.request()
        request.POST = {}
        response = view.handler(request)
        self.assertTrue(isinstance(response, HttpResponse))
        self.assertEqual(response._container, [b''])
        expected = {'content-type': ('Content-Type', 'text/html; charset=utf-8')}
        self.assertEqual(response._headers, expected)

    def test_handler_return_empty_response_if_no_element(self):
        view = self.cls_view()
        record = None
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        kwargs['name'] = 'Нова тека'
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        response = view.handler(request)
        self.assertTrue(isinstance(response, HttpResponse))
        self.assertEqual(response._container, [b''])
        expected = {'content-type': ('Content-Type', 'text/html; charset=utf-8')}
        self.assertEqual(response._headers, expected)

    def test_dispatch(self):
        view = self.cls_view()
        request = self.client.request()
        request.POST = {}
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)


@skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxFolderCreateTest(AjaxTableRowTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxFolderCreate
        self.path = '/folders/ajax-folder-create'
        DummyUser().add_dummy_permission(self.john, 'add_folder')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_dispatch(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view()
        request = self.client.request()
        request.POST = {}
        request.user = self.john
        request.session = {}
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_view_gives_response_status_code_200(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_view_response_raise_exception_AnonymousUser(self):
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_view_response_raise_exception_user_w_o_permission(self):
        self.client.login(username='ringo', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_processing_no_changes_made_no_name(self):
        view = self.cls_view()
        folder0 = self.folder1
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'folder'
        view.rqst.id          = '2'
        view.rqst.name        = ''
        view.rqst.target_id   = None
        folder, msg = view.processing(folder0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(folder, folder0)
        self.assertEqual(msg.title  , 'Нова тека')
        self.assertEqual(msg.type   , msgType.IncorrectData)
        self.assertEqual(msg.message, "Ви не вказали назву теки!")

    def test_processing_no_changes_made_name_already_exists(self):
        view = self.cls_view()
        folder0 = self.folder1
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'folder'
        view.rqst.id          = '2'
        view.rqst.name        = 'dum_f_0_0_0'
        view.rqst.target_id   = None
        folder, msg = view.processing(folder0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(folder, folder0)
        self.assertEqual(msg.title  , 'Нова тека')
        self.assertEqual(msg.type   , msgType.IncorrectData)
        self.assertEqual(msg.message, "Тека з такою назвою вже існує!")

    def test_processing_changes_made(self):
        view = self.cls_view()
        folder0 = self.folder1
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'folder'
        view.rqst.id          = '2'
        view.rqst.name        = 'New folder'
        view.rqst.target_id   = None
        folder, msg = view.processing(folder0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        folder_db = Folder.objects.last()
        self.assertEqual(folder_db, folder)
        self.assertEqual(folder.name, 'New folder')
        self.assertAlmostEqual(folder.created_on, now(), delta=timedelta(minutes=1))
        self.assertEqual(msg.title  , folder.name)
        self.assertEqual(msg.type   , msgType.NewRow)
        self.assertEqual(msg.message, "Теку створено!")


@skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxFolderRenameTest(AjaxTableRowTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxFolderRename
        self.path = '/folders/ajax-folder-rename'
        DummyUser().add_dummy_permission(self.john, 'change_folder')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_dispatch(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view()
        request = self.client.request()
        request.POST = {}
        request.user = self.john
        request.session = {}
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_view_gives_response_status_code_200(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_view_response_raise_exception_AnonymousUser(self):
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_view_response_raise_exception_user_w_o_permission(self):
        self.client.login(username='ringo', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_processing_no_changes_made_no_name(self):
        view = self.cls_view()
        folder0 = self.folder1
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'folder'
        view.rqst.id          = '2'
        view.rqst.name        = ''
        view.rqst.target_id   = None
        folder, msg = view.processing(folder0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(folder, folder0)
        self.assertEqual(msg.title  , folder0.name)
        self.assertEqual(msg.type   , msgType.IncorrectData)
        self.assertEqual(msg.message, "Ви не вказали назву теки!")

    def test_processing_no_changes_made_name_already_exists(self):
        view = self.cls_view()
        folder0 = self.folder1
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'folder'
        view.rqst.id          = '2'
        view.rqst.name        = 'dum_f_0_0_1'
        view.rqst.target_id   = None
        folder, msg = view.processing(folder0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(folder, folder0)
        self.assertEqual(msg.title  , folder0.name)
        self.assertEqual(msg.type   , msgType.IncorrectData)
        self.assertEqual(msg.message, "Тека з такою назвою вже існує!")

    def test_processing_no_changes_made_the_same_name(self):
        view = self.cls_view()
        folder0 = self.folder1
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'folder'
        view.rqst.id          = '2'
        view.rqst.name        = 'dum_f_0_0_0'
        view.rqst.target_id   = None
        folder, msg = view.processing(folder0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(folder, folder0)
        self.assertEqual(msg.title  , folder0.name)
        self.assertEqual(msg.type   , msgType.NoChange)
        self.assertEqual(msg.message, "Ви не змінили назву теки!")

    def test_processing_changes_made(self):
        view = self.cls_view()
        folder0 = self.folder1
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'folder'
        view.rqst.id          = '2'
        view.rqst.name        = 'New folder name'
        view.rqst.target_id   = None
        folder, msg = view.processing(folder0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        folder_db = get_or_none(Folder, id=folder0.id)
        self.assertEqual(folder_db, folder)
        self.assertEqual(folder.name, 'New folder name')
        self.assertEqual(msg.title  , folder.name)
        self.assertEqual(msg.type   , msgType.Rename)
        self.assertEqual(msg.message, "Теку перейменовано!")


@skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxReportRenameTest(AjaxTableRowTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxReportRename
        self.path = '/folders/ajax-report-rename'
        DummyUser().add_dummy_permission(self.john, 'change_report')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_dispatch(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view()
        request = self.client.request()
        request.POST = {}
        request.user = self.john
        request.session = {}
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_view_gives_response_status_code_200(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_view_response_raise_exception_AnonymousUser(self):
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_view_response_raise_exception_user_w_o_permission(self):
        self.client.login(username='ringo', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_processing_no_changes_made_no_name(self):
        view = self.cls_view()
        report0 = self.report
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'report'
        view.rqst.id          = '1'
        view.rqst.name        = ''
        view.rqst.target_id   = None
        report, msg = view.processing(report0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(report, report0)
        self.assertEqual(msg.title  , report0.filename)
        self.assertEqual(msg.type   , msgType.IncorrectData)
        self.assertEqual(msg.message, "Ви не вказали нову назву файла!")

    def test_processing_no_changes_made_name_already_exists(self):
        view = self.cls_view()
        DummyFolder().create_dummy_report(self.root, filename='text.txt')
        report0 = self.report
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'report'
        view.rqst.id          = '1'
        view.rqst.name        = 'text.txt'
        view.rqst.target_id   = None
        report, msg = view.processing(report0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(report, report0)
        self.assertEqual(msg.title  , report0.filename)
        self.assertEqual(msg.type   , msgType.IncorrectData)
        self.assertEqual(msg.message, "Файл з такою назвою вже існує!")

    def test_processing_no_changes_made_the_same_name(self):
        view = self.cls_view()
        report0 = self.report
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'report'
        view.rqst.id          = '1'
        view.rqst.name        = 'file.txt'
        view.rqst.target_id   = None
        report, msg = view.processing(report0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(report, report0)
        self.assertEqual(msg.title  , report0.filename)
        self.assertEqual(msg.type   , msgType.NoChange)
        self.assertEqual(msg.message, "Ви не змінили назву файла!")

    def test_processing_changes_made(self):
        view = self.cls_view()
        report0 = self.report
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'report'
        view.rqst.id          = '1'
        view.rqst.name        = 'New file name'
        view.rqst.target_id   = None
        report, msg = view.processing(report0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        report_db = get_or_none(Report, id=report0.id)
        self.assertEqual(report_db, report)
        self.assertEqual(report.filename, 'New file name')
        self.assertEqual(msg.title  , report.filename)
        self.assertEqual(msg.type   , msgType.Rename)
        self.assertEqual(msg.message, "Файл перейменовано!")


@skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxElementMoveTest(AjaxTableRowTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxElementMove
        self.path = '/folders/ajax-element-move'
        DummyUser().add_dummy_permission(self.john, 'change_folder')
        DummyUser().add_dummy_permission(self.john, 'change_report')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_dispatch(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view()
        request = self.client.request()
        request.POST = {}
        request.user = self.john
        request.session = {}
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_view_gives_response_status_code_200(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_view_response_raise_exception_AnonymousUser(self):
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_view_response_raise_exception_user_w_o_permission(self):
        self.client.login(username='ringo', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_view_response_raise_exception_user_with_not_enough_permission(self):
        self.client.login(username='ringo', password='secret')
        DummyUser().add_dummy_permission(self.ringo, 'change_folder')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_view_response_raise_exception_user_with_not_enough_permission_2(self):
        self.client.login(username='ringo', password='secret')
        DummyUser().add_dummy_permission(self.ringo, 'change_report')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_processing_no_changes_made_folder_no_target_id(self):
        view = self.cls_view()
        folder0 = self.folder1
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'folder'
        view.rqst.id          = '2'
        view.rqst.name        = 'dum_f_0_0_0'
        view.rqst.target_id   = None
        folder, msg = view.processing(folder0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(folder, folder0)
        self.assertEqual(msg.title  , folder0.name)
        self.assertEqual(msg.type   , msgType.IncorrectData)
        self.assertEqual(msg.message, "Ви не обрали місце призначення!")

    def test_processing_no_changes_made_folder_the_same_target(self):
        view = self.cls_view()
        folder0 = self.folder1
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'folder'
        view.rqst.id          = '2'
        view.rqst.name        = 'dum_f_0_0_0'
        view.rqst.target_id   = '1'
        folder, msg = view.processing(folder0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(folder, folder0)
        self.assertEqual(msg.title  , folder0.name)
        self.assertEqual(msg.type   , msgType.NoChange)
        self.assertEqual(msg.message, "Ви не змінили розташування!")

    def test_processing_no_changes_made_folder_target_equal_to_folder(self):
        view = self.cls_view()
        folder0 = self.folder1
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'folder'
        view.rqst.id          = '2'
        view.rqst.name        = 'dum_f_0_0_0'
        view.rqst.target_id   = '2'
        folder, msg = view.processing(folder0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(folder, folder0)
        self.assertEqual(msg.title  , folder0.name)
        self.assertEqual(msg.type   , msgType.IncorrectData)
        self.assertEqual(msg.message, "Не можна перемістити теку саму в себе :)")

    def test_processing_no_changes_made_folder_name_already_exists(self):
        view = self.cls_view()
        DummyFolder().create_dummy_folder(parent=Folder.objects.get(id='3'), name='dum_f_0_0_1')
        folder0 = self.folder1
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'folder'
        view.rqst.id          = '2'
        view.rqst.name        = 'dum_f_0_0_1'
        view.rqst.target_id   = '3'
        folder, msg = view.processing(folder0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(folder, folder0)
        self.assertEqual(msg.title  , 'dum_f_0_0_1')
        self.assertEqual(msg.type   , msgType.IncorrectData)
        self.assertEqual(msg.message, "В обраному місці призначення є тека з такою назвою!")

    def test_processing_no_changes_folder_made_no_element(self):
        view = self.cls_view()
        folder0 = None
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'folder'
        view.rqst.id          = '2'
        view.rqst.name        = 'dum_f_0_0_0'
        view.rqst.target_id   = '3'
        folder, msg = view.processing(folder0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(folder, folder0)
        self.assertEqual(msg.title  , "dum_f_0_0_0")
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Не вдалося змінити розташування! Можливо обране місце призначення не існує.")

    def test_processing_no_changes_folder_made_no_target(self):
        view = self.cls_view()
        folder0 = self.folder1
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'folder'
        view.rqst.id          = '2'
        view.rqst.name        = 'dum_f_0_0_0'
        view.rqst.target_id   = '100'
        folder, msg = view.processing(folder0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(folder, folder0)
        self.assertEqual(msg.title  , folder0.name)
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Не вдалося змінити розташування! Можливо обране місце призначення не існує.")

    def test_processing_changes_made_folder(self):
        view = self.cls_view()
        folder0 = self.folder1
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'folder'
        view.rqst.id          = '2'
        view.rqst.name        = 'dum_f_0_0_0'
        view.rqst.target_id   = '3'
        folder, msg = view.processing(folder0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        folder_db = get_or_none(Folder, id=folder0.id)
        self.assertEqual(folder_db, folder)
        self.assertEqual(folder.parent.id, 3)
        self.assertEqual(msg.title  , folder.name)
        self.assertEqual(msg.type   , msgType.MoveElement)
        self.assertEqual(msg.message, "Теку переміщено!")

    # Ф-ції для report: -----------------------------------

    def test_processing_no_changes_made_report_no_target_id(self):
        view = self.cls_view()
        report0 = self.report
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'report'
        view.rqst.id          = '1'
        view.rqst.name        = 'file.txt'
        view.rqst.target_id   = None
        report, msg = view.processing(report0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(report, report0)
        self.assertEqual(msg.title  , report0.filename)
        self.assertEqual(msg.type   , msgType.IncorrectData)
        self.assertEqual(msg.message, "Ви не обрали місце призначення!")

    def test_processing_no_changes_made_report_the_same_target(self):
        view = self.cls_view()
        report0 = self.report
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'report'
        view.rqst.id          = '1'
        view.rqst.name        = 'file.txt'
        view.rqst.target_id   = '1'
        report, msg = view.processing(report0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(report, report0)
        self.assertEqual(msg.title  , report0.filename)
        self.assertEqual(msg.type   , msgType.NoChange)
        self.assertEqual(msg.message, "Ви не змінили розташування!")

    def test_processing_no_changes_made_report_name_already_exists(self):
        view = self.cls_view()
        DummyFolder().create_dummy_report(parent=Folder.objects.get(id='3'), filename='file.txt')
        report0 = self.report
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'report'
        view.rqst.id          = '1'
        view.rqst.name        = 'file.txt'
        view.rqst.target_id   = '3'
        report, msg = view.processing(report0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(report, report0)
        self.assertEqual(msg.title  , 'file.txt')
        self.assertEqual(msg.type   , msgType.IncorrectData)
        self.assertEqual(msg.message, "В обраному місці призначення є файл з такою назвою!")

    def test_processing_no_changes_report_made_no_element(self):
        view = self.cls_view()
        report0 = None
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'report'
        view.rqst.id          = '1'
        view.rqst.name        = 'file.txt'
        view.rqst.target_id   = '3'
        report, msg = view.processing(report0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(report, report0)
        self.assertEqual(msg.title  , "file.txt")
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Не вдалося змінити розташування! Можливо обране місце призначення не існує.")

    def test_processing_no_changes_report_made_no_target(self):
        view = self.cls_view()
        report0 = self.report
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'report'
        view.rqst.id          = '1'
        view.rqst.name        = 'file.txt'
        view.rqst.target_id   = '100'
        report, msg = view.processing(report0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(report, report0)
        self.assertEqual(msg.title  , report0.filename)
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Не вдалося змінити розташування! Можливо обране місце призначення не існує.")

    def test_processing_changes_made_report(self):
        view = self.cls_view()
        report0 = self.report
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'report'
        view.rqst.id          = '1'
        view.rqst.name        = 'file.txt'
        view.rqst.target_id   = '3'
        report, msg = view.processing(report0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        report_db = get_or_none(Report, id=report0.id)
        self.assertEqual(report_db, report)
        self.assertEqual(report.parent.id, 3)
        self.assertEqual(msg.title  , report.filename)
        self.assertEqual(msg.type   , msgType.MoveElement)
        self.assertEqual(msg.message, "Файл переміщено!")


@skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxFolderDeleteTest(AjaxTableRowTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxFolderDelete
        self.path = '/folders/ajax-folder-delete'
        DummyUser().add_dummy_permission(self.john, 'delete_folder')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_dispatch(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view()
        request = self.client.request()
        request.POST = {}
        request.user = self.john
        request.session = {}
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_view_gives_response_status_code_200(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_view_response_raise_exception_AnonymousUser(self):
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_view_response_raise_exception_user_w_o_permission(self):
        self.client.login(username='ringo', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_processing_no_changes_made_folder_not_empty(self):
        view = self.cls_view()
        folder0 = self.folder1
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'folder'
        view.rqst.id          = '2'
        view.rqst.name        = 'dum_f_0_0_0'
        view.rqst.target_id   = None
        folder, msg = view.processing(folder0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        folder_db = get_or_none(Folder, id=folder0.id)
        self.assertEqual(folder_db, folder0)
        self.assertEqual(msg.title  , folder0.name)
        self.assertEqual(msg.type   , msgType.Forbidden)
        self.assertEqual(msg.message, "Обрана тека не порожня! Спершу слід видалити вміст теки.")

    def test_processing_changes_made(self):
        view = self.cls_view()
        folder0 = Folder.objects.get(id=7)
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'folder'
        view.rqst.id          = '7'
        view.rqst.name        = 'dum_f_0_0_1_1_1'
        view.rqst.target_id   = None
        folder, msg = view.processing(folder0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        folder_db = get_or_none(Folder, id=folder0.id)
        self.assertEqual(folder_db, None)
        self.assertEqual(msg.title  , folder0.name)
        self.assertEqual(msg.type   , msgType.DeleteRow)
        self.assertEqual(msg.message, "Теку видалено!")


@skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxReportDeleteTest(AjaxTableRowTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxReportDelete
        self.path = '/folders/ajax-report-delete/1/'
        DummyUser().add_dummy_permission(self.john, 'delete_report')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_dispatch(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view()
        request = self.client.request()
        request.POST = {}
        request.user = self.john
        request.session = {}
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_view_gives_response_status_code_200_user_with_permission(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {'pk': 1}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_view_gives_response_status_code_200_user_author(self):
        self.client.login(username='ringo', password='secret')
        self.report.user = self.ringo
        self.report.save()
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {'pk': 1}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_view_response_raise_exception_AnonymousUser(self):
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        request.session = {}
        kwargs = {'pk': 1}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_view_response_raise_exception_user_w_o_permission(self):
        self.client.login(username='ringo', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {'pk': 1}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_processing_changes_made(self):
        view = self.cls_view()
        report0 = self.report
        path0 = report0.file.path
        view.rqst.parent_id   = '1'
        view.rqst.model       = 'report'
        view.rqst.id          = '1'
        view.rqst.name        = 'file.txt'
        view.rqst.target_id   = None
        report, msg = view.processing(report0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        report_db = get_or_none(Report, id=report0.id)
        self.assertEqual(report_db, None)
        self.assertEqual(msg.title  , report0.filename)
        self.assertEqual(msg.type   , msgType.DeleteRow)
        self.assertEqual(msg.message, "Файл видалено!")
        with self.assertRaises(FileNotFoundError):
            open(path0)


class XHRTableRowTestBase(AjaxTableRowTestBase):

    def setUp(self):
        super().setUp()
        self.rqst = types.SimpleNamespace(
                            parent_id   = None,
                            model       = None,
                            id          = None,
                            name        = None,
                            target_id   = None,
                            fileName             = None,
                            fileSize             = None,
                            fileType             = None,
                            fileLastModifiedDate = None,
                            )


    def set_view_rqst(self, rqst, kwarqs):
        rqst.parent_id = kwarqs.get('parent_id')
        rqst.model     = kwarqs.get('model')
        rqst.id        = kwarqs.get('id')
        rqst.name      = kwarqs.get('name')
        rqst.target_id = kwarqs.get('target_id')
        rqst.fileName             = kwarqs.get('fileName')
        rqst.fileSize             = kwarqs.get('fileSize')
        rqst.fileType             = kwarqs.get('fileType')
        rqst.fileLastModifiedDate = kwarqs.get('fileLastModifiedDate')



    def get_elemSet(self, userSet):
        elemSet = []
        for user in userSet:
            elem = {
                    'model': 'user',
                    'id'   : user.id,
                    'name' : user.username,
                    }
            elemSet.append(elem)
        return elemSet

    def get_expected(self, record, changes_678, suppl_678):
        # Очікувані дані з response
        model, id, name = self.get_m_id_n(record)
        expected_model      = model
        expected_id         = id
        expected_changes    = {0: {'id': id,
                                   'name': name,
                                   'model': model},
                               }
        expected_changes.update(changes_678)
        d = {}
        for k in suppl_678:
            d[k] = '/static/admin/img/icon-%s.gif' % suppl_678[k]
        expected_supplement = {'iconPath': d}
        return expected_model, expected_id, expected_changes, expected_supplement


    def check_view_response_cont(self, d, stringify,
                                        expected_model,
                                        expected_id,
                                        expected_changes,
                                        expected_supplement
                                       ):
        # Чи ф-ція повертає правильний словник?
        if stringify: # словники мають "пройти" крізь дворазове перетворення json
            self.assertEqual(d['model'     ], json.loads(json.dumps(expected_model     )))
            self.assertEqual(d['id'        ], json.loads(json.dumps(expected_id        )))
            self.assertEqual(d['changes'   ], json.loads(json.dumps(expected_changes   )))
            self.assertEqual(d['supplement'], json.loads(json.dumps(expected_supplement)))
        else:
            self.assertEqual(d['model'     ], expected_model     )
            self.assertEqual(d['id'        ], expected_id        )
            self.assertEqual(d['changes'   ], expected_changes   )
            self.assertEqual(d['supplement'], expected_supplement)

    def get_request(self, ajax_data=None):
        request = self.client.request()
        request.method = "POST"
        request.META = ajax_data or {}
        request.session = {}
        return request


@skipIf(SKIP_TEST, "пропущено для економії часу")
class XHRTableRowViewTest(XHRTableRowTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = XHRTableRowView

    # Метод processing тестується у дочірніх класах

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.msg     , self.msg     )
        self.assertEqual(view.rqst    , self.rqst    )

    def test_get_XHR_data_folder(self):
        view = self.cls_view
        record = self.folder1
        rqst = self.rqst
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.get_request(ajax_data)
        element, rqst = view().get_XHR_data(request, rqst)
        # Чи метод повертає правильні записи?
        self.assertEqual(element, record)
        self.check_rqst_equal_to_ajax_kwarqs(rqst, kwargs)

    def test_get_XHR_data_report(self):
        view = self.cls_view
        record = self.report
        rqst = self.rqst
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.get_request(ajax_data)
        element, rqst = view().get_XHR_data(request, rqst)
        # Чи метод повертає правильні записи?
        self.assertEqual(element, record)
        self.check_rqst_equal_to_ajax_kwarqs(rqst, kwargs)

    def test_get_XHR_data_3_no_record(self):
        view = self.cls_view
        record = None
        rqst = self.rqst
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.get_request(ajax_data)
        element, rqst = view().get_XHR_data(request, rqst)
        # Чи метод повертає правильні записи?
        self.assertEqual(element, None)
        self.assertEqual(rqst, None)

    def test_get_XHR_data_4_no_model(self):
        view = self.cls_view
        record = self.folder1
        rqst = self.rqst
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        kwargs['model']=''
        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.get_request(ajax_data)
        element, rqst = view().get_XHR_data(request, rqst)
        # Чи метод повертає правильні записи?
        self.assertEqual(element, None)
        self.assertEqual(rqst, None)

    def test_get_XHR_data_5_model_mismatch_table_name(self):
        view = self.cls_view
        record = self.folder1
        rqst = self.rqst
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        kwargs['browTabName'] = 'users_table'
        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.get_request(ajax_data)
        element, rqst = view().get_XHR_data(request, rqst)
        # Чи метод повертає правильні записи?
        self.assertEqual(element, None)
        self.assertEqual(rqst, None)

    def test_get_XHR_data_5_no_table_name(self):
        view = self.cls_view
        record = self.folder1
        rqst = self.rqst
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        kwargs['browTabName'] = ''
        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.get_request(ajax_data)
        element, rqst = view().get_XHR_data(request, rqst)
        # Чи метод повертає правильні записи?
        self.assertEqual(element, None)
        self.assertEqual(rqst, None)

    def test_get_XHR_data_6_unknown_table_name(self):
        view = self.cls_view
        record = self.folder1
        rqst = self.rqst
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        kwargs['browTabName'] = 'FOLDER'
        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.get_request(ajax_data)
        element, rqst = view().get_XHR_data(request, rqst)
        # Чи метод повертає правильні записи?
        self.assertEqual(element, None)
        self.assertEqual(rqst, None)

    def test_handler(self):
        view = self.cls_view()
        record = self.report
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.get_request(ajax_data)
        response = view.handler(request)
        # Очікувані дані з response
        rec = Report.objects.last()
        expected_title      = rec.filename
        expected_type       = "Normal"
        expected_message    = "Файл успішно завантажено!"
        expected_changes   = {'0': {'id': str(rec.id),
                                    'name': rec.filename,
                                    'model': rec._meta.model_name,
                                    },
                              # '1': rec._meta.model_name,
                              # '2': rec.filename,
                              # '3': rec.uploaded_on.isoformat(),
                              # '4': '',
                              }
        expected_supplement = {
                            'fileExt'   : '.txt',
                            'fileType'  : 'report',
                            'iconPath'  : '/static/img/file-icons/32px/txt.png',
                            }
        expected_response = response_for_download(record)
        server_response = response['server_response']
        del response['server_response']
        self.maxDiff = None
        self.assertEqual(response.__dict__, expected_response.__dict__)
        self.check_view_server_response_data(server_response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)

    def test_handler_return_empty_response_if_no_client_request(self):
        view = self.cls_view()
        request = self.get_request()
        response = view.handler(request)
        self.assertTrue(isinstance(response, HttpResponse))
        expected = [b"There is no 'HTTP_X_CLIENT_REQUEST' in request.META"]
        self.assertEqual(response._container, expected)
        expected = {'content-type': ('Content-Type', 'text/html; charset=utf-8')}
        self.assertEqual(response._headers, expected)

    def test_handler_return_empty_response_if_no_element(self):
        view = self.cls_view()
        record = None
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.get_request(ajax_data)
        response = view.handler(request)
        self.assertTrue(isinstance(response, HttpResponse))
        expected = [b'There is no element in request.META']
        self.assertEqual(response._container, expected)
        expected = {'content-type': ('Content-Type', 'text/html; charset=utf-8')}
        self.assertEqual(response._headers, expected)

    def test_dispatch(self):
        view = self.cls_view()
        request = self.get_request()
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)


@skipIf(SKIP_TEST, "пропущено для економії часу")
class XHRReportDownloadTest(XHRTableRowTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = XHRReportDownload
        self.path = '/folders/ajax-report-download'
        DummyUser().add_dummy_permission(self.john, 'download_report')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_dispatch(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view()
        request = self.get_request()
        request.user = self.john
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_view_gives_response_status_code_400_user_with_permission_empty_request(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 400)

    def test_view_response_raise_exception_AnonymousUser(self):
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_view_response_raise_exception_user_w_o_permission(self):
        self.client.login(username='ringo', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_processing_changes_made(self):
        view = self.cls_view()
        report0 = self.report
        kwargs = self.get_kwargs_for_ajax_data_one_record(report0)
        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.get_request(ajax_data)
        self.set_view_rqst(view.rqst, kwargs)
        report, msg, response = view.processing(request, report0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        report_db = get_or_none(Report, id=report0.id)
        self.assertEqual(report_db, report)
        self.assertEqual(report.parent.id, 1)
        self.assertEqual(msg.title  , report.filename)
        self.assertEqual(msg.type   , msgType.Normal)
        self.assertEqual(msg.message, "Файл успішно завантажено!")
        expected_response = response_for_download(report_db)
        self.assertEqual(response.__dict__, expected_response.__dict__)


@skipIf(SKIP_TEST, "пропущено для економії часу")
class XHRFolderDownloadTest(XHRTableRowTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = XHRFolderDownload
        self.path = '/folders/ajax-folder-download'
        DummyUser().add_dummy_permission(self.john, 'download_folder')
        DummyUser().add_dummy_permission(self.john, 'download_report')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_dispatch(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view()
        request = self.get_request()
        request.user = self.john
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_view_gives_response_status_code_400_user_with_permission_empty_request(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 400)

    def test_view_response_raise_exception_AnonymousUser(self):
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_view_response_raise_exception_user_w_o_permission(self):
        self.client.login(username='ringo', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_view_response_raise_exception_user_with_one_permission(self):
        self.client.login(username='ringo', password='secret')
        DummyUser().add_dummy_permission(self.ringo, 'download_folder')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_view_response_raise_exception_user_with_one_permission_2(self):
        self.client.login(username='ringo', password='secret')
        DummyUser().add_dummy_permission(self.ringo, 'download_report')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_processing_changes_made(self):
        view = self.cls_view()
        folder0 = self.root
        kwargs = self.get_kwargs_for_ajax_data_one_record(folder0)
        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.get_request(ajax_data)
        self.set_view_rqst(view.rqst, kwargs)
        folder, msg, response = view.processing(request, folder0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        folder_db = get_or_none(Folder, id=folder0.id)
        expected_response, expected_zipFilename, expected_msg_message = \
                                    response_for_download_zip(folder_db)
        self.assertEqual(response.__dict__, expected_response.__dict__)
        self.assertEqual(folder_db, folder)
        self.assertEqual(msg.title  , expected_zipFilename)
        self.assertEqual(msg.type   , msgType.Normal)
        self.assertEqual(msg.message, "Вміст теки успішно завантажено!")


@skipIf(SKIP_TEST, "пропущено для економії часу")
class XHRReportUploadTest(XHRTableRowTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = XHRReportUpload
        self.path = '/folders/ajax-report-upload'
        DummyUser().add_dummy_permission(self.john, 'add_report')

    def tearDown(self):
        super().tearDown()
        try:
            report = Report.objects.last()
            report.file.delete()
        except:
            pass

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_dispatch(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view()
        request = self.get_request()
        request.user = self.john
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_view_gives_response_status_code_400_user_with_permission_empty_request(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 400)

    def test_view_response_raise_exception_AnonymousUser(self):
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_view_response_raise_exception_user_w_o_permission(self):
        self.client.login(username='ringo', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_processing_changes_made(self):
        view = self.cls_view()
        report0 = None
        b = create_byte_string(3000)    # створюємо "вміст файла"
        kwargs = self.get_kwargs_for_ajax_data_one_record(report0)
        kwargs['fileName' ] = 'new_file.txt'
        kwargs['fileSize' ] = len(b)
        kwargs['parent_id'] = '1'

        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.get_request(ajax_data)
        # request.body = b'new_file_content'
        request.body = b
        self.set_view_rqst(view.rqst, kwargs)
        report, msg, response = view.processing(request, report0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        report_db = Report.objects.last()
        path = report_db.file.path
        with open(path, 'rb') as f:
            self.assertEqual(f.read(), b)
        self.assertEqual(report_db, report)
        self.assertEqual(report.parent.id, 1)
        self.assertEqual(msg.title  , report.filename)
        self.assertEqual(msg.type   , msgType.NewRow)
        self.assertEqual(msg.message, "Файл успішно заладовано на сервер!")
        expected_response = HttpResponse()
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_processing_changes_made_insert_file_name(self):
        view = self.cls_view()
        report0 = None
        b = create_byte_string(3000)    # створюємо "вміст файла"
        kwargs = self.get_kwargs_for_ajax_data_one_record(report0)
        kwargs['fileName' ] = 'file.txt'
        kwargs['fileSize' ] = len(b)
        kwargs['parent_id'] = '1'

        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.get_request(ajax_data)
        # request.body = b'new_file_content'
        request.body = b
        self.set_view_rqst(view.rqst, kwargs)
        report, msg, response = view.processing(request, report0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        report_db = Report.objects.last()
        path = report_db.file.path
        with open(path, 'rb') as f:
            self.assertEqual(f.read(), b)
        self.assertEqual(report_db, report)
        self.assertEqual(report.parent.id, 1)
        self.assertEqual(msg.title  , report.filename)
        self.assertEqual(msg.type   , msgType.NewRow)
        self.assertEqual(msg.message, "Файл успішно заладовано на сервер!")
        expected_response = HttpResponse()
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_processing_no_changes_no_fileName(self):
        view = self.cls_view()
        report0 = None
        b = create_byte_string(3000)    # створюємо "вміст файла"
        kwargs = self.get_kwargs_for_ajax_data_one_record(report0)
        kwargs['fileName' ] = ''
        kwargs['fileSize' ] = len(b)
        kwargs['parent_id'] = '1'

        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.get_request(ajax_data)
        # request.body = b'new_file_content'
        request.body = b
        self.set_view_rqst(view.rqst, kwargs)
        report, msg, response = view.processing(request, report0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        report_db = Report.objects.last()
        self.assertEqual(report, None)
        self.assertEqual(report_db.id, 1)   # є тільки старий файл
        self.assertEqual(msg.title  , "Заладування файла")
        self.assertEqual(msg.type   , msgType.IncorrectData)
        self.assertEqual(msg.message, "Ви не вказали назву файла!")
        expected_response = HttpResponse()
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_processing_no_changes_too_large_file(self):
        view = self.cls_view()
        report0 = None
        kwargs = self.get_kwargs_for_ajax_data_one_record(report0)
        kwargs['fileName' ] = 'new_file.txt'
        kwargs['fileSize' ] = MAX_FILE_SIZE + 1
        kwargs['parent_id'] = '1'

        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.get_request(ajax_data)
        request.body = b'new_file_content'
        # request.body = b
        self.set_view_rqst(view.rqst, kwargs)
        report, msg, response = view.processing(request, report0, view.rqst, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        report_db = Report.objects.last()
        self.assertEqual(report, None)
        self.assertEqual(report_db.id, 1)   # є тільки старий файл
        self.assertEqual(msg.title  , "Заладування файла")
        self.assertEqual(msg.type   , msgType.Forbidden)
        expected = "Розмір файла %s перевищує дозволене значення %s!" \
                   % (MAX_FILE_SIZE + 1, MAX_FILE_SIZE)
        self.assertEqual(msg.message, expected)
        expected_response = HttpResponse()
        self.assertEqual(response.__dict__, expected_response.__dict__)


# @skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxFoldersTreeFromBaseTest(AjaxTableRowTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = ajaxFoldersTreeFromBase

    def test_view(self):
        view = self.cls_view
        record = None
        kwargs = self.get_kwargs_for_ajax_data_one_record(record)
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        response = view(request)
        # Очікувані дані з response
        expected = {'content-type': ('Content-Type', 'application/json')}
        self.assertEqual(response._headers, expected)
        expected = {'server_response': get_folders_tree_HTML()}
        d = dict_from_json_str_or_bytes(response._container[0])
        # Чи ф-ція повертає правильний response?
        self.assertEqual(d, expected)


    def test_handler_return_empty_response_if_no_client_request(self):
        view = self.cls_view
        request = self.client.request()
        request.POST = {}
        response = view(request)
        self.assertTrue(isinstance(response, HttpResponse))
        self.assertEqual(response._container, [b''])
        expected = {'content-type': ('Content-Type', 'text/html; charset=utf-8')}
        self.assertEqual(response._headers, expected)

