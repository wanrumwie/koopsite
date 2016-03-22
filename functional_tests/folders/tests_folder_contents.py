from datetime import timedelta
import inspect
from unittest.case import skipIf, skip
from django.contrib.auth.models import AnonymousUser
from django.utils.timezone import now
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from folders.functions import get_full_named_path, get_parents
from folders.models import Folder, Report
from folders.tests.test_base import DummyFolder
from folders.views import FolderReportList
from functional_tests.koopsite.ft_base import PageVisitTest
from koopsite.settings import SKIP_TEST


# @skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderContentsPageVisitTest(PageVisitTest):
    """
    Допоміжний клас для функціональних тестів.
    Описані тут параметри - для перевірки одної сторінки сайту.
    Цей клас буде використовуватися як основа
    для класів тестування цієї сторінки з іншими користувачами.
    """
    this_url    = '/folders/1/contents/'
    page_title  = 'Пасічний'
    page_name   = 'КАРТОТЕКА ФАЙЛІВ'

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
            {'ls':'#body-navigation'          , 'lt': 'Картотека (ст.)' , 'un': 'folders:folder-list-all'},
            # {'ls':'#body-navigation'          , 'lt': 'Теки'            , 'un': 'folders:folder-list'},
            # {'ls':'#body-navigation'          , 'lt': 'Кореневі теки'   , 'un': 'folders:folder-parents'},
            # {'ls':'#body-navigation'          , 'lt': 'Файли'           , 'un': 'folders:report-list'},
            # {'ls':'#body-navigation'          , 'lt': 'Нова тека'       , 'un': 'folders:folder-create'},
            # {'ls':'#body-navigation'          , 'lt': 'Новий файл'      , 'un': 'folders:report-upload'},
            # {'ls':'#body-navigation'          , 'lt': 'Картотека (js)'  , 'un': 'folders:folder-contents', 'kw': {'pk': 1}, 'st': 5},
            {'ls':'#body-navigation'          , 'lt': 'Уверх'           , 'un': "index"},
            {'ls':'#header-aside-2-navigation', 'lt': username          , 'un': 'own-profile' , 'cd': "user.is_authenticated()"},
            {'ls':'#header-aside-2-navigation', 'lt': "Кв." + flat_No   , 'un': "flats:flat-detail", 'kw': {'pk': flat_id}, 'cd': "user.is_authenticated() and user.userprofile.flat"},
            {'ls':'#header-aside-2-navigation', 'lt': 'Вийти'           , 'un': 'logout'      , 'cd': "user.is_authenticated()", 'er': '/index/'},
            {'ls':'#header-aside-2-navigation', 'lt': 'Авторизуватися'  , 'un': 'login'       , 'cd': "not user.is_authenticated()"},
            ]
        return s

    def popup_activation_buttons_in_template(self):
        # Повертає список словників, які поступають як параметри до функції
        # self.check_button_click_popup_appearance(...)
        # def check_button_click_popup_appearance(self, this_url, button_parent_selector,
        #             button_text, dialog_selector=None, dialog_title=None,
        #             okey_text=None, cancel_text=None, close_on_esc=None):
        # Ключі словників скорочені до 2-х літер: bs bt ds dt ot kt ce
        # плюс cd - condition для перевірки видимості кнопки (буде аргументом ф-ції eval() ).
        s = [
            {'bs':'#body-aside-1-buttons', 'bt': 'Нова тека'    , 'ds': '.ui-dialog', 'dt': 'Нова тека'             , 'ot': 'Ok', 'ct': 'Cancel', 'ce': True, },
            {'bs':'#body-aside-1-buttons', 'bt': 'Новий файл'   , 'ds': '.ui-dialog', 'dt': 'Новий файл'            , 'ot': 'Ok', 'ct': 'Cancel', 'ce': True, },
            {'bs':'#body-aside-1-buttons', 'bt': 'Завантажити'  , 'ds': '.ui-dialog', 'dt': 'Завантаження '         , 'ot': 'Ok', 'ct': 'Cancel', 'ce': True, },
            {'bs':'#body-aside-1-buttons', 'bt': 'Перейменувати', 'ds': '.ui-dialog', 'dt': 'Перейменування '       , 'ot': 'Ok', 'ct': 'Cancel', 'ce': True, },
            {'bs':'#body-aside-1-buttons', 'bt': 'Перемістити'  , 'ds': '.ui-dialog', 'dt': 'Перемістити виділену ' , 'ot': 'Ok', 'ct': 'Cancel', 'ce': True, },
            {'bs':'#body-aside-1-buttons', 'bt': 'Видалити'     , 'ds': '.ui-dialog', 'dt': 'Видалення '            , 'ot': 'Ok', 'ct': 'Cancel', 'ce': True, },
            ]
        return s

    def get_data_length(self):
        this_folder_id = 1
        this_folder = Folder.objects.get(id=this_folder_id)
        self.data_length = len(Folder.objects.filter(parent=this_folder)) \
                         + len(Report.objects.filter(parent=this_folder)) \
                         + len(get_parents(this_folder)) \
                         + 1 # довжина списку з даними
        return self.data_length

    def get_data_links_number(self):
        self.data_links_number = self.get_data_length() # кількість лінків, які приходять в шаблон з даними
        self.data_links_number += self.get_num_page_links(self.get_data_length(), FolderReportList.paginate_by)[1]
        return self.data_links_number


# @skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderContentsPageAuthenticatedVisitorTest(FolderContentsPageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='add_folder', model='folder')
        DummyFolder().create_dummy_catalogue(report=True)
        self.get_data_links_number()

    # @skip
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

    # @skip
    def test_visitor_can_click_popup_activation_buttons(self):
        # Користувач може клацнути по всіх кнопках на сторінці і повернутися назад
        self.visitor_can_click_popup_activation_buttons()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    # @skip
    def test_visitor_can_create_folder(self):
        # Параметри потрібної кнопки:
        button_text = "Нова тека"
        buttons = self.popup_activation_buttons_in_template()
        for d in buttons:
            if d.get('bt') == button_text:
                button_parent_selector  = d.get('bs')
                button_text             = d.get('bt')
                dialog_selector         = d.get('ds')
                dialog_title            = d.get('dt')
                okey_text               = d.get('ot')
                cancel_text             = d.get('ct')
                close_on_esc            = d.get('ce')
                break

        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Знаходить потрібну кнопку і натискає її
        parent = self.browser.find_element_by_css_selector(button_parent_selector)
        xpath = "//button[contains(.,'%s')]" % button_text
        elements = parent.find_elements_by_xpath(xpath)
        self.assertEqual(len(elements), 1)
        button = elements[0]

        actions = ActionChains(self.browser)
        actions.move_to_element(button)
        actions.click(button)
        actions.perform()

        # Чекає на появу спливаючого вікна
        try:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, dialog_selector))
            )
        except Exception as exception:
            print('exception:')
            print('this_url=', self.this_url,
                  '\nCSS_SELECTOR=', dialog_selector,
                  '\nexception=', exception)
            return
        dialog_elements = self.browser.find_elements_by_css_selector(dialog_selector)
        dialog = None
        for element in dialog_elements: # нас цікавить видимий діалог. інші ui-dialog's не містять текстів
            if element.value_of_css_property('display') != "none":
                dialog = element
        self.assertIsNotNone(dialog)

        dialog_box_form = self.browser.find_element_by_id("dialog-box-form")

        # Бачить правильний заголовок спливаючого вікна
        xpath = ".//span[contains(.,'%s')]" % dialog_title
        elements = dialog.find_elements_by_xpath(xpath)
        self.assertEqual(len(elements), 1)

        # Бачить правильний підпис поля вводу
        xpath = ".//label[@for='%s']" % "id_name"
        elements = dialog_box_form.find_elements_by_xpath(xpath)
        self.assertEqual(len(elements), 1)
        self.assertEqual(elements[0].text, "Назва теки")

        # Бачить правильне початкове значення у полі вводу
        xpath = ".//input[@id='%s']" % "id_name"
        elements = dialog_box_form.find_elements_by_xpath(xpath)
        self.assertEqual(len(elements), 1)
        inputbox = elements[0]
        self.assertEqual(inputbox.get_attribute("value"), "Тека без назви")

        # Видаляє з поля вводу непотрібну назву
        # inputbox.clear()
        ActionChains(self.browser).key_down(Keys.CONTROL).\
            send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()

        # Вводить дані в полі вводу
        inputbox.send_keys('New_folder')

        # Натискає ENTER
        # inputbox.send_keys(Keys.ENTER)
        # Натискає кнопку Ok на спливаючому вікні
        xpath = ".//button[contains(.,'%s')]" % okey_text
        elements = dialog.find_elements_by_xpath(xpath)
        self.assertEqual(len(elements), 1)
        okey_button = elements[0]
        okey_button.click()

        # Переконується, що спливаюче вікно закрите
        self.assertTrue(button.is_displayed())
        self.assertTrue(button.is_enabled())

        # Залишається на тій же сторінці
        self.check_passed_link(expected_regex=self.this_url)

        # TODO-додати перевірку появи нового запису в тілі таблиці:
        # Бачить у кінці таблиці новостворений запис

        # Бачить, що новий запис є виділеним

        # Новий запис збереджено у базі даних
        folder = Folder.objects.last()
        self.assertEqual(folder.name, 'New_folder')
        this_folder = Folder.objects.get(id=1)
        self.assertEqual(folder.parent, this_folder)

        # Час створення (до секунди) співпадає з поточним?
        self.assertAlmostEqual(folder.created_on, now(), delta=timedelta(minutes=1))








        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderContentsPageAnonymousVisitorTest(FolderContentsPageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = AnonymousUser()
        DummyFolder().create_dummy_catalogue(report=True)
        self.get_data_links_number()

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderContentsPageAuthenticatedVisitorCanFindLinkTest(FolderContentsPageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    Чи всі дані правильно відображені?
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        DummyFolder().create_dummy_catalogue(report=True)
        self.get_data_links_number()

    def test_visitor_can_find_folder(self):
        # Користувач може  перейти по лінку потрібні дані
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        for f in Folder.objects.all():
            link_parent_selector = '#body-table'
            link_text            = get_full_named_path(f)
            url_name             = 'folders:folder-detail'
            kwargs               = {'pk': f.id}
            expected_regex       = ""
            self.check_go_to_link(self.this_url, link_parent_selector, link_text,
                url_name=url_name, kwargs=kwargs, expected_regex=expected_regex)
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    def test_visitor_can_find_report(self):
        # Користувач може  перейти по лінку потрібні дані
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        for f in Report.objects.all():
            link_parent_selector = '#body-table'
            link_text            = get_full_named_path(f)
            url_name             = 'folders:report-detail'
            kwargs               = {'pk': f.id}
            expected_regex       = ""
            self.check_go_to_link(self.this_url, link_parent_selector, link_text,
                url_name=url_name, kwargs=kwargs, expected_regex=expected_regex)
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderContentsPageAnonymousVisitorCanFindLinkTest(FolderContentsPageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    Чи всі дані правильно відображені?
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = AnonymousUser()
        DummyFolder().create_dummy_catalogue(report=True)
        self.get_data_links_number()

    def test_visitor_can_find_folder(self):
        # Користувач може  перейти по лінку потрібні дані
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        for f in Folder.objects.all():
            link_parent_selector = '#body-table'
            link_text            = get_full_named_path(f)
            url_name             = 'folders:folder-detail'
            kwargs               = {'pk': f.id}
            expected_regex       = "/noaccess/"
            self.check_go_to_link(self.this_url, link_parent_selector, link_text,
                url_name=url_name, kwargs=kwargs, expected_regex=expected_regex)
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    def test_visitor_can_find_report(self):
        # Користувач може  перейти по лінку потрібні дані
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        for f in Report.objects.all():
            link_parent_selector = '#body-table'
            link_text            = get_full_named_path(f)
            url_name             = 'folders:report-detail'
            kwargs               = {'pk': f.id}
            expected_regex       = "/noaccess/"
            self.check_go_to_link(self.this_url, link_parent_selector, link_text,
                url_name=url_name, kwargs=kwargs, expected_regex=expected_regex)
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

