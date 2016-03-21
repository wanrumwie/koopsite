import inspect
from unittest.case import skipIf

from django.contrib.auth.models import AnonymousUser, User

from flats.tests.test_base import DummyFlat
from functional_tests.koopsite.ft_base import PageVisitTest
from koopsite.settings import SKIP_TEST



# @skipIf(SKIP_TEST, "пропущено для економії часу")
from koopsite.tests.test_base import DummyUser


class LoginPageVisitTest(PageVisitTest):
    """
    Допоміжний клас для функціональних тестів.
    Описані тут параметри - для перевірки одної сторінки сайту.
    Цей клас буде використовуватися як основа
    для класів тестування цієї сторінки з іншими користувачами.
    """
    this_url    = '/login/'
    page_title  = 'Пасічний'
    page_name   = 'Авторизація'

    def links_in_template(self, user):
        # Повертає список словників, які поступають як параметри до функції self.check_go_to_link(...)
        #     def check_go_to_link(self, this_url, link_parent_selector, link_text,
        #                           expected_regex=None, url_name=None, kwargs=None):
        # Ключі словників скорочені до 2-х літер: ls lt er un kw
        # плюс cd - condition для перевірки видимості лінка (буде аргументом ф-ції eval() ).
        # Спочатку визначаються деякі параметри:
        username, flat_id, flat_No = self.get_user_name_flat(user)
        s = [
            {'ls':'#body-navigation'          , 'lt': 'Головна сторінка', 'un': 'index'},
            {'ls':'#body-navigation'          , 'lt': 'Уверх'           , 'un': "index"},
            {'ls':'#header-aside-2-navigation', 'lt': username          , 'un': 'own-profile' , 'cd': "user.is_authenticated()"},
            {'ls':'#header-aside-2-navigation', 'lt': "Кв." + flat_No   , 'un': "flats:flat-detail", 'kw': {'pk': flat_id}, 'cd': "user.is_authenticated() and user.userprofile.flat"},
            {'ls':'#header-aside-2-navigation', 'lt': 'Вийти'           , 'un': 'logout'      , 'cd': "user.is_authenticated()", 'er': '/index/'},
            {'ls':'#header-aside-2-navigation', 'lt': 'Авторизуватися'  , 'un': 'login'       , 'cd': "not user.is_authenticated()"},
            ]
        return s

    def get_data_links_number(self):
        self.data_links_number = 0 # кількість лінків, які приходять в шаблон з даними
        self.data_links_number += 0 # Кнопки
        return self.data_links_number

    def enter_and_check_data(self):
        # Вводить у полях дані і завершує форму натисканням Готово
        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys('fred')

        inputbox = self.browser.find_element_by_id('id_password')
        inputbox.send_keys('secret')

        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        user = User.objects.get(username='fred')

        # Чи в сесію записано правильний id клієнта?
        # self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        # Чи оновилася дата last_login?
        # self.assertAlmostEqual(user.last_login, now(), delta=timedelta(minutes=1))

        return user


@skipIf(SKIP_TEST, "пропущено для економії часу")
class LoginPageAuthenticatedVisitorTest(LoginPageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.get_data_links_number()

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class LoginPageAnonymousVisitorTest(LoginPageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = AnonymousUser()

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
class LoginPageAnonymousVisitorCanLoginTest(LoginPageVisitTest):
    """
    Тест відвідання сторінки сайту
    користувачем
    Чи всі дані правильно відображені?
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.fred = DummyUser().create_dummy_user(username='fred', password='secret')
        self.dummy_user = AnonymousUser()
        DummyFlat().create_dummy_flat(id=1, flat_No='55')

    def test_anon_visitor_can_login(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Вводить дані і натискає кнопку Готово
        self.enter_and_check_data()

        # Опиняється на потрібній сторінці
        self.check_passed_link(url_name='index')

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    def test_error_message_if_empty_required_fields(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # НЕ вводить у полі дані
        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        for field_css in ['#id_username', '#id_password']:
            error = self.get_error_elements_for_field(field_css)[0]
            self.assertTrue(error.is_displayed())
            self.assertEqual(error.text, "Це поле обов'язкове.")

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


    # @skip
    def test_error_message_if_empty_required_fields_is_cleared_on_input(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # НЕ вводить у полі дані
        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        for field_css in ['#id_username', '#id_password']:
            # Виникає помилка
            error = self.get_error_elements_for_field(field_css)[0]
            self.assertTrue(error.is_displayed())

            # Починає вводити щоб виправити помилку
            inputbox = self.browser.find_element_by_id(field_css.lstrip('#'))
            inputbox.send_keys('a')

            # Повідомлення про помилку зникає
            error = self.get_error_elements_for_field(field_css)[0]
            self.assertFalse(error.is_displayed())

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    def test_error_message_if_not_active_account(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        self.fred.is_active = False
        self.fred.save()

        # Вводить дані і натискає кнопку Готово
        self.enter_and_check_data()

        field_id = "id_username"
        field_css = '#%s' % field_id

        error = self.get_error_element(".errorlist")
        self.assertTrue(error.is_displayed())
        self.assertEqual(error.text, "Цей запис користувача не активний.")

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


    def test_error_message_if_bad_username_and_or_password(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Вводить у полі неправильні дані
        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys('john')

        inputbox = self.browser.find_element_by_id('id_password')
        inputbox.send_keys('john')

        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        error = self.get_error_element(".errorlist")
        self.assertTrue(error.is_displayed())
        self.assertEqual(error.text, "Будь ласка, введіть правильні ім'я користувача та пароль. Зауважте, що обидва поля чутливі до регістру.")

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')



# @skipIf(SKIP_TEST, "пропущено для економії часу")
class LoginPageAuthenticatedVisitorCanLoginTest(LoginPageVisitTest):
    """
    Тест відвідання сторінки сайту
    користувачем
    Чи всі дані правильно відображені?
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.fred = DummyUser().create_dummy_user(username='fred', password='secret')
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)

    def test_anon_visitor_can_login(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Вводить дані і натискає кнопку Готово
        self.enter_and_check_data()

        # Опиняється на потрібній сторінці
        self.check_passed_link(url_name='index')

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    def test_cancel_button_go_to_proper_page(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Натискає кнопку cancel
        button = self.browser.find_element_by_css_selector('form input[type=button]')
        button.click()

        # Має бути перехід на потрібну сторінку
        self.check_passed_link(url_name='index')

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


