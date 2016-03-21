import inspect
from unittest.case import skipIf

from django.contrib.auth.models import AnonymousUser

from flats.tests.test_base import DummyFlat
from folders.tests.test_base import DummyFolder
from functional_tests.koopsite.ft_base import PageVisitTest
from koopsite.settings import SKIP_TEST


class IndexPageAuthenticatedVisitorTest(PageVisitTest):
    """
    Тест відвідання головної сторінки сайту аутентифікованим користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        # self.browser.implicitly_wait(20)
        self.dummy_user = self.create_dummy_user()
        DummyFolder().create_dummy_catalogue()
        DummyFlat().create_dummy_building()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.data_links_number = 0   # кількість лінків, які приходять в шаблон з даними

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
class IndexPageAuthenticatedVisitorWithFlatTest(PageVisitTest):
    """
    Тест відвідання головної сторінки сайту
    аутентифікованим користувачем з номером квартири)
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        DummyFolder().create_dummy_catalogue()
        DummyFlat().create_dummy_building()
        profile = self.create_dummy_profile(user=self.dummy_user)
        flat = DummyFlat().create_dummy_flat()
        profile.flat=flat
        profile.save()

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class IndexPageAuthenticatedVisitorWithPermissionTest(PageVisitTest):
    """
    Тест відвідання головної сторінки сайту
    аутентифікованим користувачем з доступом типу stuff
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        DummyFolder().create_dummy_catalogue()
        DummyFlat().create_dummy_building()
        self.add_dummy_permission(self.dummy_user,
                                  codename='activate_account')

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class IndexPageAnonymousVisitorTest(PageVisitTest):
    """
    Тест відвідання головної сторінки сайту
    анонімним користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = AnonymousUser()
        DummyFolder().create_dummy_catalogue()
        DummyFlat().create_dummy_building()

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

# TODO-додати перевірку секції справа: Оголошення, Новини, ...
