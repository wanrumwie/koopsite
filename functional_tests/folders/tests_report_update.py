import inspect
import os
from unittest.case import skipIf
from datetime import timedelta

from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import now

from folders.models import Report
from folders.tests.test_base import DummyFolder
from functional_tests.koopsite.ft_base import PageVisitTest
from koopsite.settings import SKIP_TEST



# @skipIf(SKIP_TEST, "пропущено для економії часу")
class ReportUpdatePageVisitTest(PageVisitTest):
    """
    Допоміжний клас для функціональних тестів.
    Описані тут параметри - для перевірки одної сторінки сайту.
    Цей клас буде використовуватися як основа
    для класів тестування цієї сторінки з іншими користувачами.
    """
    this_url    = '/folders/report/1/update/'
    page_title  = 'Пасічний'
    page_name   = 'Редагування даних про файл'

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
            {'ls':'#body-navigation'          , 'lt': 'Уверх'           , 'un': "folders:report-detail", 'kw':{'pk': 1}},
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
class ReportUpdatePageAuthenticatedVisitorWithPermissionTest(ReportUpdatePageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='change_report', model='report')
        self.get_data_links_number()
        parent = DummyFolder().create_dummy_folder(id=1)
        DummyFolder().create_dummy_report(parent=parent, id=1)

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


# @skipIf(SKIP_TEST, "пропущено для економії часу")
class ReportUpdatePageAuthenticatedVisitorAuthorTest(ReportUpdatePageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем без дозволів але який є автором об'єкта
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.get_data_links_number()
        parent = DummyFolder().create_dummy_folder(id=1)
        DummyFolder().create_dummy_report(parent=parent, id=1, user=self.dummy_user)

    def test_can_visit_page(self):
        # Заголовок і назва сторінки правильні
        self.can_visit_page()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


class ReportUpdatePageAuthenticatedVisitorWoPermissionNotAuthorTest(ReportUpdatePageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем без належного доступу і не автором
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        parent = DummyFolder().create_dummy_folder(id=1)
        report = DummyFolder().create_dummy_report(parent=parent, id=1)

    def test_can_not_visit_page(self):
        # Користувач НЕ може відвідати сторінку і буде переадресований
        self.can_not_visit_page()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class ReportUpdatePageAnonymousVisitorTest(ReportUpdatePageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = AnonymousUser()

    def test_can_not_visit_page(self):
        # Користувач НЕ може відвідати сторінку і буде переадресований
        self.can_not_visit_page()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class ReportUpdatePageAuthenticatedVisitorWoPermissionTest(ReportUpdatePageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем без належного доступу
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)

    def test_can_not_visit_page(self):
        # Користувач НЕ може відвідати сторінку і буде переадресований
        self.can_not_visit_page()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')



# @skipIf(SKIP_TEST, "пропущено для економії часу")
class ReportUpdatePageAuthenticatedVisitorCanUpdateReportTest(ReportUpdatePageVisitTest):
    """
    Тест відвідання сторінки сайту
    користувачем
    Чи всі дані правильно відображені?
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='change_report', model='report')
        parent = DummyFolder().create_dummy_folder(id=1)
        file = SimpleUploadedFile("file.txt", b"file_content")
        DummyFolder().create_dummy_report(parent=parent, id=1, file=file)

    def tearDown(self):
        report = Report.objects.get(id=1)
        report.file.delete()
        super().tearDown()

    @skipIf(SKIP_TEST, "пропущено для економії часу")
    def test_visitor_can_update_report_parent(self):
        new_parent = DummyFolder().create_dummy_folder(id=2)
        report = Report.objects.get(id=1)
        expected_parent       = new_parent
        expected_filename     = report.filename
        expected_file         = report.file
        expected_file_content = report.file.read()
        expected_upload_on    = report.uploaded_on
        report.file.close()

        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Бачить у полі очікувану інформацію
        inputbox = self.browser.find_element_by_id('id_parent')
        all_options = inputbox.find_elements_by_tag_name("option")
        for option in all_options:
            if option.is_selected():
                self.assertEqual(option.get_attribute('value'), '1')

        # Вибирає значення
        inputbox = self.browser.find_element_by_id('id_parent')
        self.choose_option_in_select(inputbox, val='2')

        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        # Все збережено вірно?
        report = Report.objects.get(id=1)
        self.assertEqual(report.parent,      expected_parent)
        self.assertEqual(report.filename,    expected_filename)
        self.assertEqual(report.file,        expected_file)
        self.assertEqual(report.file.read(), expected_file_content)
        self.assertEqual(report.uploaded_on, expected_upload_on)
        report.file.close()

        # Має бути перехід на потрібну сторінку
        self.check_passed_link(expected_regex=report.get_absolute_url())

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


    @skipIf(SKIP_TEST, "пропущено для економії часу")
    def test_visitor_can_update_report_filename(self):
        parent = DummyFolder().create_dummy_folder(id=1)
        report = Report.objects.get(id=1)
        expected_parent       = parent
        expected_filename     = "new_file_name"
        expected_file         = report.file
        expected_file_content = report.file.read()
        expected_upload_on    = report.uploaded_on
        report.file.close()

        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Бачить у полі очікувану інформацію
        inputbox = self.browser.find_element_by_id('id_filename')
        self.assertEqual(inputbox.get_attribute('value'), report.filename)

        # Видаляє з поля дані
        inputbox = self.browser.find_element_by_id('id_filename')
        inputbox.clear()

        # Вводить нове значення
        inputbox.send_keys(expected_filename)

        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        # Все збережено вірно?
        report = Report.objects.get(id=1)
        self.assertEqual(report.parent,      expected_parent)
        self.assertEqual(report.filename,    expected_filename)
        self.assertEqual(report.file,        expected_file)
        self.assertEqual(report.file.read(), expected_file_content)
        self.assertEqual(report.uploaded_on, expected_upload_on)

        report.file.close()

        # Має бути перехід на потрібну сторінку
        self.check_passed_link(expected_regex=report.get_absolute_url())

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


    def test_visitor_can_update_report_file(self):
        parent = DummyFolder().create_dummy_folder(id=1)
        report = Report.objects.get(id=1)
        old_full_path = report.file.path

        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Бачить у полі очікувану інформацію
        inputbox = self.browser.find_element_by_id('id_filename')
        self.assertEqual(inputbox.get_attribute('value'), report.filename)

        # Вводить нове значення
        # Для прикладу беремо цей файл:
        cwd = os.getcwd()   # поточний каталог (в ньому є manage.py)
        full_path = os.path.join(cwd, 'example.txt') # повний шлях

        # Натискає кнопку Browse - емулюється шляхом посилання в цей елемент шляху до файла.
        inputbox = self.browser.find_element_by_css_selector('input[type=file]')
        inputbox.send_keys(full_path)

        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        # Все збережено вірно?
        report = Report.objects.get(id=1)
        expected_parent       = parent
        expected_filename     = 'example.txt'
        with open(full_path, 'rb') as f:
            expected_file_content = f.read()

        self.assertEqual(report.parent,      expected_parent)
        self.assertEqual(report.filename,    expected_filename)
        self.assertEqual(report.file.read(), expected_file_content)

        # Час створення (до хвилини) співпадає з поточним?
        self.assertAlmostEqual(report.uploaded_on, now(), delta=timedelta(minutes=1))

        report.file.close()

        # Втидаляємо старий файл, оскільки файлова система
        # записує новий файл під новим іменем:
        os.remove(old_full_path)

        # Має бути перехід на потрібну сторінку
        self.check_passed_link(expected_regex=report.get_absolute_url())

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


    @skipIf(SKIP_TEST, "пропущено для економії часу")
    def test_error_message_if_empty_parent(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Видаляє дані
        inputbox = self.browser.find_element_by_id('id_parent')
        self.choose_option_in_select(inputbox, val='')

        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        error = self.get_error_elements_for_field('#id_parent')[0]
        self.assertTrue(error.is_displayed())
        self.assertEqual(error.text, "Це поле обов'язкове.")

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


    @skipIf(SKIP_TEST, "пропущено для економії часу")
    def test_error_message_if_empty_parent_is_cleared_on_input(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Видаляє дані
        inputbox = self.browser.find_element_by_id('id_parent')
        self.choose_option_in_select(inputbox, val='')

        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        # Виникає помилка
        error = self.get_error_elements_for_field('#id_parent')[0]
        self.assertTrue(error.is_displayed())

        # Вибирає дані, щоб виправити помилку
        inputbox = self.browser.find_element_by_id('id_parent')
        self.choose_option_in_select(inputbox, val='1')

        # Повідомлення про помилку зникає
        error = self.get_error_elements_for_field('#id_parent')[0]
        self.assertFalse(error.is_displayed())

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


    @skipIf(SKIP_TEST, "пропущено для економії часу")
    def test_error_message_if_empty_filename(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Видаляє з поля дані
        inputbox = self.browser.find_element_by_id('id_filename')
        inputbox.clear()

        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        error = self.get_error_elements_for_field('#id_filename')[0]
        self.assertTrue(error.is_displayed())
        self.assertEqual(error.text, "Це поле обов'язкове.")

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


    @skipIf(SKIP_TEST, "пропущено для економії часу")
    def test_error_message_if_empty_filename_is_cleared_on_input(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Видаляє з поля дані
        inputbox = self.browser.find_element_by_id('id_filename')
        inputbox.clear()

        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        # Виникає помилка
        error = self.get_error_elements_for_field('#id_filename')[0]
        self.assertTrue(error.is_displayed())

        # Починає вводити щоб виправити помилку
        inputbox = self.browser.find_element_by_id('id_filename')
        inputbox.send_keys('a')

        # Повідомлення про помилку зникає
        error = self.get_error_elements_for_field('#id_filename')[0]
        self.assertFalse(error.is_displayed())

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


    @skipIf(SKIP_TEST, "пропущено для економії часу")
    def test_cancel_button_go_to_proper_page(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Нічого не вводить

        # Натискає кнопку cancel
        button = self.browser.find_element_by_css_selector('form input[type=button]')
        button.click()

        # Має бути перехід на потрібну сторінку
        self.check_passed_link(url_name='folders:report-detail', kwargs={'pk': '1'})

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


