import inspect
from unittest.case import skipIf

from django.contrib.auth.models import AnonymousUser

from flats.models import Flat
from flats.tests.test_base import DummyFlat
from functional_tests.koopsite.ft_base import PageVisitTest
from koopsite.functions import get_flat_users
from koopsite.settings import SKIP_TEST


class FlatUsersListPageVisitTest(PageVisitTest):
    """
    Допоміжний клас для функціональних тестів.
    Описані тут параметри - для перевірки одної сторінки сайту.
    Цей клас буде використовуватися як основа
    для класів тестування цієї сторінки з іншими користувачами.
    """
    this_url    = '/flats/2/users-list/'
    page_title  = 'Пасічний'
    page_name   = 'Квартира № 2 : Список користувачів сайту'

    def setUp(self):
        john, paul, george, ringo, freddy = self.create_dummy_beatles()
        flat1, flat2 = self.set_flats_to_beatles(john, paul, george, ringo, freddy)
        self.add_dummy_permission(john, 'view_userprofile')
        self.john = john
        self.paul = paul
        self.flat1 = flat1
        self.flat2 = flat2

    def links_in_template(self, user):
        # Повертає список словників, які поступають як параметри до функції self.check_go_to_link(...)
        #     def check_go_to_link(self, this_url, link_parent_selector, link_text,
        #                           expected_regex=None, url_name=None, kwargs=None):
        # Ключі словників скорочені до 2-х літер: ls lt er un kw
        # плюс cd - condition для перевірки видимості лінка (буде аргументом ф-ції eval() ).
        # Спочатку визначаються деякі параметри:
        username, flat_id, flat_No = self.get_user_name_flat(user)
        s = [
            {'ls':'#body-navigation'          , 'lt': 'Головна сторінка' , 'un': 'index'},
            {'ls':'#body-navigation'          , 'lt': 'Схема будинку'    , 'un': 'flats:flat-scheme'},#########
            {'ls':'#body-navigation'          , 'lt': 'Список квартир'   , 'un': 'flats:flat-list'},
            {'ls':'#body-navigation'          , 'lt': 'Параметри квартир', 'un': 'flats:flat-table'},
            {'ls':'#body-navigation'          , 'lt': 'Схема користувачів','un': 'flats:flat-scheme-users', 'cd': "user.has_perm('koopsite.view_userprofile')"},
            {'ls':'#body-navigation'          , 'lt': 'Уверх'            , 'un': "flats:flat-scheme-users"},
            {'ls':'#header-aside-2-navigation', 'lt': username           , 'un': 'own-profile' , 'cd': "user.is_authenticated()"},
            {'ls':'#header-aside-2-navigation', 'lt': "Кв." + flat_No    , 'un': "flats:flat-detail", 'kw': {'pk': flat_id}, 'cd': "user.is_authenticated() and user.userprofile.flat"},
            {'ls':'#header-aside-2-navigation', 'lt': 'Вийти'            , 'un': 'logout'      , 'cd': "user.is_authenticated()", 'er': '/index/'},
            {'ls':'#header-aside-2-navigation', 'lt': 'Авторизуватися'   , 'un': 'login'       , 'cd': "not user.is_authenticated()"},
            ]
        return s

    def data_len(self):
        flat = Flat.objects.get(id=2)
        qs = get_flat_users(flat)
        return len(qs)

    def get_data_links_number(self):
        self.data_links_number = self.data_len() # кількість лінків, які приходять в шаблон з даними
        self.data_links_number += 0 # лінк javascript:history.back()
        return self.data_links_number


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FlatUsersListPageAuthenticatedVisitorWithPermsTest(FlatUsersListPageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        super().setUp()
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='view_userprofile')
        self.get_data_links_number()

    def test_can_visit_page(self):
        # Заголовок і назва сторінки правильні
        self.can_visit_page()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    def test_layout_and_styling_page(self):
        # CSS завантажено і працює
        self.layout_and_styling_page()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


# @skipIf(SKIP_TEST, "пропущено для економії часу")
class FlatUsersListPageAuthenticatedVisitorWithFlatTest(FlatUsersListPageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем з номером квартири)
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        super().setUp()
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='view_userprofile')
        profile = self.create_dummy_profile(user=self.dummy_user)
        flat = DummyFlat().create_dummy_flat()
        profile.flat=flat
        profile.save()
        self.get_data_links_number()

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FlatUsersListPageAnonymousVisitorTest(FlatUsersListPageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        super().setUp()
        self.dummy_user = AnonymousUser()
        # self.create_dummy_folder()
        self.get_data_links_number()

    def test_can_not_visit_page(self):
        # Заголовок і назва сторінки правильні
        self.can_not_visit_page()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FlatUsersListPageAuthenticatedVisitorWoPermsTest(FlatUsersListPageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        super().setUp()
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.get_data_links_number()

    def test_can_not_visit_page(self):
        # Заголовок і назва сторінки правильні
        self.can_not_visit_page()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FlatUsersListPageGoToDataLinkTest(FlatUsersListPageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    і переходу за лінком, вказаним в таблиці даних
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        super().setUp()
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='view_userprofile')
        self.get_data_links_number()

    def test_visitor_can_go_to_link(self):
        # Користувач може перейти по лінку потрібні дані
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        user = self.paul
        link_parent_selector = '#body-table'
        link_text            = user.username
        url_name             = 'adm-users-profile'
        kwargs               = {'pk': user.id}
        expected_regex       = ""
        self.check_go_to_link(self.this_url, link_parent_selector, link_text,
            url_name=url_name, kwargs=kwargs, expected_regex=expected_regex)
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FlatUsersListPageVisitorCanFindLinkTest(FlatUsersListPageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    Чи всі дані правильно відображені?
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        super().setUp()
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='view_userprofile')
        DummyFlat().create_dummy_building()
        self.get_data_links_number()

    def test_visitor_can_find_link(self):
        # Користувач може  перейти по лінку потрібні дані
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        for user in get_flat_users(self.flat2):
            link_parent_selector = '#body-table'
            link_text            = user.username
            url_name             = 'adm-users-profile'
            kwargs               = {'pk': user.id}
            expected_regex       = ""
            self.check_go_to_link(self.this_url, link_parent_selector, link_text,
                url_name=url_name, kwargs=kwargs, expected_regex=expected_regex)
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

