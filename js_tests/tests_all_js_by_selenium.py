import inspect
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functional_tests.koopsite.ft_base import PageVisitTest
from koopsite.tests.test_urls import WalkURL
from koopsite.urls import urlpatterns


class JsQunitPageTest(PageVisitTest):
    """
    Допоміжний клас для js-тестів.
    """
    this_url    = '/js_tests/'

    def get_hrefs(self):
        # Отримуємо список href з файлів urls.py
        all_url = WalkURL(urlpatterns,
                          trace=False,
                          only_namespace=['js_tests']).all_url_names
        exclude_list = [    # список непотрібних href
            r'/js_tests/$',
            r'/js_tests/example/$',
            r'/js_tests/folders/$',
            ]
        hrefs = []
        for u, n in all_url:
            href = u.replace('^', '/')
            href = href.rstrip('$')
            # Відкидаємо зайві
            match = False
            for exclude in exclude_list:
                if re.search(exclude, href):
                    match = True
                    break
            if not match:
                hrefs.append(href)
        return sorted(hrefs)


# @skipIf(SKIP_TEST, "пропущено для економії часу")
class JsQunitTest(JsQunitPageTest):
    """
    Клас запускає всі js-тести
    """
    def setUp(self):
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        # Формуємо список атрибутів href елементів <a> - вони будуть
        # на всіх сторінках js тестів
        self.hrefs = self.get_hrefs()

    def test_run_all_js_qunit_tests(self):
        passed = 0
        failed = 0
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        try:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".qunit-pass"))
            )
        except Exception as exception:
            print('href=', self.this_url, 'exception=', exception)
            return
        for href in self.hrefs:
            link = self.browser.find_element_by_xpath("//a[@href='%s']" % href)
            link_text = link.text
            try:
                actions = ActionChains(self.browser)
                actions.move_to_element(link)
                actions.click(link)
                actions.perform()
            except Exception as exception:
                print('href=', href, 'exception=', exception)
                break

            passing_url = self.browser.current_url  # url після переходу
            self.assertRegex(passing_url, href)
            try:
                WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".qunit-pass"))
                )
                # print('%-25s %-10s %-10s %s' % (link_text,'', 'success', passing_url))
                print('.',end='')
                passed += 1
            except:
                print('\n','%-25s %-10s %-10s %s' % (link_text,'', 'FAIL!', passing_url))
                failed += 1

            self.browser.find_element_by_id("qunit-urlconfig-noglobals").click()
            try:
                WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".qunit-pass"))
                )
                # print('%-25s %-10s %-10s %s' % (link_text,'Globals', 'success', passing_url))
                passed += 1
            except:
                print('\n','%-25s %-10s %-10s %s' % (link_text,'Globals', 'FAIL!', passing_url))
                failed += 1

        self.assertEqual(passed, 2*len(self.hrefs), 'Не всі js тести пройшли успішно')

        print('finished: %s' % inspect.stack()[0][3], end=' >> ')

