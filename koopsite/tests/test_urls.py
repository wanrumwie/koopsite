import importlib
from django.test import TestCase
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver, reverse, resolve
from koopsite.urls import urlpatterns

def get_view_from_RegexURLPattern(u):
    func = u._callback
    module_name = func.__module__
    func_name = func.__name__
    module = importlib.import_module(module_name)
    try:
        view = getattr(module, func.__name__)
        try:
            templ_name = view.template_name
        except:
            templ_name = ''
        try:
            form_class = view.form_class
        except:
            form_class = ''
    except:
        templ_name = ''
        form_class = ''
    return module_name, func_name, templ_name, form_class


class WalkURL():
    def __init__(self, urlpatterns, exclude_namespace=None, only_namespace=None, trace=False):
        self.urlpatterns = urlpatterns
        self.trace = trace
        if exclude_namespace:
            if isinstance(exclude_namespace, list):
                self.exclude_namespace = exclude_namespace
            else:
                self.exclude_namespace = [exclude_namespace]
        else:
            self.exclude_namespace = []
        if only_namespace:
            if isinstance(only_namespace, list):
                self.only_namespace = only_namespace
            else:
                self.only_namespace = [only_namespace]
        else:
            self.only_namespace = []
        if self.trace:
            print("WalkURL(exclude_namespace =", self.exclude_namespace)
            print("WalkURL(   only_namespace =", self.only_namespace)
        self.all_url_names = []
        self.get_all_url_names()

    def url_walk(self, urlpatterns, prefix='^', namespace=None):
        for u in urlpatterns:
            if type(u) == RegexURLPattern:
                # print(u._callback, u._callback.__module__, u._callback.__name__, u.__dict__)
                s = u.regex.pattern
                s = prefix + s.lstrip('^')
                ns = ('%s:' % namespace) if namespace else ''
                ns_name = '%s%s' % (ns, u.name)
                flag = True
                if self.only_namespace:
                    flag = flag and namespace and namespace in self.only_namespace
                if flag:
                    self.all_url_names.append((s, ns_name))
                # x = get_view_from_name(ns_name)
                if self.trace:
                    module_name, func_name, templ_name, form_class = \
                        get_view_from_RegexURLPattern(u)
                    # print('%-50s, %-15s, %-20s, %-20s, %-20s, %-20s, %s' %
                    #  (s, ns, u.name, module_name, func_name, templ_name, form_class))
                    print('%s,%s,%s,%s,%s,%s,%s' %
                     (s, ns, u.name, module_name, func_name, templ_name, form_class))
            if type(u) == RegexURLResolver:
                ns = u.namespace or '--'
                flag = True
                if self.exclude_namespace:
                    flag = flag and ns not in self.exclude_namespace
                if self.only_namespace:
                    flag = flag and ns and ns in self.only_namespace
                if self.trace:
                    print('%10s %s' % (flag ,ns))
                if flag:
                    self.url_walk(u.url_patterns,
                                  prefix=u.regex.pattern,
                                  namespace=u.namespace)

    def get_all_url_names(self):
        self.url_walk(self.urlpatterns, prefix='^', namespace=None)
        return self.all_url_names

def get_duplicates(lst):
    d = [x for x in lst if lst.count(x) > 1]
    return d

def get_duplicates_in_tuple_list(lst):
    u_list = []
    n_list = []
    for u, n in lst:
        u_list.append(u)
        n_list.append(n)
    du = []
    dn = []
    for u, n in lst:
        if u_list.count(u) > 1: du.append((u, n))
        if n_list.count(n) > 1: dn.append((u, n))
    return du, dn

if_trace = False

class UrlNameSpaceTest(TestCase):

    def test_no_duplicate_urls(self):
        all_url = WalkURL(urlpatterns,
                          trace=if_trace,
                          exclude_namespace=['js_tests']).all_url_names
        # print('all_urls exclude js:')
        # for u, n in sorted(all_url):
        #     print('%-60s %s' % (u, n))
        # print('-'*50)
        dupl_in_urls, dupl_in_name = get_duplicates_in_tuple_list(all_url)
        if dupl_in_urls:
            print('urls duplicates:')
            for u, n in dupl_in_urls:
                print('%-50s %s' % (u, n))
        if dupl_in_name:
            print('name duplicates:')
            for u, n in dupl_in_name:
                print('%-50s %s' % (u, n))
        self.assertEqual(len(dupl_in_name), 0, 'Виявлено дублікати в назвах url')
        self.assertEqual(len(dupl_in_urls), 0, 'Виявлено дублікати в шаблонах url')

    def test_root_equal_index(self):
        self.assertEqual('/', reverse('root'))
        self.assertEqual('/index/', reverse('index'))
        found1 = resolve('/')
        found2 = resolve('/index/')
        self.assertEqual(found1.func, found2.func)

    def test_no_duplicate_urls_js(self):
        all_url = WalkURL(urlpatterns,
                          trace=if_trace,
                          only_namespace=['js_tests']).all_url_names
        # print('urls js_tests:')
        # for u, n in sorted(all_url):
            # print('%-60s %s' % (u, n))
        # print('-'*50)
        dupl_in_urls, dupl_in_name = get_duplicates_in_tuple_list(all_url)
        if dupl_in_urls:
            print('urls duplicates:')
            for u, n in dupl_in_urls:
                print('%-50s %s' % (u, n))
        if dupl_in_name:
            print('name duplicates:')
            for u, n in dupl_in_name:
                print('%-50s %s' % (u, n))
        self.assertEqual(len(dupl_in_name), 0, 'Виявлено дублікати в назвах url')
        self.assertEqual(len(dupl_in_urls), 0, 'Виявлено дублікати в шаблонах url')


