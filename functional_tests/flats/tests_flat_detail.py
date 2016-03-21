import inspect
from unittest.case import skipIf

from django.contrib.auth.models import AnonymousUser

from flats.models import Flat
from flats.tests.test_base import DummyFlat
from flats.views import FlatDetail
from functional_tests.koopsite.ft_base import PageVisitTest
from koopsite.settings import SKIP_TEST



# @skipIf(SKIP_TEST, "пропущено для економії часу")
class FlatDetailPageVisitTest(PageVisitTest):
    """
    Допоміжний клас для функціональних тестів.
    Описані тут параметри - для перевірки одної сторінки сайту.
    Цей клас буде використовуватися як основа
    для класів тестування цієї сторінки з іншими користувачами.
    """
    this_url    = '/flats/1/'
    page_title  = 'Пасічний'
    page_name   = 'Характеристика квартири № 1'

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
            {'ls':'#body-navigation'          , 'lt': 'Схема будинку', 'un': 'flats:flat-scheme'},
            {'ls':'#body-navigation'          , 'lt': 'Список квартир'   , 'un': 'flats:flat-list'},
            {'ls':'#body-navigation'          , 'lt': 'Параметри квартир'   , 'un': 'flats:flat-table'},
            {'ls':'#body-navigation'          , 'lt': 'Схема користувачів','un': 'flats:flat-scheme-users', 'cd': "user.has_perm('koopsite.view_userprofile')"},
            {'ls':'#body-navigation'          , 'lt': 'Уверх'            , 'un': "flats:flat-scheme"},
            {'ls':'#header-aside-2-navigation', 'lt': username           , 'un': 'own-profile' , 'cd': "user.is_authenticated()"},
            {'ls':'#header-aside-2-navigation', 'lt': "Кв." + flat_No    , 'un': "flats:flat-detail", 'kw': {'pk': flat_id}, 'cd': "user.is_authenticated() and user.userprofile.flat"},
            {'ls':'#header-aside-2-navigation', 'lt': 'Вийти'            , 'un': 'logout'      , 'cd': "user.is_authenticated()", 'er': '/index/'},
            {'ls':'#header-aside-2-navigation', 'lt': 'Авторизуватися'   , 'un': 'login'       , 'cd': "not user.is_authenticated()"},
            ]
        return s

    def get_data_links_number(self):
        page_links_number = self.get_num_page_links(22, FlatDetail.paginate_by)[1]
        self.data_links_number = page_links_number # кількість лінків, які приходять в шаблон з даними
        self.data_links_number += 1 # лінк "В один рядок"
        self.data_links_number += 0 # лінк javascript:history.back()
        return self.data_links_number

@skipIf(SKIP_TEST, "пропущено для економії часу")
class FlatDetailPageAuthenticatedVisitorTest(FlatDetailPageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        DummyFlat().create_dummy_flat(flat_No='1')
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
class FlatDetailPageAuthenticatedVisitorWithFlatTest(FlatDetailPageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем з номером квартири)
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        DummyFlat().create_dummy_flat(flat_No='1')
        self.add_user_cookie_to_browser(self.dummy_user)
        profile = self.create_dummy_profile(user=self.dummy_user)
        flat = DummyFlat().create_dummy_flat()
        profile.flat=flat
        profile.save()
        self.get_data_links_number()

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


# @skipIf(SKIP_TEST, "пропущено для економії часу")
class FlatDetailPageAuthenticatedVisitorWithPermTest(FlatDetailPageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем з доступом
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        DummyFlat().create_dummy_flat(flat_No='1')
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='view_userprofile')
        self.get_data_links_number()

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FlatDetailPageAnonymousVisitorTest(FlatDetailPageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = AnonymousUser()
        DummyFlat().create_dummy_flat(flat_No='1')
        self.get_data_links_number()

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FlatDetailPageDataTest(FlatDetailPageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    і переходу за лінком, вказаним в таблиці даних
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = AnonymousUser()
        DummyFlat().create_dummy_flat(flat_No='1')
        self.get_data_links_number()

    def test_data_links(self):
        # Користувач може перейти по лінку на горизонтальну таблицю
        # Таблиця має дві колонки і потрібну кількість рядків
        # Під таблицею є лінки пейджінатора
        # Користувач може гортати сторінки
        # TODO-перевірити пейджінатор окремо, на списку з більшою к-стю сторінок
        # TODO-чи перевіряти як виглядає таблиця і які містить дані?

        self.browser.get('%s%s' % (self.server_url, self.this_url))
        flat = Flat.objects.get(flat_No='1')
        link_parent_selector = '#paginator'
        # Знайти href за "стрілочкою" не вдається.
        # Тому шукаю за самим атрибутом href
        # link_text            = html.entities.html5["larr;"]
        # link_text            = u"\u2190"
        link_text            = ""
        url_name             = 'flats:flat-detail'
        kwargs               = {'pk': flat.id}
        expected_regex       = "/?page=2"
        self.check_go_to_link(self.this_url, link_parent_selector, link_text,
            kwargs=kwargs, expected_regex=expected_regex,
            href_itself="?page=2")

        link_parent_selector = '#under-paginator'
        link_text            = "В один рядок"
        url_name             = 'flats:flat-detail-h'
        expected_regex       = ""
        self.check_go_to_link(self.this_url, link_parent_selector, link_text,
            kwargs=kwargs, url_name=url_name, expected_regex=expected_regex)
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

