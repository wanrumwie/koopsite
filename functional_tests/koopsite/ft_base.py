import os
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
import sys
import time
from selenium.webdriver.support.wait import WebDriverWait
from koopsite.functions import round_up_division, get_miniature_path
from koopsite.settings import PYTHON_ANYWHERE
from koopsite.tests.test_base import DummyUser
if PYTHON_ANYWHERE:
    from pyvirtualdisplay import Display


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



class FunctionalTest(StaticLiveServerTestCase): # працює з окремою спеціально
                                                # створюваною БД для тестів
                                                # + статичні файли
    server_url = None       # резервуємо імена, які будуть
    this_url   = None       # означені в дочірніх класах

    @classmethod
    def setUpClass(cls):
        print('start class: %s' % cls.__name__, end=' >> ')
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
            actions = ActionChains(self.browser)
            actions.move_to_element(href)
            actions.click(href)
            actions.perform()
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



class PageVisitTest(DummyUser, FunctionalTest):
    """
    Допоміжний клас для функціональних тестів.
    Описані тут параметри - для перевірки головної сторінки сайту.
    Цей клас буде використовуватися як основа
    для класів тестування інших сторінок.
    """
    this_url    = '/index/'
    page_title  = 'Пасічний'
    page_name   = 'Головна сторінка'
    data_links_number = 0   # кількість лінків, які приходять в шаблон з даними

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
        # Спочатку визначаються деякі параметри:
        username, flat_id, flat_No = self.get_user_name_flat(user)
        s = [
            {'ls':'#body-aside-1-navigation'  , 'lt': 'Увійти'           , 'un': 'login'       , 'cd': "not user.is_authenticated()"},
            {'ls':'#body-aside-1-navigation'  , 'lt': 'Зареєструватися'  , 'un': 'register'    , 'cd': "not user.is_authenticated()"},
            # {'ls':'#body-navigation'          , 'lt': 'Головна сторінка' , 'un': 'index'},##########
            {'ls':'#body-navigation'          , 'lt': 'Квартири'         , 'un': 'flats:flat-scheme'},
            {'ls':'#body-navigation'          , 'lt': 'Картотека'        , 'un': 'folders:folder-contents', 'kw': {'pk': 1}, 'st': 5},
            {'ls':'#body-navigation'          , 'lt': 'Увійти'           , 'un': 'login'       , 'cd': "not user.is_authenticated()"},
            {'ls':'#body-navigation'          , 'lt': 'Зареєструватися'  , 'un': 'register'    , 'cd': "not user.is_authenticated()"},
            {'ls':'#body-navigation'          , 'lt': 'Мій профіль'      , 'un': 'own-profile' , 'cd': "user.is_authenticated()"},
            {'ls':'#body-navigation'          , 'lt': 'Адміністрування'  , 'un': 'adm-index'   , 'cd': "user.has_perm('koopsite.activate_account')"},
            # {'ls':'#body-navigation'          , 'lt': 'Назад           ' , 'un': '"javascript:history.back()"'},#########
            {'ls':'#header-aside-2-navigation', 'lt': username           , 'un': 'own-profile' , 'cd': "user.is_authenticated()"},
            {'ls':'#header-aside-2-navigation', 'lt': "Кв." + flat_No    , 'un': "flats:flat-detail", 'kw': {'pk': flat_id}, 'cd': "user.is_authenticated() and user.userprofile.flat"},
            {'ls':'#header-aside-2-navigation', 'lt': 'Вийти'            , 'un': 'logout'      , 'cd': "user.is_authenticated()", 'er': '/index/'},
            {'ls':'#header-aside-2-navigation', 'lt': 'Авторизуватися'   , 'un': 'login'       , 'cd': "not user.is_authenticated()"},
            ]
        return s

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


