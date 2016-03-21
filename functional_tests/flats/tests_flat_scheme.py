import inspect
from unittest.case import skipIf

from django.contrib.auth.models import AnonymousUser

from flats.models import Flat
from flats.tests.test_base import DummyFlat
from functional_tests.koopsite.ft_base import PageVisitTest
from koopsite.settings import SKIP_TEST


class FlatSchemePageVisitTest(PageVisitTest):
    """
    Допоміжний клас для функціональних тестів.
    Описані тут параметри - для перевірки одної сторінки сайту.
    Цей клас буде використовуватися як основа
    для класів тестування цієї сторінки з іншими користувачами.
    """
    this_url    = '/flats/scheme/'
    page_title  = 'Пасічний'
    page_name   = 'Схема будинку'

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
            # {'ls':'#body-navigation'          , 'lt': 'Схема будинку', 'un': 'flats:flat-scheme'},#########
            {'ls':'#body-navigation'          , 'lt': 'Список квартир'   , 'un': 'flats:flat-list'},
            {'ls':'#body-navigation'          , 'lt': 'Параметри квартир'   , 'un': 'flats:flat-table'},
            {'ls':'#body-navigation'          , 'lt': 'Схема користувачів','un': 'flats:flat-scheme-users', 'cd': "user.has_perm('koopsite.view_userprofile')"},
            {'ls':'#body-navigation'          , 'lt': 'Уверх'            , 'un': "index"},
            {'ls':'#header-aside-2-navigation', 'lt': username           , 'un': 'own-profile' , 'cd': "user.is_authenticated()"},
            {'ls':'#header-aside-2-navigation', 'lt': "Кв." + flat_No    , 'un': "flats:flat-detail", 'kw': {'pk': flat_id}, 'cd': "user.is_authenticated() and user.userprofile.flat"},
            {'ls':'#header-aside-2-navigation', 'lt': 'Вийти'            , 'un': 'logout'      , 'cd': "user.is_authenticated()", 'er': '/index/'},
            {'ls':'#header-aside-2-navigation', 'lt': 'Авторизуватися'   , 'un': 'login'       , 'cd': "not user.is_authenticated()"},
            ]
        return s

    def get_data_links_number(self):
        self.data_links_number = len(Flat.objects.all()) # кількість лінків, які приходять в шаблон з даними
        self.data_links_number += 0 # лінк javascript:history.back()
        return self.data_links_number


# @skipIf(SKIP_TEST, "пропущено для економії часу")
class FlatSchemePageAuthenticatedVisitorTest(FlatSchemePageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
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


class FlatSchemePageAuthenticatedVisitorWithPermTest(FlatSchemePageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем з доступом
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='view_userprofile')
        self.get_data_links_number()

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')



@skipIf(SKIP_TEST, "пропущено для економії часу")
class FlatSchemePageAuthenticatedVisitorWithFlatTest(FlatSchemePageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем з номером квартири)
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        # self.create_dummy_folder()
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
class FlatSchemePageAnonymousVisitorTest(FlatSchemePageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = AnonymousUser()
        # self.create_dummy_folder()
        self.get_data_links_number()

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FlatSchemePageGoToFlatTest(FlatSchemePageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    і переходу за лінком, вказаним в таблиці даних
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = AnonymousUser()
        DummyFlat().create_dummy_flat(flat_No='52d')
        self.get_data_links_number()

    def test_visitor_can_go_to_flat(self):
        # Користувач може перейти по лінку потрібні дані
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        flat = Flat.objects.get(flat_No='52d')
        link_parent_selector = '#body-table'
        link_text            = flat.flat_No
        url_name             = 'flats:flat-detail'
        kwargs               = {'pk': flat.id}
        expected_regex       = ""
        self.check_go_to_link(self.this_url, link_parent_selector, link_text,
            url_name=url_name, kwargs=kwargs, expected_regex=expected_regex)
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FlatSchemePageVisitorCanFindFlatTest(FlatSchemePageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    Чи всі дані правильно відображені?
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = AnonymousUser()
        DummyFlat().create_dummy_building()
        self.get_data_links_number()

    def test_visitor_can_find_flat(self):
        # Користувач може  перейти по лінку потрібні дані
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        for flat in Flat.objects.all():
            link_parent_selector = '#body-table'
            link_text            = flat.flat_No
            url_name             = 'flats:flat-detail'
            kwargs               = {'pk': flat.id}
            expected_regex       = ""
            self.check_go_to_link(self.this_url, link_parent_selector, link_text,
                url_name=url_name, kwargs=kwargs, expected_regex=expected_regex)
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    def test_flats_situated_properly(self):
        # Квартири розташовані в таблиці коректно:
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        link_parent_selector = '#body-table'
        floors = set()
        entrances = set()
        for flat in Flat.objects.all():
            floors.add(flat.floor_No)
            entrances.add(flat.entrance_No)
        floors = sorted(floors, reverse=True)
        entrances = sorted(entrances)
        # Поверхи розташовані знизу вверх
        yfact = []
        ydict = {}
        for floor in floors:
            flat = Flat.objects.filter(floor_No=floor)[:1].get()
            link_text      = flat.flat_No
            location, size = self.get_link_location(link_parent_selector,
                                                    link_text)
            yc = location['y'] + size['height']/2
            yfact.append(yc)
            ydict[floor] = yc
        # yfact -  список y координат у порядку ЗМЕНШЕННЯ поверха
        # y має зростати. Перевіряємо:
        self.assertListEqual(yfact, sorted(yfact))

        # Під'їзди розташовані зліва направо
        xfact = []
        xdict = {}
        for entr in entrances:
            flat = Flat.objects.filter(entrance_No=entr)[:1].get()
            link_text      = flat.flat_No
            location, size = self.get_link_location(link_parent_selector,
                                                    link_text)
            xc = location['x'] + size['width']/2
            xfact.append(xc)
            xdict[entr] = xc
        # xfact -  список y координат у порядку ЗБІЛЬШЕННЯ номера під'їзду
        # x має зростати. Перевіряємо:
        self.assertListEqual(xfact, sorted(xfact))

        # Всі квартири на одному поверсі мають однаковий Y
        for flat in Flat.objects.all():
            floor = flat.floor_No
            link_text      = flat.flat_No
            location, size = self.get_link_location(link_parent_selector,
                                                    link_text)
            yc = location['y'] + size['height']/2
            # Порівнюємо з ydict[floor] - попередньо визначені координати поверхів
            self.assertAlmostEqual(yc, ydict[floor])

        # Всі перші на поверсі квартири в одному під'їзді мають однаковий X
        xentr = {}
        for flat in Flat.objects.all():
            entr = flat.entrance_No
            link_text      = flat.flat_No
            location, size = self.get_link_location(link_parent_selector,
                                                    link_text)
            xc = location['x'] + size['width']/2
            if entr in xentr: xentr[entr] = min(xentr[entr], xc)
            else: xentr[entr] = xc

        # Порівнюємо з xdict[entr] - попередньо визначені координати під'їздів
        for entr in entrances:
            self.assertAlmostEqual(xentr[entr], xdict[entr])

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')
