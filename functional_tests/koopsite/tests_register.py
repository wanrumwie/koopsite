import inspect
import os
from unittest.case import skipIf

from django.contrib.auth.models import AnonymousUser, User
from selenium.webdriver.common.action_chains import ActionChains

from flats.tests.test_base import DummyFlat
from functional_tests.koopsite.ft_base import PageVisitTest, create_dummy_miniature_file
from koopsite.forms import Human_Check
from koopsite.models import UserProfile
from koopsite.settings import SKIP_TEST
from koopsite.tests.test_base import DummyUser


class RegisterPageVisitTest(PageVisitTest):
    """
    Допоміжний клас для функціональних тестів.
    Описані тут параметри - для перевірки одної сторінки сайту.
    Цей клас буде використовуватися як основа
    для класів тестування цієї сторінки з іншими користувачами.
    """
    this_url    = '/register/'
    page_title  = 'Пасічний'
    page_name   = 'Реєстрація нового користувача'

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

    def enter_and_check_new_user_minimum_data(self):
        # Вводить у полях дані і завершує форму натисканням Готово
        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys('fred')

        inputbox = self.browser.find_element_by_id('id_password1')
        inputbox.send_keys('secret')

        inputbox = self.browser.find_element_by_id('id_password2')
        inputbox.send_keys('secret')

        inputbox = self.browser.find_element_by_id('id_human_check')
        inputbox.send_keys('abrakadabra')

        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        user = User.objects.last()
        self.assertEqual(user.username, 'fred')
        self.assertEqual(user.is_active, False)
        self.assertNotEqual(user.password, None)
        self.assertNotEqual(user.password, 'secret')

        profile = UserProfile.objects.last()
        self.assertEqual(profile.user, user)

        return user

    def enter_and_check_new_user_all_data(self):
        # Вводить у полях дані і завершує форму натисканням Готово
        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys('fred')

        inputbox = self.browser.find_element_by_id('id_first_name')
        inputbox.send_keys('Freddy')

        inputbox = self.browser.find_element_by_id('id_last_name')
        inputbox.send_keys('Mercury')

        inputbox = self.browser.find_element_by_id('id_email')
        inputbox.send_keys('fred@gmail.com')

        inputbox = self.browser.find_element_by_id('id_password1')
        inputbox.send_keys('secret')

        inputbox = self.browser.find_element_by_id('id_password2')
        inputbox.send_keys('secret')

        # Вибирає значення
        inputbox = self.browser.find_element_by_id('id_flat')
        all_options = inputbox.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute('value') == "1" :
                option.click()

        # Для прикладу беремо цей файл, з якого створимо мініатюру:
        full_path, \
        mini_path, \
        uploaded_big_file, \
        expected_mini_content \
            = create_dummy_miniature_file('example.jpg')

        # Натискає кнопку Browse - емулюється шляхом посилання в цей елемент шляху до файла.
        inputbox = self.browser.find_element_by_css_selector('input[type=file]')
        inputbox.send_keys(full_path)

        inputbox = self.browser.find_element_by_id('id_human_check')
        inputbox.send_keys('abrakadabra')

        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        user = User.objects.last()
        self.assertEqual(user.username, 'fred')
        self.assertEqual(user.first_name, 'Freddy')
        self.assertEqual(user.last_name, 'Mercury')
        self.assertEqual(user.email, 'fred@gmail.com')
        self.assertEqual(user.is_active, False)
        self.assertNotEqual(user.password, None)
        self.assertNotEqual(user.password, 'secret')

        profile = UserProfile.objects.last()
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.flat.id, 1)

        # Завантажено той файл?
        saved_path = profile.picture.path
        with open(saved_path, 'rb') as saved_f:
            file_content = saved_f.read()
        with open(mini_path, 'rb') as f:
            expected_file_content = f.read()
        self.assertEqual(file_content, expected_file_content)

        return user

    def check_finish_sub_page_for_Anonymous_visitor(self, new_user):
        # Залишається на тій же сторінці з оновленим текстом
        self.check_passed_link(url_name='register')
        div = self.browser.find_element_by_css_selector('.welcome_text')
        text = div.text
        self.assertEqual(text, "Вітаємо, %s!" % new_user.username)
        div = self.browser.find_element_by_css_selector('.message_text')
        text = div.text
        self.assertIn("Дякуємо, що зареєструвались на сайті!", text)

    def check_finish_sub_page_for_Authenticated_visitor(self, new_user):
        # Залишається на тій же сторінці з оновленим текстом
        self.check_passed_link(url_name='register')
        div = self.browser.find_element_by_css_selector('.welcome_text')
        text = div.text
        self.assertEqual(text, "Вітаємо, %s!" % self.dummy_user.username)
        div = self.browser.find_element_by_css_selector('.message_text')
        text = div.text
        self.assertIn("Ви зареєстрували нового користувача: %s" % new_user.username, text)


@skipIf(SKIP_TEST, "пропущено для економії часу")
class RegisterPageAuthenticatedVisitorTest(RegisterPageVisitTest):
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
class RegisterPageAnonymousVisitorTest(RegisterPageVisitTest):
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



@skipIf(SKIP_TEST, "пропущено для економії часу")
class RegisterPageAnonymousVisitorCanCreateNewAccountTest(RegisterPageVisitTest):
    """
    Тест відвідання сторінки сайту
    користувачем
    Чи всі дані правильно відображені?
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        Human_Check.if_view_test = True
        self.dummy_user = AnonymousUser()
        DummyFlat().create_dummy_flat(id=1, flat_No='55')

    def tearDown(self):
        Human_Check.if_view_test = False
        super().tearDown()

    def test_anon_visitor_can_create_account_with_minimum_needed_fields(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Вводить дані і натискає кнопку Готово
        new_user = self.enter_and_check_new_user_minimum_data()

        # Опиняється на фінішній суб-сторінці з оновленим текстом
        self.check_finish_sub_page_for_Anonymous_visitor(new_user)

        # Шукає лінк і переходить по ньому на головну сторінку
        link_text = "повернутися на головну сторінку"
        href = self.browser.find_element_by_partial_link_text(link_text)

        actions = ActionChains(self.browser)
        actions.move_to_element(href)
        actions.click(href)
        actions.perform()
        self.check_passed_link(url_name='index')

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    def test_error_message_if_empty_required_fields(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # НЕ вводить у полі дані
        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        for field_css in ['#id_username', '#id_password1', '#id_password2']:
            error = self.get_error_elements_for_field(field_css)[0]
            self.assertTrue(error.is_displayed())
            self.assertEqual(error.text, "Це поле обов'язкове.")

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    def test_error_message_if_empty_required_fields_is_cleared_on_input(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # НЕ вводить у полі дані
        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        for field_css in ['#id_username', '#id_password1', '#id_password2']:
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

    def test_error_message_if_fail_human_check(self):
        Human_Check.if_view_test = False
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        field_id = "id_human_check"
        field_css = '#%s' % field_id
        # Вводить у полі неправильні дані
        inputbox = self.browser.find_element_by_id(field_id)
        inputbox.send_keys('abrakadabra')

        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        error = self.get_error_elements_for_field(field_css)[0]
        self.assertTrue(error.is_displayed())
        self.assertEqual(error.text, "Помилка!")

        # Починає вводити щоб виправити помилку
        inputbox = self.browser.find_element_by_id(field_id)
        inputbox.send_keys('a')

        # Повідомлення про помилку зникає
        error = self.get_error_elements_for_field(field_css)[0]
        self.assertFalse(error.is_displayed())

        # Повідомлення про помилку в іншому полі залишається
        error = self.get_error_elements_for_field('#id_username')[0]
        self.assertTrue(error.is_displayed())

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    def test_error_message_if_not_unique_username(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        DummyUser().create_dummy_user('john')
        field_id = "id_username"
        field_css = '#%s' % field_id
        # Вводить у полі неправильні дані
        inputbox = self.browser.find_element_by_id(field_id)
        inputbox.send_keys('john')

        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        error = self.get_error_elements_for_field(field_css)[0]
        self.assertTrue(error.is_displayed())
        self.assertEqual(error.text, "Користувач з таким ім'ям вже існує.")

        # Починає вводити щоб виправити помилку
        inputbox = self.browser.find_element_by_id(field_id)
        inputbox.send_keys('a')

        # Повідомлення про помилку зникає
        error = self.get_error_elements_for_field(field_css)[0]
        self.assertFalse(error.is_displayed())

        # Повідомлення про помилку в іншому полі залишається
        error = self.get_error_elements_for_field('#id_password1')[0]
        self.assertTrue(error.is_displayed())

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


# @skipIf(SKIP_TEST, "пропущено для економії часу")
class RegisterPageAuthenticatedVisitorCanCreateNewAccountTest(RegisterPageVisitTest):
    """
    Тест відвідання сторінки сайту
    користувачем
    Чи всі дані правильно відображені?
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        Human_Check.if_view_test = True
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        DummyFlat().create_dummy_flat(id=1, flat_No='55')

    def tearDown(self):
        Human_Check.if_view_test = False
        try:
            profile = UserProfile.objects.last()
            profile.picture.delete()
        except:
            pass
        super().tearDown()

    def test_auth_visitor_can_create_account_with_minimum_needed_fields(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Вводить дані і натискає кнопку Готово
        new_user = self.enter_and_check_new_user_minimum_data()

        # Опиняється на фінішній суб-сторінці з оновленим текстом
        self.check_finish_sub_page_for_Authenticated_visitor(new_user)

        # Шукає ОДИН з ДВОХ лінків і переходить по ньому на головну сторінку
        link_text = "продовжити роботу"
        href = self.browser.find_element_by_partial_link_text(link_text)

        actions = ActionChains(self.browser)
        actions.move_to_element(href)
        actions.click(href)
        actions.perform()
        self.check_passed_link(url_name='index')

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    def test_auth_visitor_can_create_account_with_all_needed_fields(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Вводить дані і натискає кнопку Готово
        new_user = self.enter_and_check_new_user_all_data()

        # Опиняється на фінішній суб-сторінці з оновленим текстом
        self.check_finish_sub_page_for_Authenticated_visitor(new_user)

        # Шукає ОДИН з ДВОХ лінків і переходить по ньому на головну сторінку
        link_text = "вийти з облікового запису"
        href = self.browser.find_element_by_partial_link_text(link_text)

        actions = ActionChains(self.browser)
        actions.move_to_element(href)
        actions.click(href)
        actions.perform()
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


@skipIf(SKIP_TEST, "пропущено для економії часу")
class LogoutUrlTest(RegisterPageVisitTest):
    """
    Тест відвідання сторінки сайту
    користувачем
    Чи всі дані правильно відображені?
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.this_url = '/logout/'

    def test_auth_visitor_can_logout(self):
        self.dummy_user = AnonymousUser()
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        self.check_passed_link(url_name='noaccess')

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    def test_anon_visitor_can_not_logout(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        self.check_passed_link(url_name='index')

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

