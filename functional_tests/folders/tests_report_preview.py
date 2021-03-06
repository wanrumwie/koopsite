import inspect
import os
from unittest.case import skipIf

from django.contrib.auth.models import AnonymousUser

from folders.tests.test_base import DummyFolder
from functional_tests.koopsite.ft_base import PageVisitTest
from koopsite.fileExtIconPath import get_viewable_extension_list
from koopsite.settings import SKIP_TEST, WAIT_VISUAL_TEST



# @skipIf(SKIP_TEST, "пропущено для економії часу")
class ReportPreviewPageVisitTest(PageVisitTest):
    """
    Допоміжний клас для функціональних тестів.
    Описані тут параметри - для перевірки одної сторінки сайту.
    Цей клас буде використовуватися як основа
    для класів тестування цієї сторінки з іншими користувачами.
    """
    this_url    = '/folders/report/1/preview/'
    page_title  = 'Пасічний'
    page_name   = 'Попередній перегляд файла: example.jpg'

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
            # {'ls':'#body-navigation'          , 'lt': 'Нова тека в цій' , 'un': 'folders:folder-create-in', 'kw': {'parent': 1}},
            # {'ls':'#body-navigation'          , 'lt': 'Редагувати деталі теки', 'un': 'folders:folder-update', 'kw': {'pk': 1}},
            # {'ls':'#body-navigation'          , 'lt': "Завантажити теку", 'un': 'folders:folder-download', 'kw': {'pk': 1}},
            # {'ls':'#body-navigation'          , 'lt': "Видалити теку", 'un': 'folders:folder-delete', 'kw': {'pk': 1}},
            # {'ls':'#body-navigation'          , 'lt': 'Новий файл в цю теку', 'un': 'folders:report-upload-in', 'kw': {'parent': 1}},
            # {'ls':'#body-navigation'          , 'lt': 'Файли'           , 'un': 'folders:report-list'},
            # {'ls':'#body-navigation'          , 'lt': 'Попередній перегляд', 'un': 'folders:report-preview', 'kw': {'pk': 1}},
            {'ls':'#body-navigation'          , 'lt': 'Деталі файла'    , 'un': 'folders:report-detail', 'kw': {'pk': 1}},
            {'ls':'#body-navigation'          , 'lt': 'Редагувати деталі файла', 'un': 'folders:report-update', 'kw': {'pk': 1}},
            {'ls':'#body-navigation'          , 'lt': 'Завантажити файл', 'un': 'folders:report-download', 'kw': {'pk': 1}},
            {'ls':'#body-navigation'          , 'lt': 'Видалити файл'   , 'un': 'folders:report-delete', 'kw': {'pk': 1}},
            # {'ls':'#body-navigation'          , 'lt': 'Нова тека'       , 'un': 'folders:folder-create'},
            # {'ls':'#body-navigation'          , 'lt': 'Новий файл'      , 'un': 'folders:report-upload'},
            # {'ls':'#body-navigation'          , 'lt': 'Картотека (js)'  , 'un': 'folders:folder-contents', 'kw': {'pk': 1}, 'st': 5},
            {'ls':'#body-navigation'          , 'lt': 'Уверх'           , 'un': 'folders:folder-list-all'},
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
class ReportPreviewPageAuthenticatedVisitorTest(ReportPreviewPageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='view_report', model='report')
        self.get_data_links_number()
        parent = DummyFolder().create_dummy_folder()
        # Для прикладу беремо цей файл:
        full_path = os.path.join(os.getcwd(), 'example.jpg') # повний шлях
        self.report = DummyFolder().create_dummy_report(parent=parent,
                                                   id=1, path=full_path)

    def tearDown(self):
        self.report.file.delete()
        super().tearDown()

    def test_can_visit_page(self):
        # Заголовок і назва сторінки правильні
        self.can_visit_page()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    def test_layout_and_styling_page(self):
        # CSS завантажено і працює
        self.layout_and_styling_page(delta=20) # враховуємо смужку скролінгу, через яку зображення зсувається з центру
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class ReportPreviewPageAnonymousVisitorTest(ReportPreviewPageVisitTest):
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
class ReportPreviewPageAuthenticatedVisitorWoPermissionTest(ReportPreviewPageVisitTest):
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


@skipIf(SKIP_TEST, "пропущено для економії часу")
class ReportPreviewPageAuthenticatedVisitorNotViewableFileTest(ReportPreviewPageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='view_report', model='report')
        self.get_data_links_number()
        parent = DummyFolder().create_dummy_folder()
        # Для прикладу беремо цей файл:
        full_path = os.path.join(os.getcwd(), 'example.docx') # повний шлях
        self.report = DummyFolder().create_dummy_report(parent=parent,
                                                   id=1, path=full_path)

    def tearDown(self):
        self.report.file.delete()
        super().tearDown()

    def test_can_visit_page_with_no_viewable_message(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Бачить у полі очікувану інформацію
        inputbox = self.browser.find_element_by_id('preview-box')
        self.assertEqual(inputbox.text, "На даний час неможливо переглянути файл цього типу")
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


class ReportPreviewPageAuthenticatedVisitorTestVisual(ReportPreviewPageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='view_report', model='report')
        self.get_data_links_number()
        self.parent = DummyFolder().create_dummy_folder()

    def tearDown(self):
        if WAIT_VISUAL_TEST:
            input(' press Enter key')
        self.report.file.delete()
        super().tearDown()

    def visit_page(self, file_name, expected_text=""):
        fileExt = os.path.splitext(file_name)[1]
        # Чи розширення цього файла входить до списку "previewable"?
        if expected_text:
            self.assertNotIn(fileExt, get_viewable_extension_list())
        else:
            self.assertIn(fileExt, get_viewable_extension_list())

        # Створюємо запис з цим файлом:
        full_path = os.path.join(os.getcwd(), file_name) # повний шлях
        self.report = DummyFolder().create_dummy_report(parent=self.parent,
                                                   id=1, path=full_path)
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Бачить у полі очікувану інформацію
        div_box = self.browser.find_element_by_id('preview-box')
        self.assertEqual(div_box.text, expected_text)

    def test_jpg(self):
        self.visit_page('example.jpg')
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    def test_pdf(self):
        self.visit_page('example.pdf')
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    def test_txt(self):
        # self.visit_page('example.txt', "На даний час неможливо переглянути файл цього типу")
        self.visit_page('example.txt')
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

