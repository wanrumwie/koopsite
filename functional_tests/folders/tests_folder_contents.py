import calendar
import inspect
import os
import time
import types
import datetime
from unittest.case import skipIf, skip
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from os import unlink
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from folders.functions import get_full_named_path, get_parents
from folders.models import Folder, Report
from folders.tests.test_base import DummyFolder
from folders.views import FolderReportList
from functional_tests.koopsite.ft_base import PageVisitTest, get_test_files_cwd
from koopsite.functions import dict_print
from koopsite.settings import SKIP_TEST


# @skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderContentsPageVisitTest(PageVisitTest):
    """
    Допоміжний клас для функціональних тестів.
    Описані тут параметри - для перевірки одної сторінки сайту.
    Цей клас буде використовуватися як основа
    для класів тестування цієї сторінки з іншими користувачами.
    """
    this_folder_id = 2
    this_url    = '/folders/2/contents/'
    page_title  = 'Пасічний'
    page_name   = 'КАРТОТЕКА ФАЙЛІВ'
    saved_report_file_path = [] # файли, які треба видалити з диска після тестів

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
            {'bs':'#body-aside-1-buttons', 'bt': 'Нова тека'    , 'ds': self.dialog_box_form_selector, 'dt': 'Нова тека'             , 'ot': 'Ok', 'ct': 'Cancel', 'ce': True, },
            {'bs':'#body-aside-1-buttons', 'bt': 'Новий файл'   , 'ds': self.dialog_box_form_selector, 'dt': 'Новий файл'            , 'ot': 'Ok', 'ct': 'Cancel', 'ce': False, },
            {'bs':'#body-aside-1-buttons', 'bt': 'Завантажити'  , 'ds': self.dialog_box_form_selector, 'dt': 'Завантаження '         , 'ot': 'Ok', 'ct': 'Cancel', 'ce': True, },
            {'bs':'#body-aside-1-buttons', 'bt': 'Перейменувати', 'ds': self.dialog_box_form_selector, 'dt': 'Перейменування '       , 'ot': 'Ok', 'ct': 'Cancel', 'ce': True, },
            {'bs':'#body-aside-1-buttons', 'bt': 'Перемістити'  , 'ds': self.dialog_box_tree_selector, 'dt': 'Перемістити виділену ' , 'ot': 'Ok', 'ct': 'Cancel', 'ce': True, },
            {'bs':'#body-aside-1-buttons', 'bt': 'Видалити'     , 'ds': self.dialog_box_form_selector, 'dt': 'Видалення '            , 'ot': 'Ok', 'ct': 'Cancel', 'ce': True, },
            ]
        return s

    def get_popup_parameters_by_button_text(self, button_text):
        # Повертає параметри спливаючого вікна,
        # представлені для зручності як SimpleNamespace
        buttons = self.popup_activation_buttons_in_template()
        popup = None
        for d in buttons:
            if d.get('bt') == button_text:
                popup = types.SimpleNamespace(
                    button_parent_selector  = d.get('bs'),
                    button_text             = d.get('bt'),
                    dialog_selector         = d.get('ds'),
                    dialog_title            = d.get('dt'),
                    okey_text               = d.get('ot'),
                    cancel_text             = d.get('ct'),
                    close_on_esc            = d.get('ce'),
                )
                break
        return popup

    def get_data_length(self):
        this_folder_id = self.this_folder_id
        this_folder = Folder.objects.get(id=this_folder_id)
        self.table_data_length = len(Folder.objects.filter(parent=this_folder)) \
                               + len(Report.objects.filter(parent=this_folder))
        self.parents_data_length = len(get_parents(this_folder))
        self.data_length = self.table_data_length \
                         + self.parents_data_length \
                         + 1 # довжина списку з даними
        return self.data_length

    def get_data_links_number(self):
        self.data_links_number = self.get_data_length() # кількість лінків, які приходять в шаблон з даними
        self.data_links_number += self.get_num_page_links(self.get_data_length(), FolderReportList.paginate_by)[1]
        return self.data_links_number

    def folder_creation_by_visitor(self, new_name="new_folder", end_dialog_by="button", end_message_by="button"):
        # Параметри потрібної кнопки:
        button_text             = "Нова тека"
        popup = self.get_popup_parameters_by_button_text(button_text)

        inputbox_label_val      = "Назва теки"
        inputbox_default_val    = "Тека без назви"
        inputbox_new_val        = new_name          # PARAMETER
        message_title           = inputbox_new_val
        message_text            = "Теку створено!"
        message_okey_text       = "Ok"

        this_folder = Folder.objects.get(id=self.this_folder_id)

        # Знаходить потрібну кнопку і НАТИСКАЄ кнопку
        parent = self.browser.find_element_by_css_selector(popup.button_parent_selector)
        xpath = ".//button[contains(.,'%s')]" % popup.button_text
        button = self.find_single_by_xpath(parent, xpath)

        ActionChains(self.browser).move_to_element(button)\
            .click(button).perform()

        # Чекає на появу спливаючого вікна
        dialog = self.get_waited_visible_element(self.dialog_box_form_selector)

        # Бачить правильний заголовок спливаючого вікна
        xpath = ".//span[contains(.,'%s')]" % popup.dialog_title
        self.find_single_by_xpath(dialog, xpath)

        # Бачить правильний підпис поля вводу
        xpath = ".//label[@for='%s']" % "id_name"
        label = self.find_single_by_xpath(dialog, xpath)
        self.assertEqual(label.text, inputbox_label_val)

        # Бачить правильне початкове значення у полі вводу
        xpath = ".//input[@id='%s']" % "id_name"
        inputbox = self.find_single_by_xpath(dialog, xpath)
        self.assertEqual(inputbox.get_attribute("value"), inputbox_default_val)

        # ВИДАЛЯЄ з поля вводу непотрібне значення
        ActionChains(self.browser)\
            .key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)\
            .send_keys(Keys.DELETE).perform()

        # ВВОДИТЬ дані в полі вводу
        inputbox.send_keys(inputbox_new_val)

        # Завершує ввід натисканням...
        if end_dialog_by != "button":   # ... натисканням клавіші Enter на клавіатурі
            ActionChains(self.browser).send_keys(end_dialog_by).perform()
        else:                           # ... натисканням кнопки на спливаючому вікні
            self.terminate_dialog_by_button(dialog, popup.okey_text)

        # TODO-помилка очікування на спливаюче повідомлення (часом виникає, хоча візуально вікно з'являється і нова тека створюється)
        # Traceback: selenium.common.exceptions.TimeoutException: Message:
        # Помилка виникає, очевидно, тому, що в js виконується
        # така послідовність дій ( function xhrSuccessHandler( sr ) ):
        #   dialogMessage( sr.message, sr.type, sr.title, 2000 );
        #           ...
        #           setTimeout( function(){ $dialog_message.dialog( "close" ); }, time );
        #   dialog_box_form_close();
        #   addNewElement( sr.changes, sr.supplement ); // add new element; changes has all values of new element
        # Через setTimeout послідовність закривання вікон
        # dialog_message i dialog_box_form не завжди однакова.
        # Для виправлення варто:
        #   в dialogMessage додати callback функцію,
        #     яка буде виконуватися після закриття вікна message;
        #   xhrSuccessHandler змінити так,
        #     щоб switch описував для кожного пункту функцію callback,
        #     яка як переметр потім бередається в dialogMessage
        # Поки-що я просто переставляє очікування в цьому тесті:
        # спочатку повинно відкритися вікно message,
        # а потім закритися dialog_box

        # Бачить спливаюче повідомлення
        message = self.get_waited_visible_element(self.dialog_message_selector)

        # Бачить правильний заголовок і текст спливаючого повідомлення
        xpath = ".//span[contains(.,'%s')]" % message_title
        self.find_single_by_xpath(message, xpath)

        xpath = ".//div[contains(.,'%s')]" % message_text
        self.find_single_by_xpath(message, xpath)

        # Переконується, що спливаюче ОСНОВНЕ вікно закрите
        self.get_waited_invisible_element(self.dialog_box_form_selector)

        # Завершує перегляд повідомлення ...
        if end_message_by == "timer": # ... очікуванням заданого в повідомленні часу
            pass
        elif end_message_by != "button":  # ... натисканням клавіші Enter на клавіатурі
            ActionChains(self.browser).send_keys(end_message_by).perform()
        else:                   # ... кнопки на спливаючому вікні
            self.terminate_dialog_by_button(message, message_okey_text)

        # Переконується, що спливаюче повідомлення закрите
        self.get_waited_invisible_element(self.dialog_message_selector)

        # Залишається на тій же сторінці
        self.check_passed_link(expected_regex=self.this_url)

        # Новий запис збережено у базі даних
        folder = Folder.objects.last()
        self.assertEqual(folder.name, inputbox_new_val)
        self.assertEqual(folder.parent, this_folder)

        # Час створення (до хвилини) співпадає з поточним?
        self.assertAlmostEqual(folder.created_on, now(), delta=datetime.timedelta(minutes=1))

        # Бачить новий запис, який є виділеним
        tr = self.get_waited_visible_element(".selected")

        xpath = ".//a[contains(.,'%s')]" % inputbox_new_val
        a = self.find_single_by_xpath(tr, xpath)
        return folder, a    # new folder & <a> element of new added row

    def report_uploading_by_visitor(self, new_filename="example.jpg", end_dialog_by="button", end_message_by="button"):
        # Параметри потрібної кнопки:
        button_text             = "Новий файл"
        popup = self.get_popup_parameters_by_button_text(button_text)

        cwd_test = get_test_files_cwd()   # каталог з файлами для тестування
        new_filename_path = os.path.join(cwd_test, new_filename) # повний шлях

        inputbox_label_val      = "Назва файла"
        inputbox_default_val    = ""
        inputbox_new_val        = new_filename_path
        message_title           = new_filename
        message_text            = "Файл успішно заладовано на сервер!"
        message_okey_text       = "Ok"

        this_folder = Folder.objects.get(id=self.this_folder_id)

        # Знаходить потрібну кнопку і НАТИСКАЄ кнопку
        parent = self.browser.find_element_by_css_selector(popup.button_parent_selector)
        xpath = ".//button[contains(.,'%s')]" % popup.button_text
        button = self.find_single_by_xpath(parent, xpath)

        ActionChains(self.browser).move_to_element(button)\
            .click(button).perform()

        # Чекає на появу спливаючого вікна
        dialog = self.get_waited_visible_element(self.dialog_box_form_selector)

        # Бачить правильний заголовок спливаючого вікна
        xpath = ".//span[contains(.,'%s')]" % popup.dialog_title
        self.find_single_by_xpath(dialog, xpath)

        # Бачить правильний підпис поля вводу
        xpath = ".//label[@for='%s']" % "id_file"
        label = self.find_single_by_xpath(dialog, xpath)
        self.assertEqual(label.text, inputbox_label_val)

        # Бачить правильне початкове значення у полі вводу
        xpath = ".//input[@id='%s']" % "id_file"
        inputbox = self.find_single_by_xpath(dialog, xpath)
        self.assertEqual(inputbox.get_attribute("value"), inputbox_default_val)

        # Натискає кнопку Browse - емулюється шляхом посилання в цей елемент шляху до файла.
        # inputbox = self.browser.find_element_by_css_selector('input[type=file]')
        inputbox.send_keys(new_filename_path)

        # Завершує ввід натисканням...
        if end_dialog_by != "button":   # ... натисканням клавіші Enter на клавіатурі
            ActionChains(self.browser).send_keys(end_dialog_by).perform()
        else:                           # ... натисканням кнопки на спливаючому вікні
            self.terminate_dialog_by_button(dialog, popup.okey_text)

        # Бачить спливаюче повідомлення
        message = self.get_waited_visible_element(self.dialog_message_selector)

        # Бачить правильний заголовок і текст спливаючого повідомлення
        xpath = ".//span[contains(.,'%s')]" % message_title
        self.find_single_by_xpath(message, xpath)

        xpath = ".//div[contains(.,'%s')]" % message_text
        self.find_single_by_xpath(message, xpath)

        # Переконується, що спливаюче ОСНОВНЕ вікно закрите
        self.get_waited_invisible_element(self.dialog_box_form_selector)

        # Завершує перегляд повідомлення ...
        if end_message_by == "timer": # ... очікуванням заданого в повідомленні часу
            pass
        elif end_message_by != "button":  # ... натисканням клавіші Enter на клавіатурі
            ActionChains(self.browser).send_keys(end_message_by).perform()
        else:                   # ... кнопки на спливаючому вікні
            self.terminate_dialog_by_button(message, message_okey_text)

        # Переконується, що спливаюче повідомлення закрите
        self.get_waited_invisible_element(self.dialog_message_selector)

        # Залишається на тій же сторінці
        self.check_passed_link(expected_regex=self.this_url)

        # Новий запис збережено у базі даних
        report = Report.objects.last()
        self.assertEqual(report.filename, new_filename)
        self.assertEqual(report.parent, this_folder)

        print('report.file.path =', report.file.path)
        self.saved_report_file_path.append(report.file.path)
        # TODO-перевірити правильність збереження вмісту файла

        (mode, ino, dev, nlink, uid, gid, size, atime, modtime, cretime) \
            = os.stat(new_filename_path)
        print((mode, ino, dev, nlink, uid, gid, size, atime, modtime, cretime))
        print('   modtime  =', modtime)
        upload_time = calendar.timegm(report.uploaded_on.timetuple())
        print('upload_time =', upload_time)

        # self.assertEqual(folder.created_on.isoformat(), datetime(2015,12,25,tzinfo=UTC).isoformat())

        #  У параметр uploaded_on записано первинний час створення файла
        print('report.uploaded_on           =', report.uploaded_on)
        print('delta =', upload_time - modtime)
        self.assertAlmostEqual(upload_time, modtime, delta=1)

        # Бачить новий запис, який є виділеним
        tr = self.get_waited_visible_element(".selected")

        xpath = ".//a[contains(.,'%s')]" % new_filename
        a = self.find_single_by_xpath(tr, xpath)
        return report, a    # new report & <a> element of new added row


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderContentsPageAuthenticatedVisitorTest(FolderContentsPageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        # self.add_dummy_permission(self.dummy_user, codename='add_folder', model='folder')
        # self.add_dummy_permission(self.dummy_user, codename='add_report', model='report')
        DummyFolder().create_dummy_alfa_beta_catalogue()
        self.get_data_links_number()

    def tearDown(self):
        self.browser.delete_all_cookies()
        super().tearDown()

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
    def test_visitor_can_go_to_parent_links(self):
        # Користувач може перейти по лінках над таблицею
        this_folder = Folder.objects.get(id=self.this_folder_id)
        folders = get_parents(this_folder)
        folders.append(this_folder)
        for folder in folders:
            link_parent_selector = '#parent-folders-navigation'
            link_text            = '%s' % folder
            url_name             = 'folders:folder-contents'
            kwargs               = {'pk': folder.pk}
            self.check_go_to_link(self.this_url, link_parent_selector,
                link_text, url_name=url_name, kwargs=kwargs)
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

    # @skip
    def test_visitor_can_click_popup_activation_buttons(self):
        # Користувач може клацнути по всіх кнопках на сторінці і повернутися назад
        self.visitor_can_click_popup_activation_buttons()
        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderContentsPageVisitorCanCreateFolderTest(FolderContentsPageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='add_folder', model='folder')
        # self.add_dummy_permission(self.dummy_user, codename='add_report', model='report')
        DummyFolder().create_dummy_alfa_beta_catalogue()
        self.get_data_links_number()

    def tearDown(self):
        self.browser.delete_all_cookies()
        super().tearDown()

    # TODO-зробити тест створення нової теки у ПОРОЖНІЙ теці
    # @skip
    def test_visitor_can_create_folder(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Бачить в таблиці правильну кількість рядків
        n = self.table_data_length   # кількість рядків у таблиці
        tbody = self.get_waited_visible_element("tbody")
        xpath = ".//tr"
        elements = tbody.find_elements_by_xpath(xpath)
        self.assertEqual(len(elements), n)

        # Створює нову таблицю
        folder, a = self.folder_creation_by_visitor("New folder")

        # Загальна кількість записів у таблиці правильна
        tbody = self.browser.find_element_by_tag_name('tbody')
        elements = tbody.find_elements_by_tag_name('tr')
        self.assertEqual(len(elements), n + 1)
        self.assertTrue("selected" in elements[n].get_attribute("class"))

        # TODO-помилка створення ще одної нової теки: повідомлення "така назва вже існує",
        # але тека створюється і стає видима в таблиці з правильною назвою.
        # Причину, мабуть, теж вдасться усунути з доп. callback до dialogMessage

        # Створює ще одну нову таблицю
        # folder, a = self.folder_creation_by_visitor("Newest folder", end_dialog_by=Keys.ENTER,
        #                                             end_message_by=Keys.ESCAPE)

        # Загальна кількість записів у таблиці правильна
        # tbody = self.browser.find_element_by_tag_name('tbody')
        # elements = tbody.find_elements_by_tag_name('tr')
        # self.assertEqual(len(elements), n + 2)
        # self.assertTrue("selected" in elements[n+1].get_attribute("class"))

        # Натискає клавішу Enter і потрапляє на сторінку нової теки
        a.send_keys(Keys.ENTER)
        href= reverse('folders:folder-contents', kwargs={'pk': folder.pk})

        self.check_passed_link(expected_regex=href)

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderContentsPageVisitorCanUploadReportTest(FolderContentsPageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        # self.add_dummy_permission(self.dummy_user, codename='add_folder', model='folder')
        self.add_dummy_permission(self.dummy_user, codename='add_report', model='report')
        DummyFolder().create_dummy_alfa_beta_catalogue()
        self.get_data_links_number()
        self.saved_report_file_path = []

    def tearDown(self):
        for path in self.saved_report_file_path:
            try:
                unlink(path)
                print('deleted: ', path)
            except:
                pass
        self.browser.delete_all_cookies()
        super().tearDown()

    # TODO-зробити тест завантаження нового файла у ПОРОЖНЮ теку
    # TODO-не працює завантаження файла 500Kb у порожню теку
    # ("...probably file too long"). Однак після того як файл
    # був завантаженй синхронним методом (Картотека(ст.)),
    # у цю ж теку він був повторно завантажений аяксом без проблем.

    def test_visitor_can_upload_report(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Бачить в таблиці правильну кількість рядків
        n = self.table_data_length   # кількість рядків у таблиці
        tbody = self.get_waited_visible_element("tbody")
        xpath = ".//tr"
        elements = tbody.find_elements_by_xpath(xpath)
        self.assertEqual(len(elements), n)

        # Заладовує новий файл
        report, a = self.report_uploading_by_visitor("example.jpg")

        # Загальна кількість записів у таблиці правильна
        tbody = self.browser.find_element_by_tag_name('tbody')
        elements = tbody.find_elements_by_tag_name('tr')
        self.assertEqual(len(elements), n + 1)
        self.assertTrue("selected" in elements[n].get_attribute("class"))

        # Натискає клавішу Enter і потрапляє на сторінку перегляду нового файла
        a.send_keys(Keys.ENTER)
        href= reverse('folders:report-view', kwargs={'pk': report.pk})

        # TODO-перевірити, який href встановлюється для нового запису
        # AssertionError: Regex didn't match: '/folders/report/3/view/' not found in 'http://localhost:8081/folders/report/3/'

        self.check_passed_link(expected_regex=href)

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')



# @skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderContentsPageVisitorCanSearchTest(FolderContentsPageVisitTest):
    """
    Тест пошуку теки в каталозі
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        # self.add_user_cookie_to_browser(self.dummy_user)
        # self.add_dummy_permission(self.dummy_user, codename='add_folder', model='folder')
        # self.add_dummy_permission(self.dummy_user, codename='add_report', model='report')
        DummyFolder().create_dummy_alfa_beta_catalogue()
        self.get_data_links_number()

    def tearDown(self):
        self.browser.delete_all_cookies()
        super().tearDown()

    # @skip
    def test_visitor_can_search_folder(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # В каталозі є кілька тек/файлів з однаковими фрагментами назв
        # Користувач збирається знайти теку або файл, у назві якої є букви "sigm"
        button_text = "Пошук"
        dialog_title = "Результати пошуку"
        inputbox_search_val = "sigm"
        exact_search_val = "sigma_report_3"
        expected_n = 3
        expected_report = Report.objects.get(filename=exact_search_val)
        expected_parent = expected_report.parent
        expected_href= reverse('folders:folder-contents', kwargs={'pk': expected_parent.pk})

        # Користувач знаходить поле пошуку
        inputbox = self.browser.find_element_by_id("id_search")

        # Вводить в полі пошуку
        inputbox.send_keys(inputbox_search_val)

        # Під полем пошуку з'являється список слів, які вже колись шукав користувач


        # Знаходить потрібну кнопку і НАТИСКАЄ кнопку
        parent = self.browser.find_element_by_css_selector("#body-aside-2")
        xpath = ".//button[contains(.,'%s')]" % button_text
        button = self.find_single_by_xpath(parent, xpath)

        ActionChains(self.browser).move_to_element(button)\
            .click(button).perform()

        # Чекає на появу спливаючого вікна
        dialog = self.get_waited_visible_element(self.dialog_search_results_selector)

        # Бачить правильний заголовок спливаючого вікна
        xpath = ".//span[contains(.,'%s')]" % dialog_title
        self.find_single_by_xpath(dialog, xpath)

        # Бачить у спливаючому вікні список всіх знайдених тек
        # і файлів, у яких є шукане слово

        rows = dialog.find_elements_by_css_selector("tbody tr")

        # Кількість знайдених тек/файлів - правильна
        self.assertEqual(len(rows), expected_n)

        # Шукане слово виділене у кожному рядку списку іншим кольором/шрифтом

        # Користувач вибирає один з рядків і клікає мишкою
        xpath = ".//a[contains(.,'%s')]" % exact_search_val
        a = rows.self.find_single_by_xpath(rows, xpath)

        a.send_keys(Keys.ENTER)

        # Спливаюче вікно закривається, і користувач опиняється у теці, яка містить обраний файл/теку
        self.check_passed_link(expected_regex=expected_href)

        # Бачить шуканий файл/теку, який є виділеним
        tr = self.get_waited_visible_element(".selected")

        xpath = ".//a[contains(.,'%s')]" % exact_search_val
        a = self.find_single_by_xpath(tr, xpath)


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

