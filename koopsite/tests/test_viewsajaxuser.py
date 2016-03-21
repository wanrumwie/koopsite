import json
import types
from unittest.case import skipIf
from copy import deepcopy

from django.contrib.auth.models import User, AnonymousUser
from django.core import mail
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import resolve
from django.http.response import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory

from flats.tests.test_base import DummyFlat
from functional_tests.koopsite.ft_base import DummyUser
from koopsite.functions import get_or_none, has_group, \
                                dict_from_json_str_or_bytes
from koopsite.models import UserProfile
from koopsite.settings import LOGIN_URL, SKIP_TEST
from koopsite.tests.test_views import setup_view
from koopsite.tests.test_viewsajax import DummyAjaxRequest
from koopsite.viewsajax import msgType
from koopsite.viewsajaxuser import UsersTableArray, UsersTable, \
    AjaxAccountViewBase, AjaxRecognizeAccount, AjaxDenyAccount, \
    AjaxActivateAccount, AjaxDeactivateAccount, AjaxSetMemberAccount, \
    AjaxDenyMemberAccount, AjaxDeleteAccount


@skipIf(SKIP_TEST, "пропущено для економії часу")
class UsersTableArrayTest(TestCase):

    def setUp(self):
        user = DummyUser().create_dummy_user('fred', id=1)
        flat = DummyFlat().create_dummy_flat(id=1, flat_No='55')
        DummyUser().create_dummy_profile(user, flat=flat)
        user.first_name = 'Fred'
        user.last_name  = 'Aster'
        user.email      = 'user@gmail.com'
        user.save()
        DummyUser().create_dummy_user('john', id=2)
        self.bta_cls = UsersTableArray

    def test_get_table_headers(self):
        expected = {0: '', 1: 'Логін', 2: 'Користувач', 3: 'Кв.', 4: 'e-mail', 5: 'Дата ств.', 6: 'Підтв.', 7: 'Актив.', 8: 'Чл.кооп.'}
        cap = self.bta_cls().get_table_headers()
        self.assertEqual(cap, expected)

    def test_get_row(self):
        user = get_or_none(User, id=1)
        expected = {
            0: {'model': 'user', 'name': 'fred', 'id': '1'},
            1: 'fred',
            2: 'Aster Fred',
            3: '55',
            4: 'user@gmail.com',
            5: user.date_joined,
            6: None,
            7: True,
            8: False,
            }
        row = self.bta_cls().get_row(user)
        self.assertEqual(row, expected)

    def test_get_row_2(self):
        user = get_or_none(User, id=3)
        expected = None
        row = self.bta_cls().get_row(user)
        self.assertEqual(row, expected)

    def test_get_model_id_name(self):
        user = get_or_none(User, id=1)
        expected = {'id': '1', 'model': 'user', 'name': 'fred'}
        m_id_n = self.bta_cls().get_model_id_name(user)
        self.assertEqual(m_id_n, expected)

    def test_get_model_id_name_2(self):
        user = get_or_none(User, id=3)
        expected = {}
        m_id_n = self.bta_cls().get_model_id_name(user)
        self.assertEqual(m_id_n, expected)

    def test_get_supplement_data(self):
        user = get_or_none(User, id=1)
        expected = {'iconPath': {
                            8: '/static/admin/img/icon-no.gif',
                            6: '/static/admin/img/icon-unknown.gif',
                            7: '/static/admin/img/icon-yes.gif',
                            }}
        data = self.bta_cls().get_supplement_data(user)
        self.assertEqual(data, expected)

    def test_get_supplement_data_2(self):
        user = get_or_none(User, id=3)
        expected = None
        data = self.bta_cls().get_supplement_data(user)
        self.assertEqual(data, expected)


@skipIf(SKIP_TEST, "пропущено для економії часу")
class UsersTableTest(TestCase):

    def setUp(self):
        self.cls_view = UsersTable
        self.path = '/adm/users/table/'
        self.template = 'koop_adm_users_table.html'
        DummyUser().create_dummy_group(group_name='members')
        DummyUser().create_dummy_group(group_name='staff')
        self.john   = DummyUser().create_dummy_user(username='john', password='secret')
        self.paul   = DummyUser().create_dummy_user(username='paul', password='secret')
        self.george = DummyUser().create_dummy_user(username='george', password='secret')
        self.ringo  = DummyUser().create_dummy_user(username='ringo', password='secret')
        DummyUser().add_dummy_group(self.john  , 'members')
        DummyUser().add_dummy_group(self.john  , 'staff')
        DummyUser().add_dummy_group(self.paul  , 'members')
        DummyUser().add_dummy_group(self.george, 'staff')
        DummyUser().add_dummy_permission(self.john, 'activate_account')
        self.john.is_staff = True
        self.john.save()
        self.dummy_user = AnonymousUser()

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model      , User)

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_proper_template(self):
        self.client.login(username='john', password='secret')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view
        kwargs = {}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_302_user_w_o_permission(self):
        self.client.login(username='ringo', password='secret')
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        view = self.cls_view
        kwargs = {}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_view_gives_response_status_code_200_setup(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view()
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        view = setup_view(view, request, **kwargs)
        response = view.dispatch(view.request, *view.args, **view.kwargs)
        self.assertEqual(response.status_code, 200)

    def test_get_queryset_for_anonymous_user(self):
        view = self.cls_view()
        request = RequestFactory().get(self.path)
        request.user = self.dummy_user
        kwargs = {}
        view = setup_view(view, request, **kwargs)
        expected = [self.john, self.paul, self.ringo]
        self.assertEqual(view.get_queryset(), expected)

    def test_get_queryset_for_staff_user(self):
        self.client.login(username='john', password='secret')

        view = self.cls_view()
        request = RequestFactory().get(self.path)
        request.user = self.john
        kwargs = {}
        view = setup_view(view, request, **kwargs)

        qs = view.get_queryset()
        self.assertEqual(qs[0], self.george)
        self.assertEqual(qs[1], self.john)
        self.assertEqual(qs[2], self.paul)
        self.assertEqual(qs[3], self.ringo)

    def test_get_context_data(self):
        self.client.login(username='john', password='secret')

        view = self.cls_view()
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        view = setup_view(view, request, **kwargs)

        response = view.dispatch(view.request, *view.args, **view.kwargs)
        context = view.get_context_data(**kwargs)
        self.assertEqual(context['arr'            ], {0: {0: {'id': '3', 'model': 'user', 'name': 'george'}, 1: 'george', 2: '', 3: '', 4: '', 5: self.george.date_joined, 6: '', 7: True, 8: False}, 1: {0: {'id': '1', 'model': 'user', 'name': 'john'}, 1: 'john', 2: '', 3: '', 4: '', 5: self.john.date_joined, 6: '', 7: True, 8: True}, 2: {0: {'id': '2', 'model': 'user', 'name': 'paul'}, 1: 'paul', 2: '', 3: '', 4: '', 5: self.paul.date_joined, 6: '', 7: True, 8: True}, 3: {0: {'id': '4', 'model': 'user', 'name': 'ringo'}, 1: 'ringo', 2: '', 3: '', 4: '', 5: self.ringo.date_joined, 6: '', 7: True, 8: False}})
        self.assertEqual(context['browTabName'    ], "users_table")
        self.assertEqual(context['cap'            ], {0: '', 1: 'Логін', 2: 'Користувач', 3: 'Кв.', 4: 'e-mail', 5: 'Дата ств.', 6: 'Підтв.', 7: 'Актив.', 8: 'Чл.кооп.'})
        self.assertEqual(context['selElementID'   ], None)
        self.assertEqual(context['selElementModel'], None)
        self.assertEqual(context['selRowIndex'    ], 0)

        j_arr = deepcopy(context['arr'])   # arr - змінюваний об'єкт!
        for i in j_arr:
            if j_arr[i][5]: j_arr[i][5] = j_arr[i][5].isoformat()
        json_arr = json.dumps(j_arr)
        self.assertEqual(context['json_arr'       ], json_arr)
        self.assertEqual(request.session['Selections'], {'users_table': {'': {'model': None, 'id': None, 'selRowIndex': 0}}})


class AjaxAccountTestBase(TestCase):

    def setUp(self):
        self.msg = types.SimpleNamespace(title   = "",
                                        type    = "",
                                        message = "",
                                        )
        self.sendMail = False

        DummyUser().create_dummy_group(group_name='members')
        DummyUser().create_dummy_group(group_name='staff')
        self.john   = DummyUser().create_dummy_user(id=1, username='john', password='secret', email='john@gmail.com')
        self.paul   = DummyUser().create_dummy_user(id=2, username='paul', password='secret')
        self.george = DummyUser().create_dummy_user(id=3, username='george', password='secret')
        self.ringo  = DummyUser().create_dummy_user(id=4, username='ringo', password='secret')
        self.freddy = DummyUser().create_dummy_user(id=5, username='freddy', password='secret', email='freddy@gmail.com')

        # john буде логінитись і має доступ
        self.john.is_staff = True
        DummyUser().add_dummy_group(self.john  , 'staff')
        DummyUser().add_dummy_permission(self.john, 'activate_account')

        self.set_parameters_to_user(self.john,   True,  True,  True)
        self.set_parameters_to_user(self.paul,   True,  True,  False)
        self.set_parameters_to_user(self.george, True,  False, False)
        self.set_parameters_to_user(self.ringo,  None,  False, False)
        self.set_parameters_to_user(self.freddy, False, False, False)

    def set_parameters_to_user(self, user, is_recognized=None, is_active=False, is_member=False):
        if is_recognized != None:
            DummyUser().create_dummy_profile(user)
            user.userprofile.is_recognized = is_recognized
            user.userprofile.save()
        user.is_active = is_active
        if is_member:
            DummyUser().add_dummy_group(user, 'members')
        else:
            DummyUser().remove_dummy_group(user, 'members')
        user.save()

    def check_view_response_container_data(self,
                                            response=None,
                                            expected_title=None,
                                            expected_type=None,
                                            expected_message=None,
                                            expected_changes=None,
                                            expected_supplement=None,
                                            expected_status_code=200
                                           ):
        d = dict_from_json_str_or_bytes(response._container[0])

        # Чи ф-ція повертає правильний response?
        self.assertEqual(d['title'     ], expected_title     )
        self.assertEqual(d['type'      ], expected_type      )
        self.assertEqual(d['message'   ], expected_message   )
        self.assertEqual(d['changes'   ], expected_changes   )
        self.assertEqual(d['supplement'], expected_supplement)
        expected = {'content-type': ('Content-Type', 'application/json')}
        self.assertEqual(response._headers, expected)
        self.assertEqual(response.status_code, expected_status_code)

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

    def get_kwargs_for_ajax_data(self, elemSet):
        kwargs = {
                    'browTabName' : 'users_table',
                    'parent_id'   : "",
                    'sendMail'    : "",
                    'selRowIndex' : '0',
                    'elemSet'     : elemSet,
                }
        return kwargs

    def get_expected(self, user, changes_678, suppl_678):
        # Очікувані дані з response
        id = str(user.id)
        name = user.username
        model = "user"
        expected_model      = model
        expected_id         = str(id)
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


# @skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxAccountViewTest(AjaxAccountTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxAccountViewBase

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.msg     , self.msg     )
        self.assertEqual(view.sendMail, self.sendMail)

    def test_get_request_data(self):
        view = self.cls_view
        kwargs = {
                    'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'1',
                    'name'        :'john',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        user, profile = view().get_request_data(request)
        # Чи метод повертає правильні записи?
        self.assertEqual(user, self.john)
        self.assertEqual(profile, self.john.userprofile)


    def test_get_request_data_2_no_profile(self):
        view = self.cls_view
        kwargs = {
                    'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'4',
                    'name'        :'ringo',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        user, profile = view().get_request_data(request)
        # Чи метод повертає правильні записи?
        self.assertEqual(user, self.ringo)
        self.assertEqual(profile, None)

    def test_get_request_data_3_no_user(self):
        view = self.cls_view
        kwargs = {
                    'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'99',
                    'name'        :'paul',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        user, profile = view().get_request_data(request)
        # Чи метод повертає правильні записи?
        self.assertEqual(user, None)
        self.assertEqual(profile, None)

    def test_get_request_data_4_no_model(self):
        view = self.cls_view
        kwargs = {
                    'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'',
                    'id'          :'99',
                    'name'        :'paul',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        user, profile = view().get_request_data(request)
        # Чи метод повертає правильні записи?
        self.assertEqual(user, None)
        self.assertEqual(profile, None)

    def test_get_request_data_4_model_mismatch_table_name(self):
        view = self.cls_view
        kwargs = {
                    'browTabName' :'folders_contents',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'99',
                    'name'        :'paul',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        user, profile = view().get_request_data(request)
        # Чи метод повертає правильні записи?
        self.assertEqual(user, None)
        self.assertEqual(profile, None)

    def test_get_request_data_5_no_table_name(self):
        view = self.cls_view
        kwargs = {
                    'browTabName' :'',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'99',
                    'name'        :'paul',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        user, profile = view().get_request_data(request)
        # Чи метод повертає правильні записи?
        self.assertEqual(user, None)
        self.assertEqual(profile, None)

    def test_get_request_data_6_unknown_table_name(self):
        view = self.cls_view
        kwargs = {
                    'browTabName' :'FOLDER',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'99',
                    'name'        :'paul',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        user, profile = view().get_request_data(request)
        # Чи метод повертає правильні записи?
        self.assertEqual(user, None)
        self.assertEqual(profile, None)

        # Метод processing тестується у дочірніх класах

    def test_send_e_mail(self):
        view = self.cls_view()
        view.sendMail = True
        user = self.freddy

        e_msg_body = "Ваш акаунт на сайті підтверджено!"
        view.send_e_mail(user, e_msg_body)

        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.recipients(), [user.email])
        self.assertEqual(msg.subject, 'KoopSite administrator')
        self.assertIn(e_msg_body, msg.body)

    def test_send_e_mail_no_address(self):
        view = self.cls_view()
        view.sendMail = True
        user = self.paul
        e_msg_body = "Ваш акаунт на сайті підтверджено!"
        view.send_e_mail(user, e_msg_body)
        self.assertEqual(len(mail.outbox), 0)

    def test_send_e_mail_not_send(self):
        view = self.cls_view()
        view.sendMail = False
        user = self.freddy
        e_msg_body = "Ваш акаунт на сайті підтверджено!"
        view.send_e_mail(user, e_msg_body)
        self.assertEqual(len(mail.outbox), 0)

    def test_handler(self):
        view = self.cls_view()
        kwargs = {
                    'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'1',
                    'name'        :'john',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "john"
        expected_type       = "NoChange"
        expected_message    = "Акаунт раніше вже був підтверджений!"
        expected_changes    = {'0': {'id': '1', 'name': 'john', 'model': 'user'},
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-yes.gif',
                            '8': '/static/admin/img/icon-yes.gif',
                            }}
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}

        response = view.handler(request)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)

    def test_handler_return_empty_response_if_no_client_request(self):
        view = self.cls_view()

        request = self.client.request()
        request.POST = {}
        response = view.handler(request)
        self.assertTrue(isinstance(response, HttpResponse))
        expected = [b"There is no 'client_request' in request.POST"]
        self.assertEqual(response._container, expected)
        expected = {'content-type': ('Content-Type', 'text/html; charset=utf-8')}
        self.assertEqual(response._headers, expected)

    def test_handler_return_empty_response_if_no_element(self):
        view = self.cls_view()
        kwargs = {
                    'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'',
                    'name'        :'john',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        response = view.handler(request)
        self.assertTrue(isinstance(response, HttpResponse))
        expected = [b'There is no user in request.POST']
        self.assertEqual(response._container, expected)
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
class AjaxRecognizeAccountTest(AjaxAccountTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxRecognizeAccount
        self.path = '/adm/users/ajax-recognize-account'

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_dispatch(self):
        view = self.cls_view()
        request = self.client.request()
        request.POST = {}
        request.user = self.john
        request.session = {}
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_view_gives_response_status_code_400_empty_request(self):
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
        self.client.login(username='paul', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_processing_no_changes_made(self):
        view = self.cls_view()
        user0 = self.john
        prof0 = user0.userprofile
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.NoChange)
        self.assertEqual(msg.message, "Акаунт раніше вже був підтверджений!")

    def test_processing_changes_made(self):
        view = self.cls_view()
        user0 = self.ringo
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(prof_db.is_recognized, True)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Change)
        self.assertEqual(msg.message, "Акаунт підтверджено!")

    def test_view_response_container_data_no_changes(self):
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'1',
                    'name'        :'john',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "john"
        expected_type       = "NoChange"
        expected_message    = "Акаунт раніше вже був підтверджений!"
        expected_changes    = {'0': {'id': '1', 'name': 'john', 'model': 'user'},
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-yes.gif',
                            '8': '/static/admin/img/icon-yes.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)

    def test_view_response_container_data_Make_changes(self):
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'5',
                    'name'        :'freddy',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "freddy"
        expected_type       = "Change"
        expected_message    = "Акаунт підтверджено!"
        expected_changes    = {'0': {'id': '5', 'name': 'freddy', 'model': 'user'},
                               '6': True,
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-no.gif',
                            '8': '/static/admin/img/icon-no.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)

    def test_view_response_container_data_Make_changes_no_profile(self):
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'4',
                    'name'        :'ringo',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "ringo"
        expected_type       = "Change"
        expected_message    = "Акаунт підтверджено!"
        expected_changes    = {'0': {'id': '4', 'name': 'ringo', 'model': 'user'},
                               '6': True,
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-no.gif',
                            '8': '/static/admin/img/icon-no.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)


@skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxDenyAccountTest(AjaxAccountTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxDenyAccount
        self.path = '/adm/users/ajax-deny-account'

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_dispatch(self):
        view = self.cls_view()
        request = self.client.request()
        request.POST = {}
        request.user = self.john
        request.session = {}
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_view_gives_response_status_code_400_empty_request(self):
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
        self.client.login(username='paul', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_processing_no_changes_made(self):
        view = self.cls_view()
        user0 = self.freddy
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.NoChange)
        self.assertEqual(msg.message, "Акаунт раніше вже був відхилений!")

    def test_processing_changes_made(self):
        view = self.cls_view()
        user0 = self.george
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(prof_db.is_recognized, False)
        self.assertEqual(user_db.is_active, False)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Change)
        self.assertEqual(msg.message, "Акаунт відхилено і деактивовано!")

    def test_processing_changes_made_no_profile(self):
        view = self.cls_view()
        user0 = self.ringo
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(prof_db.is_recognized, False)
        self.assertEqual(user_db.is_active, False)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Change)
        self.assertEqual(msg.message, "Акаунт відхилено і деактивовано!")

    def test_view_response_container_data_No_changes(self):
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'5',
                    'name'        :'freddy',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "freddy"
        expected_type       = "NoChange"
        expected_message    = "Акаунт раніше вже був відхилений!"
        expected_changes    = {'0': {'id': '5', 'name': 'freddy', 'model': 'user'},
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-no.gif',
                            '7': '/static/admin/img/icon-no.gif',
                            '8': '/static/admin/img/icon-no.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)

    def test_view_response_container_data_Make_changes(self):
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'2',
                    'name'        :'paul',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "paul"
        expected_type       = "Change"
        expected_message    = "Акаунт відхилено і деактивовано!"
        expected_changes    = {'0': {'id': '2', 'name': 'paul', 'model': 'user'},
                               '6': False,
                               '7': False,
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-no.gif',
                            '7': '/static/admin/img/icon-no.gif',
                            '8': '/static/admin/img/icon-no.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)

    def test_view_response_container_data_Make_changes_no_profile(self):
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'4',
                    'name'        :'ringo',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "ringo"
        expected_type       = "Change"
        expected_message    = "Акаунт відхилено і деактивовано!"
        expected_changes    = {'0': {'id': '4', 'name': 'ringo', 'model': 'user'},
                               '6': False,
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-no.gif',
                            '7': '/static/admin/img/icon-no.gif',
                            '8': '/static/admin/img/icon-no.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)


@skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxActivateAccountTest(AjaxAccountTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxActivateAccount
        self.path = '/adm/users/ajax-activate-account'

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_dispatch(self):
        view = self.cls_view()
        request = self.client.request()
        request.POST = {}
        request.user = self.john
        request.session = {}
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_view_gives_response_status_code_400_empty_request(self):
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
        self.client.login(username='paul', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_processing_no_changes_made(self):
        view = self.cls_view()
        user0 = self.john
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.NoChange)
        self.assertEqual(msg.message, "Акаунт вже активний!")

    def test_processing_error_account_is_denied(self):
        view = self.cls_view()
        user0 = self.freddy
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Відхилений Акаунт не можна активувати!")

    def test_processing_changes_made(self):
        view = self.cls_view()
        user0 = self.george
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(user_db.is_active, True)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Change)
        self.assertEqual(msg.message, "Акаунт активовано!")

    def test_processing_changes_made_no_profile(self):
        view = self.cls_view()
        user0 = self.ringo
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(user_db.is_active, True)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Change)
        self.assertEqual(msg.message, "Акаунт активовано!")

    def test_view_response_container_data_No_changes(self):
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'1',
                    'name'        :'john',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "john"
        expected_type       = "NoChange"
        expected_message    = "Акаунт вже активний!"
        expected_changes    = {'0': {'id': '1', 'name': 'john', 'model': 'user'},
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-yes.gif',
                            '8': '/static/admin/img/icon-yes.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)

    def test_view_response_container_data_Make_changes(self):
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'3',
                    'name'        :'george',
                }
        self.paul.userprofile.is_recognized = False
        self.paul.userprofile.save()
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "george"
        expected_type       = "Change"
        expected_message    = "Акаунт активовано!"
        expected_changes    = {'0': {'id': '3', 'name': 'george', 'model': 'user'},
                               '7': True,
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-yes.gif',
                            '8': '/static/admin/img/icon-no.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)


@skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxDeactivateAccountTest(AjaxAccountTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxDeactivateAccount
        self.path = '/adm/users/ajax-deactivate-account'

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_dispatch(self):
        view = self.cls_view()
        request = self.client.request()
        request.POST = {}
        request.user = self.john
        # request.session = {}
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_view_gives_response_status_code_400_empty_request(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.john
        # request.session = {}
        kwargs = {}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 400)

    def test_view_response_raise_exception_AnonymousUser(self):
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        # request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_view_response_raise_exception_user_w_o_permission(self):
        self.client.login(username='paul', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        # request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_processing_no_changes_made(self):
        view = self.cls_view()
        user0 = self.george
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.NoChange)
        self.assertEqual(msg.message, "Акаунт вже неактивний!")

    def test_processing_changes_made(self):
        view = self.cls_view()
        user0 = self.paul
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(user_db.is_active, False)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Change)
        self.assertEqual(msg.message, "Акаунт деактивовано!")

    def test_view_response_container_data_No_changes(self):
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'3',
                    'name'        :'george',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "george"
        expected_type       = "NoChange"
        expected_message    = "Акаунт вже неактивний!"
        expected_changes    = {'0': {'id': '3', 'name': 'george', 'model': 'user'},
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-no.gif',
                            '8': '/static/admin/img/icon-no.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        # request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)

    def test_view_response_container_data_Make_changes(self):
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'2',
                    'name'        :'paul',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "paul"
        expected_type       = "Change"
        expected_message    = "Акаунт деактивовано!"
        expected_changes    = {'0': {'id': '2', 'name': 'paul', 'model': 'user'},
                               '7': False,
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-no.gif',
                            '8': '/static/admin/img/icon-no.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        # request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)


@skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxSetMemberAccountTest(AjaxAccountTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxSetMemberAccount
        self.path = '/adm/users/ajax-set-member-account'

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_dispatch(self):
        view = self.cls_view()
        request = self.client.request()
        request.POST = {}
        request.user = self.john
        request.session = {}
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_view_gives_response_status_code_400_empty_request(self):
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
        self.client.login(username='paul', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_processing_no_changes_made(self):
        view = self.cls_view()
        user0 = self.john
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.NoChange)
        self.assertEqual(msg.message, "Акаунт вже має ці права доступу!")

    def test_processing_error_account_is_denied(self):
        view = self.cls_view()
        user0 = self.freddy
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Відхилений Акаунт не може отримати права доступу!")

    def test_processing_error_account_is_not_recognized(self):
        view = self.cls_view()
        user0 = self.ringo
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Непідтверджений Акаунт не може отримати права доступу!")

    def test_processing_changes_made(self):
        view = self.cls_view()
        user0 = self.george
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(has_group(user_db, 'members'), True)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Change)
        self.assertEqual(msg.message, "Права доступу встановлено!")

    def test_view_response_container_data_No_changes(self):
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'1',
                    'name'        :'john',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "john"
        expected_type       = "NoChange"
        expected_message    = "Акаунт вже має ці права доступу!"
        expected_changes    = {'0': {'id': '1', 'name': 'john', 'model': 'user'},
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-yes.gif',
                            '8': '/static/admin/img/icon-yes.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)

    def test_view_response_container_data_Make_changes(self):
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'2',
                    'name'        :'paul',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "paul"
        expected_type       = "Change"
        expected_message    = "Права доступу встановлено!"
        expected_changes    = {'0': {'id': '2', 'name': 'paul', 'model': 'user'},
                               '8': True,
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-yes.gif',
                            '8': '/static/admin/img/icon-yes.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)


@skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxDenyMemberAccountTest(AjaxAccountTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxDenyMemberAccount
        self.path = '/adm/users/ajax-deny-member-account'

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_dispatch(self):
        view = self.cls_view()
        request = self.client.request()
        request.POST = {}
        request.user = self.john
        request.session = {}
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_view_gives_response_status_code_400_empty_request(self):
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
        self.client.login(username='paul', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_processing_no_changes_made(self):
        view = self.cls_view()
        user0 = self.paul
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.NoChange)
        self.assertEqual(msg.message, "Акаунт вже позбавлений цього права доступу!")

    def test_processing_changes_made(self):
        view = self.cls_view()
        user0 = self.john
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(has_group(user_db, 'members'), False)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Change)
        self.assertEqual(msg.message, "Право доступу вилучено!")

    def test_view_response_container_data_No_changes(self):
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'2',
                    'name'        :'paul',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "paul"
        expected_type       = "NoChange"
        expected_message    = "Акаунт вже позбавлений цього права доступу!"
        expected_changes    = {'0': {'id': '2', 'name': 'paul', 'model': 'user'},
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-yes.gif',
                            '8': '/static/admin/img/icon-no.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)

    def test_view_response_container_data_Make_changes(self):
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'1',
                    'name'        :'john',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "john"
        expected_type       = "Change"
        expected_message    = "Право доступу вилучено!"
        expected_changes    = {'0': {'id': '1', 'name': 'john', 'model': 'user'},
                               '8': False,
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-yes.gif',
                            '8': '/static/admin/img/icon-no.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)


@skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxDeleteAccountTest(AjaxAccountTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxDeleteAccount
        self.path = '/adm/users/ajax-delete-account'
        DummyUser().add_dummy_permission(self.john, 'delete_user', model='user')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_dispatch(self):
        view = self.cls_view()
        request = self.client.request()
        request.POST = {}
        request.user = self.john
        request.session = {}
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_view_gives_response_status_code_400_empty_request(self):
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
        self.client.login(username='paul', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_processing_error_account_is_active(self):
        view = self.cls_view()
        user0 = self.paul
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Активний акаунт не можна видалити!")

    def test_processing_error_account_is_recognized(self):
        view = self.cls_view()
        user0 = self.george
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Видалити можна лише відхилений акаунт!")

    def test_processing_error_account_no_profile(self):
        view = self.cls_view()
        user0 = self.ringo
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Видалити можна лише відхилений акаунт!")

    def test_processing_account_deleted(self):
        view = self.cls_view()
        user0 = self.freddy
        prof0 = getattr(user0, 'userprofile', None)
        u_name = user0.username
        u_id = user0.id
        p_id = prof0.id
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=u_id)
        prof_db = get_or_none(UserProfile, id=p_id)
        self.assertEqual(user, None)
        self.assertEqual(user_db, None)
        self.assertEqual(prof_db, None)
        self.assertEqual(msg.title  , u_name)
        self.assertEqual(msg.type   , msgType.DeleteRow)
        self.assertEqual(msg.message, "Акаунт видалено!")

    def test_view_response_container_data_Error_account_is_active(self):
        # print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'1',
                    'name'        :'john',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "john"
        expected_type       = "Error"
        expected_message    = "Активний акаунт не можна видалити!"
        expected_changes    = {'0': {'id': '1', 'name': 'john', 'model': 'user'},
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-yes.gif',
                            '8': '/static/admin/img/icon-yes.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)

    def test_view_response_container_data_Error_account_is_recognized(self):
        # print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'3',
                    'name'        :'george',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "george"
        expected_type       = "Error"
        expected_message    = "Видалити можна лише відхилений акаунт!"
        expected_changes    = {'0': {'id': '3', 'name': 'george', 'model': 'user'},
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-no.gif',
                            '8': '/static/admin/img/icon-no.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)

    def test_view_response_container_data_delete_account(self):
        # print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'5',
                    'name'        :'freddy',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()

        # Очікувані дані з response
        expected_title      = "freddy"
        expected_type       = "DeleteRow"
        expected_message    = "Акаунт видалено!"
        expected_changes    = None
        expected_supplement = None
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)


