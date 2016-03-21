import json
from unittest.case import skipIf
from django.contrib.auth.models import User, AnonymousUser
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import resolve
from django.http.response import HttpResponse
from django.test.client import RequestFactory
from koopsite.functions import get_or_none, has_group
from koopsite.models import UserProfile
from koopsite.settings import SKIP_TEST
from koopsite.tests.test_views import setup_view
from koopsite.tests.test_viewsajax import DummyAjaxRequest
from koopsite.tests.test_viewsajaxuser import AjaxAccountTestBase
from koopsite.viewsajax import msgType
from koopsite.viewsajaxuser import AjaxAllAccountsViewBase, \
            AjaxActivateAllAccounts, AjaxSetMemberAllAccounts


# @skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxAllAccountsViewTest(AjaxAccountTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxAllAccountsViewBase

    # def test_view_model_and_attributes(self):
    #     view = self.cls_view()

    def test__init__(self):
        view = self.cls_view()

        self.assertEqual(view.empty_msg, self.msg     )
        # self.assertEqual(view.group_msg, self.msg     )
        self.assertEqual(view.sendMail , self.sendMail)
        self.assertEqual(view.group_msg.title  ,"Активація групи акаунтів")
        self.assertEqual(view.group_msg.type   ,msgType.Group)
        self.assertEqual(view.group_msg.message,"")
        self.assertEqual(view.counter          , {
                                                "вже активні" : 0,
                                                "відхилені"   : 0,
                                                'непідтверджені': 0,
                                                "активовано"  : 0,
                                                }
        )

    def test_init_counter(self):
        view = self.cls_view()
        view.init_counter()
        self.assertEqual(view.group_msg.title  ,"Активація групи акаунтів")
        self.assertEqual(view.group_msg.type   ,msgType.Group)
        self.assertEqual(view.group_msg.message,"")
        self.assertEqual(view.counter          , {
                                                "вже активні" : 0,
                                                "відхилені"   : 0,
                                                "непідтверджені": 0,
                                                "активовано"  : 0,
                                                }
        )

    def test_get_request_data_set(self):
        view = self.cls_view
        users_list = [self.john, self.paul, self.george, self.ringo]
        elemSet = self.get_elemSet(users_list)
        kwargs = self.get_kwargs_for_ajax_data(elemSet)
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        users_set = view().get_request_data_set(request)
        # Чи метод повертає правильні записи?
        expected_users_list = users_list
        self.assertEqual(users_set, expected_users_list)

    def test_get_request_data_set_2_no_users(self):
        view = self.cls_view
        users_list = []
        elemSet = self.get_elemSet(users_list)
        kwargs = self.get_kwargs_for_ajax_data(elemSet)
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        users_set = view().get_request_data_set(request)
        # Чи метод повертає правильні записи?
        expected_users_list = []
        self.assertEqual(users_set, expected_users_list)

    def test_get_request_data_set_3_no_model(self):
        view = self.cls_view
        users_list = [self.john, self.paul, self.george, self.ringo]
        elemSet = self.get_elemSet(users_list)
        kwargs = self.get_kwargs_for_ajax_data(elemSet)
        kwargs['elemSet'][0]['model'] = ""
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        users_set = view().get_request_data_set(request)
        # Чи метод повертає правильні записи?
        expected_users_set = users_list[1:]
        self.assertEqual(users_set, expected_users_set)


    def test_get_request_data_set_4_model_mismatch_table_name(self):
        view = self.cls_view
        users_list = [self.john, self.paul, self.george, self.ringo]
        elemSet = self.get_elemSet(users_list)
        kwargs = self.get_kwargs_for_ajax_data(elemSet)
        kwargs['browTabName'] = 'folders_contents'
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        users_set = view().get_request_data_set(request)
        # Чи метод повертає правильні записи?
        expected_users_set = None
        self.assertEqual(users_set, expected_users_set)


    def test_get_request_data_set_5_no_table_name(self):
        view = self.cls_view
        users_list = [self.john, self.paul, self.george, self.ringo]
        elemSet = self.get_elemSet(users_list)
        kwargs = self.get_kwargs_for_ajax_data(elemSet)
        kwargs['browTabName'] = ''
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        users_set = view().get_request_data_set(request)
        # Чи метод повертає правильні записи?
        expected_users_set = None
        self.assertEqual(users_set, expected_users_set)


    def test_get_request_data_set_6_unknown_table_name(self):
        view = self.cls_view
        users_list = [self.john, self.paul, self.george, self.ringo]
        elemSet = self.get_elemSet(users_list)
        kwargs = self.get_kwargs_for_ajax_data(elemSet)
        kwargs['browTabName'] = 'FOLDER'
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        users_set = view().get_request_data_set(request)
        # Чи метод повертає правильні записи?
        expected_users_set = None
        self.assertEqual(users_set, expected_users_set)

    """
    Метод processing треба переозначити у дочірньому класі.
    Тут наводиться приклад тесту.
    """
    def test_processing_no_changes_made(self):
        view = self.cls_view()
        user0 = self.john
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.empty_msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.NoChange)
        self.assertEqual(msg.message, "Акаунт вже активний!")
        self.assertEqual(view.counter["вже активні"], 1)

    def test_processing_error_account_is_denied(self):
        view = self.cls_view()
        user0 = self.george
        prof0 = getattr(user0, 'userprofile', None)
        prof0.is_recognized = False
        prof0.save()
        user, msg = view.processing(user0, prof0, view.empty_msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Відхилений Акаунт не можна активувати!")
        self.assertEqual(view.counter["відхилені"], 1)

    def test_processing_changes_made(self):
        view = self.cls_view()
        user0 = self.george
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.empty_msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(user_db.is_active, True)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Change)
        self.assertEqual(msg.message, "Акаунт активовано!")
        self.assertEqual(view.counter["активовано"], 1)

    def test_processing_changes_made_no_profile(self):
        view = self.cls_view()
        user0 = self.ringo
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.empty_msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(user_db.is_active, False)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Непідтверджений Акаунт не можна активувати!")
        self.assertEqual(view.counter["непідтверджені"], 1)

        # TODO-2016 02 01 додати перевірку self.send_e_mail(user, e_msg_body)

    def test_group_processing(self):
        view = self.cls_view()
        users_list = [self.john, self.paul, self.george, self.ringo, self.freddy]

        # Очікувані дані
        expected_set = []
        expected_set.append(self.get_expected(
                                    self.john,
                                    {},
                                    {6: 'yes', 7: 'yes', 8: 'yes',})
                            )
        expected_set.append(self.get_expected(
                                    self.paul,
                                    {},
                                    {6: 'yes', 7: 'yes', 8: 'no',})
                            )
        expected_set.append(self.get_expected(
                                    self.george,
                                    {7: True},
                                    {6: 'yes', 7: 'yes', 8: 'no',})
                            )
        expected_set.append(self.get_expected(
                                    self.ringo,
                                    {},
                                    {6: 'unknown', 7: 'no', 8: 'no',})
                            )
        expected_set.append(self.get_expected(
                                    self.freddy,
                                    {},
                                    {6: 'no', 7: 'no', 8: 'no',})
                            )


        response_set = view.group_processing(users_list)

        # Чи метод повертає правильні записи?

        self.assertEqual(len(response_set), len(users_list))
        for i in range(len(users_list)):
            self.check_view_response_cont(response_set[i], False, *expected_set[i])

    def test_group_handler(self):
        view = self.cls_view()
        users_list = [self.john, self.paul, self.george, self.ringo, self.freddy]
        elemSet = self.get_elemSet(users_list)
        kwargs = self.get_kwargs_for_ajax_data(elemSet)
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()

        # Очікувані дані з response
        expected_set = []
        expected_set.append(self.get_expected(
                                    self.john,
                                    {},
                                    {6: 'yes', 7: 'yes', 8: 'yes',})
                            )
        expected_set.append(self.get_expected(
                                    self.paul,
                                    {},
                                    {6: 'yes', 7: 'yes', 8: 'no',})
                            )
        expected_set.append(self.get_expected(
                                    self.george,
                                    {7: True},
                                    {6: 'yes', 7: 'yes', 8: 'no',})
                            )
        expected_set.append(self.get_expected(
                                    self.ringo,
                                    {},
                                    {6: 'unknown', 7: 'no', 8: 'no',})
                            )
        expected_set.append(self.get_expected(
                                    self.freddy,
                                    {},
                                    {6: 'no', 7: 'no', 8: 'no',})
                            )
        expected_messsage = "<tr><td>  Оброблено акаунтів:</td><td>  5</td></tr><tr><td>          активовано:</td><td>  1</td></tr><tr><td>         вже активні:</td><td>  2</td></tr><tr><td>           відхилені:</td><td>  1</td></tr><tr><td>      непідтверджені:</td><td>  1</td></tr>"

        request = self.client.request()
        request.POST = ajax_data
        request.session = {}

        response = view.group_handler(request)
        group_response_cont = json.loads(response._container[0].decode())
        response_set = group_response_cont['group']
        self.assertEqual(len(response_set), len(users_list))
        for i in range(len(users_list)):
            self.check_view_response_cont(response_set[i], True, *expected_set[i])
        self.assertEqual(group_response_cont['title'], "Активація групи акаунтів")
        self.assertEqual(group_response_cont['type'], "Group")
        message = group_response_cont['message']
        self.assertHTMLEqual(message, expected_messsage)


    def test_group_handler_return_empty_response_if_no_client_request(self):
        view = self.cls_view()

        request = self.client.request()
        request.POST = {}
        response = view.group_handler(request)
        self.assertTrue(isinstance(response, HttpResponse))
        self.assertEqual(response._container, [b''])
        expected = {'content-type': ('Content-Type', 'text/html; charset=utf-8')}
        self.assertEqual(response._headers, expected)

    def test_dispatch(self):
        view = self.cls_view()

        request = self.client.request()
        request.POST = {}
        response = view.dispatch(request)
        expected_response = view.group_handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)


@skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxActivateAllAccountsTest(AjaxAccountTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxActivateAllAccounts
        self.path = '/adm/users/ajax-activate-all-accounts'

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
        expected_response = view.group_handler(request)
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
        user, msg = view.processing(user0, prof0, view.empty_msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.NoChange)
        self.assertEqual(msg.message, "Акаунт вже активний!")
        self.assertEqual(view.counter["вже активні"], 1)

    def test_processing_error_account_is_denied(self):
        view = self.cls_view()
        user0 = self.george
        prof0 = getattr(user0, 'userprofile', None)
        prof0.is_recognized = False
        prof0.save()
        user, msg = view.processing(user0, prof0, view.empty_msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Відхилений Акаунт не можна активувати!")
        self.assertEqual(view.counter["відхилені"], 1)

    def test_processing_changes_made(self):
        view = self.cls_view()
        user0 = self.george
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.empty_msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(user_db.is_active, True)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Change)
        self.assertEqual(msg.message, "Акаунт активовано!")
        self.assertEqual(view.counter["активовано"], 1)

    def test_processing_changes_made_no_profile(self):
        view = self.cls_view()
        user0 = self.ringo
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.empty_msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(user_db.is_active, False)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Непідтверджений Акаунт не можна активувати!")
        self.assertEqual(view.counter["непідтверджені"], 1)

    def test_view_response_container_data(self):
        view = self.cls_view()
        users_list = [self.john, self.paul, self.george, self.ringo, self.freddy]
        elemSet = self.get_elemSet(users_list)
        kwargs = self.get_kwargs_for_ajax_data(elemSet)
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()

        # Очікувані дані з response
        expected_set = []
        expected_set.append(self.get_expected(
                                    self.john,
                                    {},
                                    {6: 'yes', 7: 'yes', 8: 'yes',})
                            )
        expected_set.append(self.get_expected(
                                    self.paul,
                                    {},
                                    {6: 'yes', 7: 'yes', 8: 'no',})
                            )
        expected_set.append(self.get_expected(
                                    self.george,
                                    {7: True},
                                    {6: 'yes', 7: 'yes', 8: 'no',})
                            )
        expected_set.append(self.get_expected(
                                    self.ringo,
                                    {},
                                    {6: 'unknown', 7: 'no', 8: 'no',})
                            )
        expected_set.append(self.get_expected(
                                    self.freddy,
                                    {},
                                    {6: 'no', 7: 'no', 8: 'no',})
                            )

        request = self.client.request()
        request.POST = ajax_data
        request.user = self.john
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        group_response_cont = json.loads(response._container[0].decode())
        response_set = group_response_cont['group']
        self.assertEqual(len(response_set), len(users_list))
        for i in range(len(users_list)):
            self.check_view_response_cont(response_set[i], True, *expected_set[i])



@skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxSetMemberAllAccountsTest(AjaxAccountTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxSetMemberAllAccounts
        self.path = '/adm/users/ajax-set-member-all-accounts'

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
        expected_response = view.group_handler(request)
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
        # prof0.is_recognized = False
        # prof0.save()
        user, msg = view.processing(user0, prof0, view.empty_msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.NoChange)
        self.assertEqual(msg.message, "Акаунт вже має ці права доступу!")
        self.assertEqual(view.counter["доступ вже є"], 1)

    def test_processing_error_account_is_denied(self):
        view = self.cls_view()
        user0 = self.george
        prof0 = getattr(user0, 'userprofile', None)
        prof0.is_recognized = False
        prof0.save()
        user, msg = view.processing(user0, prof0, view.empty_msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Відхилений Акаунт не може отримати права доступу!")
        self.assertEqual(view.counter["відхилені"], 1)

    def test_processing_changes_made(self):
        view = self.cls_view()
        user0 = self.george
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.empty_msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(has_group(user_db, 'members'), True)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Change)
        self.assertEqual(msg.message, "Права доступу встановлено!")
        self.assertEqual(view.counter["встановлено"], 1)

    def test_processing_error_no_profile(self):
        view = self.cls_view()
        user0 = self.ringo
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.empty_msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Непідтверджений Акаунт не може отримати права доступу!")
        self.assertEqual(view.counter["непідтверджені"], 1)

    def test_view_response_container_data(self):
        view = self.cls_view()
        users_list = [self.john, self.paul, self.george, self.ringo, self.freddy]
        elemSet = self.get_elemSet(users_list)
        kwargs = self.get_kwargs_for_ajax_data(elemSet)
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()

        # Очікувані дані з response
        expected_set = []
        expected_set.append(self.get_expected(
                                    self.john,
                                    {},
                                    {6: 'yes', 7: 'yes', 8: 'yes',})
                            )
        expected_set.append(self.get_expected(
                                    self.paul,
                                    {8: True},
                                    {6: 'yes', 7: 'yes', 8: 'yes',})
                            )
        expected_set.append(self.get_expected(
                                    self.george,
                                    {8: True},
                                    {6: 'yes', 7: 'no', 8: 'yes',})
                            )
        expected_set.append(self.get_expected(
                                    self.ringo,
                                    {},
                                    {6: 'unknown', 7: 'no', 8: 'no',})
                            )
        expected_set.append(self.get_expected(
                                    self.freddy,
                                    {},
                                    {6: 'no', 7: 'no', 8: 'no',})
                            )

        request = self.client.request()
        request.POST = ajax_data
        request.user = self.john
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        group_response_cont = json.loads(response._container[0].decode())
        response_set = group_response_cont['group']
        self.assertEqual(len(response_set), len(users_list))
        for i in range(len(users_list)):
            self.check_view_response_cont(response_set[i], True, *expected_set[i])

