import inspect
import os
from unittest.case import skipIf

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile

from folders.models import Report
from folders.tests.test_base import DummyFolder
from functional_tests.koopsite.ft_base import PageVisitTest
from koopsite.settings import SKIP_TEST



# @skipIf(SKIP_TEST, "пропущено для економії часу")
class ReportDeletePageVisitTest(PageVisitTest):
    """
    Допоміжний клас для функціональних тестів.
    Описані тут параметри - для перевірки одної сторінки сайту.
    Цей клас буде використовуватися як основа
    для класів тестування цієї сторінки з іншими користувачами.
    """
    this_url    = '/folders/report/1/delete/'
    page_title  = 'Пасічний'
    page_name   = 'Видалення файла'

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


@skipIf(SKIP_TEST, "пропущено для економії часу")
class ReportDeletePageAuthenticatedVisitorWithPermissionTest(ReportDeletePageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='delete_report', model='report')
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
class ReportDeletePageAuthenticatedVisitorAuthorTest(ReportDeletePageVisitTest):
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


@skipIf(SKIP_TEST, "пропущено для економії часу")
class ReportDeletePageAnonymousVisitorTest(ReportDeletePageVisitTest):
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
class ReportDeletePageAuthenticatedVisitorWoPermissionTest(ReportDeletePageVisitTest):
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
class ReportDeletePageAuthenticatedVisitorWoPermissionNotAuthorTest(ReportDeletePageVisitTest):
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
class ReportDeletePageAuthenticatedVisitorCanDeleteReportTest(ReportDeletePageVisitTest):
    """
    Тест відвідання сторінки сайту
    користувачем
    Чи всі дані правильно відображені?
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='delete_report', model='report')
        parent = DummyFolder().create_dummy_folder(id=1)
        file = SimpleUploadedFile("file.txt", b"file_content")
        report = DummyFolder().create_dummy_report(parent=parent, id=1, file=file)
        self.file_full_path = report.file.path

    def tearDown(self):
        try:
            os.remove(self.file_full_path)
        except:
            print('file already deleted')
        super().tearDown()

    # @skipIf(SKIP_TEST, "пропущено для економії часу")
    def test_visitor_can_delete_report(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Бачить у полі очікувану інформацію
        inputbox = self.browser.find_element_by_id('id_name')
        self.assertEqual(inputbox.text, 'file.txt')

        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        # Запису в базі повинно не стати
        with self.assertRaises(ObjectDoesNotExist):
            Report.objects.get(id=1)

        # Файла на диску повинно не стати
        with self.assertRaises(FileNotFoundError):
            os.remove(self.file_full_path)

        # Має бути перехід на потрібну сторінку
        self.check_passed_link(url_name='folders:folder-list-all')

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


