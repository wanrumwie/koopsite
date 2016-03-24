import os
import time
import sys
from time import sleep
from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, \
                       HASH_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from koopsite.functions import round_up_division, get_miniature_path
from koopsite.settings import PYTHON_ANYWHERE
from koopsite.tests.test_base import DummyUser
if PYTHON_ANYWHERE:
    from pyvirtualdisplay import Display


def find_elements_by_css_text(parent, css_selector='*', text=''):
    css_elements = parent.find_elements_by_css_selector(css_selector)
    elements = []
    for element in css_elements:
        if element.text == text:
            elements.append(element)
    return elements



def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 3:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )


class wait_for_page_load(object):

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        wait_for(self.page_has_loaded)

def find_css(self, css_selector):
    """Shortcut to find elements by CSS. Returns either a list or singleton"""
    elems = self.find_elements_by_css_selector(css_selector)
    found = len(elems)
    if found == 1:
        return elems[0]
    elif not elems:
        raise NoSuchElementException(css_selector)
    return elems

def wait_for_css(self, css_selector, timeout=7):
    """ Shortcut for WebDriverWait"""
    return WebDriverWait(self, timeout).until(lambda driver : driver.find_css(css_selector))



def create_user_session(user):
    # Then create the authenticated session using the new user credentials
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    return session

def create_cookie(session):
    # Finally, create the cookie dictionary
    cookie = {
        'name': settings.SESSION_COOKIE_NAME,
        'value': session.session_key,
        'secure': False,
        'path': '/',
    }
    return cookie

def get_test_files_cwd():
    # Повертає шлях до теки, де розміщені файли
    # для тестування функцій завантаження, обробки зображення тощо.
    cwd = os.getcwd()   # поточний каталог (в цьому каталозі manage.py)
    path = os.path.join(cwd, 'functional_tests', 'files') # повний шлях
    return path

def create_dummy_miniature_file(big_file_name):
    # Створюємо файл 200*200 з великого файла jpg
    # УВАГА! Функція залишає на диску файл з шляхом mini_path
    # Для прикладу беремо цей файл:
    cwd_test = get_test_files_cwd()   # каталог з файлами для тестування
    full_path = os.path.join(cwd_test, big_file_name) # повний шлях

    # Створимо для порівняння мініатюру розміром x на y:
    # Розміри збереженого зображення:
    x = 200
    y = 200
    size='%sx%s' % (x, y)
    mini_path = get_miniature_path(full_path, size)
    try:
        image = Image.open(full_path)
        image.thumbnail([x, y], Image.ANTIALIAS)
        try:
            image.save(mini_path, image.format, quality=90, optimize=1)
        except:
            image.save(mini_path, image.format, quality=90)
    except:
        pass
    # Вміст мініатюрного файла для наступного порівняння
    with open(mini_path, 'rb') as f:
        expected_mini_content = f.read()

    # Створюємо file_content для SimpleUploadedFile
    with open(full_path, 'rb') as f:
        file_content = f.read()
    uploaded_big_file = SimpleUploadedFile(big_file_name, file_content)
    return full_path, mini_path, uploaded_big_file, expected_mini_content



class FunctionalTest(StaticLiveServerTestCase):
    # працює з окремою спеціально створюваною БД для тестів
    # + статичні файли
    browser     = None
    display     = None
    server_url  = None       # резервуємо імена, які будуть
    this_url    = None       # означені в дочірніх класах

    @classmethod
    def setUpClass(cls):
        print('start class: %s' % cls.__name__, end=' >> ')
        # TODO-Знайти причину помилки NoSuchElementException у ВСІХ FT тестах на pythonanywhere.com
        # Задавав у bash команду:
        # xvfb-run python manage.py test functional_tests.flats.tests_flat_list --liveserver=wanrumwie.pythonanywhere.com:8081
        if PYTHON_ANYWHERE:
            cls.display = Display(visible=0, size=(800, 600))
            cls.display.start()
            print('pyvirtualdisplay.display.start()', end=' >> ')
        browser_created = False
        print('webdriver.Firefox()', end=' >> ')
        for i in range(3):
            print('try Nr%s' % i, end=' >> ')
            try:
                cls.browser = webdriver.Firefox()
                print('browser created', end=' >> ')
                browser_created = True
                break
            except:
                print('except', end=' >> ')
                sleep(3)
        if not browser_created:
            if PYTHON_ANYWHERE:
                cls.display.stop() # ignore any output from this.
                print('pyvirtualdisplay.display.stop()')

        # assert browser_created, 'webdriver.Firefox() browser is not created'

        cls.browser.implicitly_wait(20)
        cls.browser.set_script_timeout(20)
        cls.browser.set_page_load_timeout(20)

        cls.browser.set_window_position(250, 0)
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        # cls.browser.refresh()
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()
        cls.browser.quit()
        if PYTHON_ANYWHERE:
            cls.display.stop() # ignore any output from this.
            print('pyvirtualdisplay.display.stop()', end=' >> ')
        print('finished class: %s' % cls.__name__)

    # def setUp(self):
    #     pass

    def tearDown(self):
        super().tearDown()


class PageVisitTest(DummyUser, FunctionalTest):
    """
    Допоміжний клас для функціональних тестів.
    Цей клас буде використовуватися як основа
    для класів тестування сторінок сайту.
    """
    this_url    = '/index/'
    page_title  = 'Пасічний'
    page_name   = 'Головна сторінка'
    data_links_number = 0   # кількість лінків, які приходять в шаблон з даними

    # CSS-селектори спливаючих діалогів:
    dialog_box_form_selector = "[aria-describedby=dialog-box-form]"
    dialog_confirm_selector  = "[aria-describedby=dialog-confirm]"
    dialog_message_selector  = "[aria-describedby=dialog-message]"
    dialog_box_tree_selector = "[aria-describedby=dialog-box-tree]"

    def add_user_cookie_to_browser(self, user, url=None):
        session = create_user_session(user)
        cookie = create_cookie(session)
        # visit some url in your domain to setup Selenium.
        if not url: url = '/selenium-cookie-setup/'
        self.browser.get('%s%s' % (self.server_url, url))
        # add the newly created session cookie to selenium webdriver.
        self.browser.add_cookie(cookie)
        # refresh to exchange cookies with the server.
        self.browser.refresh()

    def eval_condition(self, condition, user):
        # перевірка умови, заданої стрічкою
        # У складі стрічки можлива наявність виразів типу user.is_staff,
        # тому user приходить сюди як параметр
        if condition:
            try:    c = eval(condition)
            except: c = None
        else:
            c = True    # відсутність умови рівносильна виконанню умови
        # print('user =', user, 'cd =', condition, 'eval =', c)
        return c

    def check_passed_link(self, url_name=None, kwargs=None, expected_regex=None):
        """
        Допоміжна функція для функц.тесту.
        Перевіряє, чи здійснено перехід по лінку, заданому url_name
        :param url_name: назва, з якої ф-цією reverse отримується url переходу
        :param kwargs: евентуальні параметри url
        :param expected_regex: очікуваний url - альтернатива reverse(url_name, kwargs)
        :return:
        """
        passing_url = self.browser.current_url  # url після переходу
        if url_name and not expected_regex:
            expected_regex = reverse(url_name, kwargs=kwargs)
        expected_regex = expected_regex.lstrip('^')
        self.assertRegex(passing_url, expected_regex)

    def check_go_to_link(self, this_url, link_parent_selector, link_text,
                        url_name=None, kwargs=None, expected_regex=None,
                        partial=False, href_itself=None, sleep_time=None):
        """
        Допоміжна функція для функц.тесту. Викликається в циклі for
        для кожного лінка на сторінці.
        Перевіряє, чи користувач може перейти по лінку, заданому url_name
        з текстом "link_text"
        :param this_url: сторінка що тестується
        :param link_parent_selector: CSS-селектор елемента з лінками
        :param link_text: видимий текст лінка
        :param url_name: назва, з якої ф-цією reverse отримується url переходу
        :param kwargs: евентуальні параметри url
        :param expected_regex: очікуваний url - задавати при переадресації, бо тоді він інакший, ніж reverse(url_name)
        :param partial: часткове чи повне співпадіння тексту лінка
        :param href_itself: атрибут href, за яким йде пошук, якщо не задано link_text
        :param sleep_time: час очікування вкінці на завершення процесів на відвіданій сторінці
        :return:
        """
        self.browser.get('%s%s' % (self.server_url, this_url))
        # print(link_parent_selector, link_text, expected_regex)
        #
        # TODO-виловити помилку при очікуванні на сторінку "Картотека" головної сторінки.
        # Помилка виникає часом.
        # Trace:
        # selenium.common.exceptions.UnexpectedAlertPresentException: Alert Text: xhrErrorAlert:
        #  xhr.status=0
        #  xhr.statusText=error
        #  xhr.responseText={"server_response": {"selRowIndex": 0, "model": null, "id": null}}
        #
        # TODO-2015 12 31 помилка xhrError
        # selenium.common.exceptions.UnexpectedAlertPresentException: Alert Text: xhrErrorAlert:
        #  xhr.status=0
        #  xhr.statusText=error
        #  xhr.responseText=
        # <super: <class 'WebDriverException'>, <UnexpectedAlertPresentException object>>

        if url_name and not expected_regex:
            expected_regex = reverse(url_name, kwargs=kwargs)
        expected_regex = expected_regex.lstrip('^')

        # print('link_parent_selector =', link_parent_selector)
        # print('link_text =', link_text)

        parent = self.browser.find_element_by_css_selector(link_parent_selector)

        if link_text:
            if partial: href = parent.find_element_by_partial_link_text(link_text)
            else:       href = parent.find_element_by_link_text(link_text)
        elif href_itself:
            href = parent.find_element_by_xpath("//a[contains(@href,'%s')]" % href_itself)
        else:
            href = None

        # print('href.location_once_scrolled_into_view =', href.location_once_scrolled_into_view)

        try:
            ActionChains(self.browser).move_to_element(href)\
                .click(href).perform()
        except Exception as exception:
            print('Attention: Exception in actions caused probably by too long searched link text:')
            print(link_text)
            print(exception)
            return
        passing_url = self.browser.current_url  # url після переходу

        # print('link_parent_selector =', link_parent_selector)
        # print('link_text =', link_text)
        # print('href =', href)
        # print('url_name =', url_name)
        # print('kwargs =', kwargs)
        # print('passing_url =', passing_url)
        # print('expected_regex =', expected_regex)

        self.assertRegex(passing_url, expected_regex)
        if sleep_time:
            sleep(sleep_time)   # чекаємо на завершення обміну даними на деяких сторінках

    def get_link_location(self, link_parent_selector, link_text):
        parent = self.browser.find_element_by_css_selector(
                                                link_parent_selector)
        href = parent.find_element_by_link_text(link_text)
        location = href.location
        size = href.size
        return location, size

    def get_error_element(self, selector=".error"):
        return self.browser.find_element_by_css_selector(selector)

    def get_error_elements_for_field(self, css_selector, error_class='errorlist'):
        field = self.browser.find_element_by_css_selector(css_selector)
        xpath = "preceding-sibling::ul[@class='%s']" % error_class
        return field.find_elements_by_xpath(xpath)

    def choose_option_in_select(self, inputbox, val='1'):
        all_options = inputbox.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute('value') == val :
                option.click()

    def can_visit_page(self):
        # Користувач може відвідати сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        # Ця сторінка справді є сторінкою потрібного сайту
        self.assertIn(self.page_title, self.browser.title)
        # Цe потрібна сторінка
        header_text = self.browser.find_element_by_id('page-name').text
        self.assertEqual(self.page_name, header_text)

    def can_not_visit_page(self, expected_regex='/noaccess/'):
        # Користувач НЕ може відвідати сторінку і буде переадресований
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        passing_url = self.browser.current_url  # url після переходу
        expected_regex = expected_regex.lstrip('^')
        self.assertRegex(passing_url, expected_regex)

    def get_user_name_flat(self, user):
        try:    username = user.username
        except: username = ""
        try:    flat_id = user.userprofile.flat.id
        except: flat_id = ""
        try:    flat_No = user.userprofile.flat.flat_No
        except: flat_No = ""
        return username, flat_id, flat_No

    def get_num_page_links(self, list_len, paginate_by):
        # Повертає к-ть сторінок і к-ть лінків пейджінатора
        if paginate_by:
            num_pages = round_up_division(list_len, paginate_by)
            if   num_pages == 1: page_links_number = 0
            elif num_pages == 2: page_links_number = 1
            else: page_links_number = 2
        else:
            num_pages = 1
            page_links_number = 0
        return num_pages, page_links_number

    def links_in_template(self, user):
        # Перелік лінків, важливих для сторінки.
        # Повертає список словників, які поступають як параметри до функції
        #     def check_go_to_link(self, this_url, link_parent_selector, link_text,
        #                           expected_regex=None, url_name=None, kwargs=None,
        #                           sleep_time=0):
        # Ключі словників скорочені до 2-х літер: ls lt er un kw st
        # плюс cd - condition для перевірки видимості лінка (буде аргументом ф-ції eval() ).
        assert True == False, 'Клас PageVisitTest: потрібно означити метод: links_in_template'
        return []

    def visitor_can_go_to_links(self):
        # Лінки, вказані в шаблоні (в т.ч. і недоступні через умову if):
        links =  self.links_in_template(self.dummy_user)
        # Сторінка має всі передбачені лінки (по кількості)
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        elements = self.browser.find_elements_by_tag_name('a')
        visible_links = []
        for d in links:
            condition = d.get('cd')
            link_must_be_visible = self.eval_condition(condition, self.dummy_user)
            if link_must_be_visible :
                visible_links.append(d)
        expected = len(visible_links)
        expected += self.data_links_number # + лінки в таблицях з даними. Ці лінки даних не входять до словника links_in_template.
        self.assertEqual(len(elements), expected,
              msg="Кількість лінків на сторінці не відповідає очікуваній")
        # Користувач може перейти по всіх лінках на сторінці
        # Беремо список словників, які описують всі лінки на цій сторінці.
        # Ключі словників скорочені до 2-х літер: ls lt er un kw cd.
        for d in visible_links:
            link_parent_selector = d.get('ls')
            link_text            = d.get('lt')
            url_name             = d.get('un')
            kwargs               = d.get('kw')
            expected_regex       = d.get('er')
            sleep_time           = d.get('st')
            self.check_go_to_link(self.this_url, link_parent_selector,
                link_text, url_name=url_name, kwargs=kwargs,
                expected_regex=expected_regex, sleep_time=sleep_time)

    def layout_and_styling_page(self, delta=10):
        # Користувач відвідує сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        self.browser.set_window_size(1024, 800)
        # Заголовок сайта добре відцентрований
        box = self.browser.find_element_by_id('site-header')
        real = box.location['x'] + box.size['width'] / 2
        expected = 512
        self.assertAlmostEqual(real, expected, delta=delta, msg="Не працює CSS.")

    def popup_activation_buttons_in_template(self):
        assert True == False, 'Клас PageVisitTest: потрібно означити метод: popup_activation_buttons_in_template'
        return []

    def visitor_can_click_popup_activation_buttons(self):
        # Кнопки, вказані в шаблоні:
        buttons = self.popup_activation_buttons_in_template()
        # Користувач може клацнути по всіх заданих кнопках на сторінці і повернутися назад
        # Беремо список словників, які описують всі кнопки на цій сторінці.
        # Ключі словників скорочені до 2-х літер: bs bt ds dt ot ct ce.
        for d in buttons:
            button_parent_selector  = d.get('bs')
            button_text             = d.get('bt')
            dialog_selector         = d.get('ds')
            dialog_title            = d.get('dt')
            okey_text               = d.get('ot')
            cancel_text             = d.get('ct')
            close_on_esc            = d.get('ce')
            self.check_button_click_popup_appearance(self.this_url,
                        button_parent_selector, button_text,
                        dialog_selector, dialog_title,
                        okey_text, cancel_text, close_on_esc)


    def get_waited_visible_element(self, css_selector):
        element = WebDriverWait(self.browser, 10).until(
                    EC.visibility_of_element_located((
                        By.CSS_SELECTOR, css_selector))
        )
        self.assertIsNotNone(element)
        return element

    def get_waited_invisible_element(self, css_selector):
        element = WebDriverWait(self.browser, 10).until(
                    EC.invisibility_of_element_located((
                        By.CSS_SELECTOR, css_selector))
        )
        self.assertIsNotNone(element)
        self.assertFalse(element.is_displayed())
        return element

    def find_single_by_xpath(self, parent, xpath):
        elements = parent.find_elements_by_xpath(xpath)
        self.assertEqual(len(elements), 1)
        return  elements[0]

    def terminate_dialog_by_button(self, dialog, button_text="Ok"):
        # Завершує спливаючий діалог натисканням кнопки на ньому з надписом button_text
        xpath = ".//button[contains(.,'%s')]" % button_text
        button = self.find_single_by_xpath(dialog, xpath)
        ActionChains(self.browser).move_to_element(button)\
            .click(button).perform()

    def check_button_click_popup_appearance(self, this_url,
                button_parent_selector, button_text,
                dialog_selector=None, dialog_title=None,
                okey_text=None, cancel_text=None, close_on_esc=None):
        """
        Допоміжна функція для функц.тесту. Викликається в циклі for
        для кожної кнопки на сторінці.
        Перевіряє, чи користувач може натиснути на кнопку,
        побачити спливаюче вікно-діалог,
        і закрити його кнопкою Cancel і/або клавішею Esc
        НЕ перевіряє натискання кнопки Ok на спливаючому вікні!
        :param this_url: сторінка що тестується
        :param button_parent_selector: CSS-селектор елемента з кнопками
        :param button_text           : текст на кнопці
        :param dialog_selector       : CSS-селектор спливаючого діалогового вікна
        :param dialog_title          : титут спливаючого діалогового вікна
        :param okey_text             : текст на кнопці Okey спливаючого діалогового вікна
        :param cancel_text           : текст на кнопці Cancel спливаючого діалогового вікна
        :param close_on_esc          : умова closeOnEscape спливаючого діалогового вікна
        :return:
        """
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, this_url))

        # Знаходить потрібну кнопку і натискає її
        parent = self.browser.find_element_by_css_selector(button_parent_selector)
        xpath = "//button[contains(.,'%s')]" % button_text
        button = self.find_single_by_xpath(parent, xpath)
        ActionChains(self.browser).move_to_element(button)\
            .click(button).perform()

        # Чекає на появу спливаючого вікна
        dialog = self.get_waited_visible_element(dialog_selector)

        # Бачить правильний заголовок спливаючого вікна
        xpath = ".//span[contains(.,'%s')]" % dialog_title
        self.find_single_by_xpath(dialog, xpath)

        # TODO-зробити перевірку модальності спливаючого вікна
        # Переконується, що спливаюче вікно модальне
        # self.assertTrue(button.is_displayed())
        # self.assertFalse(button.is_enabled())

        # Бачить правильні надписи на кнопках спливаючого вікна
        xpath = ".//button[contains(.,'%s')]" % okey_text
        self.find_single_by_xpath(dialog, xpath)

        xpath = ".//button[contains(.,'%s')]" % cancel_text
        self.find_single_by_xpath(dialog, xpath)

        # Натискає кнопку Cancel на спливаючому вікні
        self.terminate_dialog_by_button(dialog, cancel_text)

        # Переконується, що спливаюче ОСНОВНЕ вікно закрите
        self.get_waited_invisible_element(dialog_selector)

        if close_on_esc:    # перевірка закривання вікна клавішею Esc

            # Ще раз натискає кнопку і чекає на появу спливаючого вікна
            ActionChains(self.browser).move_to_element(button)\
                .click(button).perform()
            dialog = self.get_waited_visible_element(dialog_selector)

            # Натискає клавішу Esc на клавіатурі
            ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()

            # Ще раз переконується, що спливаюче ОСНОВНЕ вікно закрите
            self.get_waited_invisible_element(dialog_selector)


    def template_input_values_print(self):
        f_name = self.browser.find_element_by_css_selector("#thisfolder span").text
        print('\nf_name =', f_name)
        template_id_list = [
            "list_length"    ,
            "json_arr"       ,
            "browTabName"    ,
            "selRowIndex"    ,
            "selElementModel",
            "selElementID"   ,
        ]
        for t_id in template_id_list:
            v = self.browser.find_element_by_id(t_id).get_attribute("value")
            print('%-20s %s' % (t_id, v))

    def wait_presence_of_element(self, css_selector):
        # Чекає на появу спливаючого вікна
        try:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
        except Exception as exception:
            print('exception:')
            print('CSS_SELECTOR=', css_selector,
                  '\nexception=', exception)
            return

    def get_displayed_dialog(self, dialog_selector='.ui-dialog'):
        # Повертає видимий елемент спливаючого вікна-діалога
        dialog_elements = self.browser.find_elements_by_css_selector(dialog_selector)
        dialog_elements_print(dialog_elements, 'dialog_elements')
        dialog = None
        for element in dialog_elements: # нас цікавить видимий діалог. інші ui-dialog's не містять текстів
            if element.value_of_css_property('display') != "none":
                dialog = element
        return  dialog

def dialog_elements_print(elements, *args):
    '''
    Допоміжна функція для друку UI dialog елементів Selenium
    :param elements:
    :return:
    '''
    if not isinstance(elements, (list, tuple)):
        elements = (elements, )
    print('\n', *args)
    print('='*77)
    print('%-20s %-10s %-10s %-10s %-20s %s' %
          ('aria', 'tag_name', 'displayed', 'display','text', 'element'))
    for element in elements:
        text = element.text
        if text:
            tt = text.split('\n')
            text = ' & '.join(tt)
        print('%-20s %-10s %-10s %-10s %-20s %s' %
              (element.get_attribute('aria-describedby'),
               element.tag_name,
               element.is_displayed(),
               element.value_of_css_property('display'),
               text,
               element))
    print('-'*77)

def elements_print(elements, *args):
    '''
    Допоміжна функція для друку елементів Selenium
    :param elements:
    :return:
    '''
    if not isinstance(elements, (list, tuple)):
        elements = (elements, )
    print('\n', *args)
    print('='*77)
    print('%-20s %-15s %-10s %-5s %-5s %-10s %-10s %-10s %-10s %s' %
          ('text', 'aria', 'tag_name', 'displ', 'enabl',
          'id', 'name', 'type', 'display', 'element'))
    for element in elements:
        print('%-20s %-15s %-10s %-5s %-5s %-10s %-10s %-10s %-10s %s' %
              (element.text, element.get_attribute('aria-describedby'),
               element.tag_name, element.is_displayed(), element.is_enabled(),
              element.get_attribute('id'), element.get_attribute('name'),
              element.get_attribute('type'), element.value_of_css_property('display'),
              element))
    print('-'*77)
