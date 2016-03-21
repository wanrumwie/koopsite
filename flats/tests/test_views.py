from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test.client import RequestFactory
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView
from flats.models import Flat
from flats.tests.test_base import DummyFlat
from flats.views import FlatScheme, FlatDetail, \
                        FlatDetailHorizontal, FlatList, FlatTable, FlatSchemeUsers, FlatUsersList
import flats.views

# @skip
from koopsite.functions import dict_print
from koopsite.settings import LOGIN_URL
from koopsite.tests.test_base import DummyUser
from koopsite.tests.test_views import setup_view


class FlatListTest(TestCase):

    def setUp(self):
        self.cls_view = FlatList
        self.path = '/flats/list/'
        self.template = 'flats/flat_list.html'

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model,                Flat)
        self.assertEqual(view.context_object_name, 'flat_list')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_view_renders_proper_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_200(self):
        request = RequestFactory().get(self.path)
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)


class FlatSchemeTest(TestCase):

    def setUp(self):
        self.cls_view = FlatScheme
        self.path = '/flats/scheme/'
        self.template = 'flats/flat_scheme.html'

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model,                Flat)

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_view_renders_proper_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_200(self):
        request = RequestFactory().get(self.path)
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_context_data(self):
        # Імітуємо будинок з одної квартири:
        floors = ['0']
        entrances = ['1']
        flat = Flat(floor_No=0, entrance_No=1)
        flat.save()
        block_scheme = {'0': {'1': [flat, ]}}
        # {0: {1: [flat, ], 2: [flat, ]}, 1: {1: [flat, ], 2: [flat, ]},}
        block_length = {'1': 1}
        kwargs = {'block_scheme': block_scheme,
                  'block_length': block_length,
                  'floors'      : floors,
                  'entrances'   : entrances,
                }
        # Setup request and view.
        request = RequestFactory().get('/flats/scheme/')
        view = FlatScheme()
        view = setup_view(view, request, kwargs)
        # Run.
        context = view.get_context_data()
        # Check.
        self.assertEqual(context['block_scheme'], block_scheme)
        self.assertEqual(context['block_length'], block_length)
        self.assertEqual(context['floors']      , floors)
        self.assertEqual(context['entrances']   , entrances)

    def test_context_data_2(self):
        # Імітуємо будинок з кількох квартир:
        flat1 = Flat(floor_No=1, entrance_No=1)
        flat1.save()
        flat2 = Flat(floor_No=2, entrance_No=2)
        flat2.save()
        flat3 = Flat(floor_No=2, entrance_No=2)
        flat3.save()
        floors = ['2', '1']
        entrances = ['1', '2']
        block_scheme = {'1': {'1': [flat1]}, '2': {'2': [flat2, flat3]}}
        # {0: {1: [flat, ], 2: [flat, ]}, 1: {1: [flat, ], 2: [flat, ]},}
        block_length = {'1': 1, '2': 2}
        kwargs = {
                'block_scheme' : block_scheme,
                'block_length' : block_length,
                'floors'       : floors,
                'entrances'    : entrances,
        }
        # Setup request and view.
        request = RequestFactory().get('/flats/scheme/')
        view = FlatScheme()
        view = setup_view(view, request, kwargs)
        # Run.
        context = view.get_context_data()
        # Check.
        self.assertEqual(context['block_scheme'], block_scheme)
        self.assertEqual(context['block_length'], block_length)
        self.assertEqual(context['floors']      , floors)
        self.assertEqual(context['entrances']   , entrances)

    def test_context_data_3(self):
        # Імітуємо будинок з кількох квартир:
        floors = (1, 2)
        entrances = (1, 2)
        DummyFlat().create_dummy_building(floors=floors, entrances=entrances)
        d, floors, entrances = flats.views.block_scheme()
        l = flats.views.block_length(d)
        kwargs = {
                'block_scheme' : d,
                'block_length' : l,
                'floors'       : floors,
                'entrances'    : entrances,
        }
        # dict_print(kwargs, 'kwargs')
        # Setup request and view.
        request = RequestFactory().get('/flats/scheme/')
        view = FlatScheme()
        view = setup_view(view, request, kwargs)
        # Run.
        context = view.get_context_data()
        # Check.
        self.assertEqual(context['block_scheme'], d)
        self.assertEqual(context['block_length'], l)
        self.assertEqual(context['floors']      , floors)
        self.assertEqual(context['entrances']   , entrances)


class FlatDetailTest(TestCase):

    def setUp(self):
        self.cls_view = FlatDetail
        self.path = '/flats/5/'
        self.template = 'flats/flat_detail.html'
        flat = Flat(id=5, flat_No='5')
        flat.save()

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Flat)
        self.assertEqual(view.paginate_by, 14)
        self.assertEqual(view.exclude, ('id', 'flat_99', 'note', 'listing'))

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_view_renders_proper_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_200(self):
        request = RequestFactory().get(self.path)
        view = self.cls_view.as_view()
        response = view(request, pk=5)
        self.assertEqual(response.status_code, 200)


class FlatDetailHorizontalTest(TestCase):

    def setUp(self):
        self.cls_view = FlatDetailHorizontal
        self.path = '/flats/5/h/'
        self.template = 'flats/flat_detail_h.html'
        flat = Flat(id=5, flat_No='5')
        flat.save()

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Flat)
        self.assertEqual(view.paginate_by, 0)
        self.assertEqual(view.exclude, ('id', 'flat_99', 'note', 'listing'))

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_view_renders_proper_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_200(self):
        request = RequestFactory().get(self.path)
        view = self.cls_view.as_view()
        response = view(request, pk=5)
        self.assertEqual(response.status_code, 200)


class FlatTableTest(TestCase):

    def setUp(self):
        self.cls_view = FlatTable
        self.path = '/flats/table/'
        self.template = 'flats/flat_table.html'

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Flat)
        self.assertEqual(view.paginate_by, 15)
        self.assertEqual(view.exclude, ('id', 'flat_99', 'note', 'listing'))
        self.assertEqual(view.context_object_name, "field_vals")
        self.assertEqual(view.context_verbose_list_name, "field_names")

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_view_renders_proper_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_200(self):
        request = RequestFactory().get(self.path)
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)


class FlatSchemeUsersTest(TestCase):

    def setUp(self):
        self.cls_view = FlatSchemeUsers
        self.path = '/flats/scheme-users/'
        self.template = 'flats/flat_scheme_users.html'

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertTrue(issubclass(self.cls_view, FlatScheme))

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_view_renders_no_template_AnonymousUser(self):
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_no_template_user_wo_permission(self):
        DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_proper_template(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'view_userprofile')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))
        # Перевіряємо response.url.startswith(), бо перевірка:
        # self.assertRedirects(response, LOGIN_URL)
        # дає помилку:
        # AttributeError: 'HttpResponseRedirect' object has no attribute 'client'

    def test_view_gives_response_status_code_302_user_wo_permission(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))
        # Перевіряємо response.url.startswith(), бо перевірка:
        # self.assertRedirects(response, LOGIN_URL)
        # дає помилку:
        # AttributeError: 'HttpResponseRedirect' object has no attribute 'client'

    def test_view_gives_response_status_code_200(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'view_userprofile')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)


class FlatUsersListTest(TestCase):

    def setUp(self):
        self.cls_view = FlatUsersList
        self.path = '/flats/1/users-list/'
        self.template = 'flats/flat_users_list.html'
        john, paul, george, ringo, freddy = DummyUser().create_dummy_beatles()
        flat1, flat2 = DummyUser().set_flats_to_beatles(john, paul, george, ringo, freddy)
        DummyUser().add_dummy_permission(john, 'view_userprofile')
        self.john = john
        self.paul = paul
        self.flat1 = flat1

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertTrue(issubclass(self.cls_view, SingleObjectMixin))
        self.assertTrue(issubclass(self.cls_view, ListView))

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_view_renders_no_template_AnonymousUser(self):
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_no_template_user_wo_permission(self):
        self.client.login(username='paul', password='secret')
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_proper_template(self):
        self.client.login(username='john', password='secret')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))
        # Перевіряємо response.url.startswith(), бо перевірка:
        # self.assertRedirects(response, LOGIN_URL)
        # дає помилку:
        # AttributeError: 'HttpResponseRedirect' object has no attribute 'client'

    def test_view_gives_response_status_code_302_user_wo_permission(self):
        self.client.login(username='paul', password='secret')
        request = RequestFactory().get(self.path)
        request.user = self.paul
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))
        # Перевіряємо response.url.startswith(), бо перевірка:
        # self.assertRedirects(response, LOGIN_URL)
        # дає помилку:
        # AttributeError: 'HttpResponseRedirect' object has no attribute 'client'

    def test_view_gives_response_status_code_200(self):
        self.client.login(username='john', password='secret')
        request = RequestFactory().get(self.path)
        request.user = self.john
        view = self.cls_view.as_view()
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_queryset(self):
        request = RequestFactory().get(self.path)
        kwargs = {'pk': 1}
        view = self.cls_view()
        view = setup_view(view, request, **kwargs)
        # view.model = Report
        view.object = self.flat1
        expected = [self.john]
        qs = view.get_queryset()
        self.assertEqual(qs, expected)

