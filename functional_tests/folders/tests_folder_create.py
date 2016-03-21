import inspect
from unittest.case import skipIf

from django.contrib.auth.models import AnonymousUser
from selenium.webdriver.common.keys import Keys

from folders.models import Folder
from folders.tests.test_base import DummyFolder
from functional_tests.koopsite.ft_base import PageVisitTest
from koopsite.settings import SKIP_TEST



# @skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderCreatePageVisitTest(PageVisitTest):
    """
    Допоміжний клас для функціональних тестів.
    Описані тут параметри - для перевірки одної сторінки сайту.
    Цей клас буде використовуватися як основа
    для класів тестування цієї сторінки з іншими користувачами.
    """
    this_url    = '/folders/create/'
    page_title  = 'Пасічний'
    page_name   = 'Створення теки'

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
            # {'ls':'#body-navigation'          , 'lt': 'Картотека (ст.)' , 'un': 'folders:folder-list-all'},
            # {'ls':'#body-navigation'          , 'lt': 'Теки'            , 'un': 'folders:folder-list'},
            # {'ls':'#body-navigation'          , 'lt': 'Кореневі теки'   , 'un': 'folders:folder-parents'},
            # {'ls':'#body-navigation'          , 'lt': 'Файли'           , 'un': 'folders:report-list'},
            # {'ls':'#body-navigation'          , 'lt': 'Нова тека'       , 'un': 'folders:folder-create'},
            # {'ls':'#body-navigation'          , 'lt': 'Новий файл'      , 'un': 'folders:report-upload'},
            # {'ls':'#body-navigation'          , 'lt': 'Картотека (js)'  , 'un': 'folders:folder-contents', 'kw': {'pk': 1}, 'st': 5},
            {'ls':'#body-navigation'          , 'lt': 'Уверх'           , 'un': "folders:folder-list-all"},
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


# @skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderCreatePageAuthenticatedVisitorTest(FolderCreatePageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='add_folder', model='folder')
        self.get_data_links_number()

    def test_can_visit_page(self):
        # Заголовок і назва сторінки правильні
        self.can_visit_page()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    # @skip
    def test_layout_and_styling_page(self):
        # CSS завантажено і працює
        self.layout_and_styling_page()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    # @skip
    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderCreatePageAnonymousVisitorTest(FolderCreatePageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = AnonymousUser()

    def test_can_not_visit_page(self):
        # Заголовок і назва сторінки правильні
        self.can_not_visit_page()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderCreatePageAuthenticatedVisitorWoPermissionTest(FolderCreatePageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем без належного доступу
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)

    def test_can_not_visit_page(self):
        # Заголовок і назва сторінки правильні
        self.can_not_visit_page()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')



# @skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderCreatePageAuthenticatedVisitorCanCreateFolderTest(FolderCreatePageVisitTest):
    """
    Тест відвідання сторінки сайту
    користувачем
    Чи всі дані правильно відображені?
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='add_folder', model='folder')
        DummyFolder().create_dummy_catalogue()


    def test_visitor_can_create_folder(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Бачить у полі очікувану інформацію
        inputbox = self.browser.find_element_by_id('id_parent')

        all_options = inputbox.find_elements_by_tag_name("option")
        for option in all_options:
            if option.is_selected():
                self.assertEqual(option.get_attribute('value'), '')

        # Вводить у полі дані
        inputbox = self.browser.find_element_by_id('id_name')
        inputbox.send_keys('New_folder')

        # Натискає ENTER
        # inputbox.send_keys(Keys.ENTER)
        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        folder = Folder.objects.last()
        self.assertEqual(folder.name, 'New_folder')
        self.assertIsNone(folder.parent)
        # Має бути перехід на потрібну сторінку
        self.check_passed_link(expected_regex=folder.get_absolute_url())

        # Час створення (до секунди) співпадає з поточним?
        # print('folder.created_on =', folder.created_on, now())
        # self.assertAlmostEqual(folder.created_on, now(), delta=timedelta(minutes=1))

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


    def test_visitor_can_create_folder_in_parent(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Вибирає значення
        inputbox = self.browser.find_element_by_id('id_parent')

        all_options = inputbox.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute('value') == "1" :
                option.click()
                parent_name = option.text

        # Вводить у полі дані
        inputbox = self.browser.find_element_by_id('id_name')
        inputbox.send_keys('New_folder')

        # Натискає ENTER
        # inputbox.send_keys(Keys.ENTER)
        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        folder = Folder.objects.last()
        self.assertEqual(folder.name, 'New_folder')
        self.assertEqual(folder.parent.id, 1)
        # Має бути перехід на потрібну сторінку
        self.check_passed_link(expected_regex=folder.get_absolute_url())

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


    def test_visitor_can_create_folder_in_parent_submit_button(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Вибирає значення
        inputbox = self.browser.find_element_by_id('id_parent')

        all_options = inputbox.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute('value') == "1" :
                option.click()
                parent_name = option.text

        # Вводить у полі дані
        inputbox = self.browser.find_element_by_id('id_name')
        inputbox.send_keys('New_folder')

        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        folder = Folder.objects.last()
        self.assertEqual(folder.name, 'New_folder')
        self.assertEqual(folder.parent.id, 1)
        # Має бути перехід на потрібну сторінку
        self.check_passed_link(expected_regex=folder.get_absolute_url())

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


    def test_error_message_if_empty_name(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # НЕ вводить у полі дані
        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        error = self.get_error_elements_for_field('#id_name')[0]
        self.assertTrue(error.is_displayed())
        self.assertEqual(error.text, "Це поле обов'язкове.")

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


    def test_error_message_if_empty_name_is_cleared_on_input(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # НЕ вводить у полі дані
        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        # Виникає помилка
        error = self.get_error_elements_for_field('#id_name')[0]
        self.assertTrue(error.is_displayed())

        # Починає вводити щоб виправити помилку
        inputbox = self.browser.find_element_by_id('id_name')
        inputbox.send_keys('a')

        # Повідомлення про помилку зникає
        error = self.get_error_elements_for_field('#id_name')[0]
        self.assertFalse(error.is_displayed())

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


    def test_error_message_if_fail_date(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Вводить у полі неправильні дані
        inputbox = self.browser.find_element_by_id('id_created_on')
        inputbox.send_keys('qwerty')

        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        error = self.get_error_elements_for_field('#id_created_on')[0]
        self.assertTrue(error.is_displayed())
        self.assertEqual(error.text, "Введіть коректну дату/час.")

        # Починає вводити щоб виправити помилку
        inputbox = self.browser.find_element_by_id('id_created_on')
        inputbox.send_keys('a')

        # Повідомлення про помилку зникає
        error = self.get_error_elements_for_field('#id_created_on')[0]
        self.assertFalse(error.is_displayed())

        # Повідомлення про помилку в іншому полі залишається
        error = self.get_error_elements_for_field('#id_name')[0]
        self.assertTrue(error.is_displayed())

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


    def test_error_message_if_parent_name_not_unique_together(self):
        parent = Folder.objects.get(id=1)
        DummyFolder().create_dummy_folder(parent=parent, name="double_name")

        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Вибирає значення
        inputbox = self.browser.find_element_by_id('id_parent')

        all_options = inputbox.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute('value') == "1" :
                option.click()

        # Вводить у полі дані
        inputbox = self.browser.find_element_by_id('id_name')
        inputbox.send_keys('double_name')

        # Натискає ENTER
        inputbox.send_keys(Keys.ENTER)

        error = self.get_error_element(".errorlist")
        self.assertEqual(error.text, "Тека з таким Материнська тека та Тека вже існує.")

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


    def test_cancel_button_go_to_proper_page(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Вводить у полі неправильні дані
        inputbox = self.browser.find_element_by_id('id_created_on')
        inputbox.send_keys('qwerty')

        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        # Через помилку залишається на тій же сторінці
        header_text = self.browser.find_element_by_id('page-name').text
        self.assertIn(self.page_name, header_text)

        # Натискає кнопку cancel
        button = self.browser.find_element_by_css_selector('form input[type=button]')
        button.click()

        # Має бути перехід на потрібну сторінку
        self.check_passed_link(url_name='folders:folder-list-all')

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


