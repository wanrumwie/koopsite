import inspect
import os
from unittest.case import skipIf

from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile

from folders.tests.test_base import DummyFolder
from functional_tests.koopsite.ft_base import PageVisitTest
from koopsite.settings import SKIP_TEST



# @skipIf(SKIP_TEST, "пропущено для економії часу")
class ReportDownloadPageVisitTest(PageVisitTest):
    """
    Допоміжний клас для функціональних тестів.
    Описані тут параметри - для перевірки одної сторінки сайту.
    Цей клас буде використовуватися як основа
    для класів тестування цієї сторінки з іншими користувачами.
    """
    this_url    = '/folders/report/1/download/'
    # page_title  = 'Пасічний'
    # page_name   = 'Видалення файла'



@skipIf(SKIP_TEST, "пропущено для економії часу")
class ReportDownloadPageAnonymousVisitorTest(ReportDownloadPageVisitTest):
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
class ReportDownloadPageAuthenticatedVisitorWoPermissionTest(ReportDownloadPageVisitTest):
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
class ReportDownloadPageAuthenticatedVisitorCanDownloadReportTest(ReportDownloadPageVisitTest):
    """
    Тест відвідання сторінки сайту
    користувачем
    Чи всі дані правильно відображені?
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='download_report', model='report')

    # @skipIf(SKIP_TEST, "пропущено для економії часу")
    def test_visitor_can_download_report(self):
        parent = DummyFolder().create_dummy_folder(id=1)
        file = SimpleUploadedFile("file.txt", b"file_content")
        report = DummyFolder().create_dummy_report(parent=parent, id=1, file=file)
        download_directory = "D:\Downloads"
        download_file_full_path = os.path.join(download_directory, report.filename)

        # Користувач перебуває на якійсь сторінці
        current_url = self.browser.current_url

        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Завантаження має початися автоматично

        os.remove(report.file.path)

        if os.path.exists(download_file_full_path):
            print('file was successfully downloaded')
            self.assertTrue(os.path.exists(download_file_full_path))
            os.remove(download_file_full_path)
        else:
            print("file wasn't downloaded")

        # Сторінка має залишитись та сама
        self.check_passed_link(expected_regex=current_url)

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


