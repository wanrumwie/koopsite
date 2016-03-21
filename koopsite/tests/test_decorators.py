from unittest.mock import Mock
from django.http.response import HttpResponseRedirect
from django.test import TestCase
from django.test.client import RequestFactory
from folders.models import Report
from folders.tests.test_base import DummyFolder
from koopsite.decorators import author_or_permission_required, request_passes_test
from koopsite.models import UserProfile
from koopsite.tests.test_base import DummyUser

class AuthorPermissionDecoratorTest(TestCase):

    def setUp(self):

        # Параметри, при яких декоратор пропускає до функції:
        user = DummyUser().create_dummy_user(username='user1')
        user.has_perms = Mock()
        user.has_perms.return_value = True

        user2 = DummyUser().create_dummy_user(username='user2')
        user2.has_perms = Mock()
        user2.has_perms.return_value = True

        root = DummyFolder().create_dummy_root_folder()
        object = DummyFolder().create_dummy_report(root,
                                    id=1, filename='report1', user=user)

        object2 = DummyFolder().create_dummy_report(root,
                                    id=2, filename='report2')

        model = Report

        request = RequestFactory()
        request.build_absolute_uri = Mock()
        request.build_absolute_uri.return_value = "" # path
        request.get_full_path = Mock()
        request.get_full_path.return_value = "" # path
        request.user = user

        view_func = Mock()
        view_func.return_value = 'passed'

        test_func = Mock()
        test_func.return_value = True

        self.user = user
        self.user2 = user2
        self.object = object
        self.model = model
        self.request = request
        self.view_func = view_func
        self.test_func = test_func
        self.perm = 'can'

        # print(self.user)
        # print(self.object)
        # print(self.object.pk)
        # print(self.model)
        # print(self.model())
        # print(self.request)
        # print(self.request.user)
        # ob = getattr(model, 'pk')
        # print(ob)


    # Наступні тести перевіряють в request_passes_test()
    # лише два рядки коду:
    #         if test_func(request, *args, **kwargs):
    #             return view_func(request, *args, **kwargs)
    # Перевіряти решту нема потеби, оскільки весь інший код
    # без змін взято з user_passes_test()

    def test_request_passes_test_True(self):
        test_func = self.test_func
        view_func = self.view_func

        decorated = request_passes_test(test_func)

        self.assertEqual(test_func(0), True)
        self.assertEqual(view_func(0), 'passed')
        self.assertEqual(decorated(view_func)(self.request), 'passed')
        self.assertEqual(decorated(view_func)(self.request, 's'), 'passed')
        self.assertEqual(decorated(view_func)(self.request, pk='1'), 'passed')
        self.assertEqual(decorated(view_func)(self.request, pk='2'), 'passed')

    def test_request_passes_test_False(self):
        test_func = self.test_func
        view_func = self.view_func

        test_func.return_value = False

        decorated = request_passes_test(test_func)

        self.assertEqual(test_func(0), False)
        self.assertEqual(view_func(0), 'passed')
        self.assertEqual(type(decorated(view_func)(self.request)), HttpResponseRedirect)


    # Наступні тести перевіряють в author_or_permission_required()
    # лише такі рядки коду:
    #     if 'pk' in kwargs:
    #         object_id = kwargs['pk']
    #         object = get_object_or_404(model, pk=object_id)
    #         if user == object.user:
    #             return True
    # Перевіряти решту нема потеби, оскільки весь інший код
    # без змін взято з permission required()

    def test_author_or_permission_required_User_1_Permission_True(self):
        view_func = self.view_func

        decorated = author_or_permission_required(self.model, self.perm)

        self.assertEqual(view_func(0), 'passed')
        self.assertEqual(decorated(view_func)(self.request, pk='1'), 'passed')
        self.assertEqual(decorated(view_func)(self.request, pk='2'), 'passed')


    def test_author_or_permission_required_User_1_Perm_False(self):
        view_func = self.view_func

        self.user.has_perms.return_value = False

        decorated = author_or_permission_required(self.model, self.perm)

        self.assertEqual(view_func(0), 'passed')
        self.assertEqual(decorated(view_func)(self.request, pk='1'), 'passed')
        self.assertEqual(type(decorated(view_func)(self.request, pk='2')), HttpResponseRedirect)


    def test_author_or_permission_required_User_False_Perm_True(self):
        view_func = self.view_func

        self.request.user = self.user2

        decorated = author_or_permission_required(self.model, self.perm)

        self.assertEqual(view_func(0), 'passed')
        self.assertEqual(decorated(view_func)(self.request, pk='1'), 'passed')
        self.assertEqual(decorated(view_func)(self.request, pk='2'), 'passed')


    def test_author_or_permission_required_User_False_Perm_False(self):
        view_func = self.view_func

        self.request.user = self.user2
        self.user2.has_perms.return_value = False

        decorated = author_or_permission_required(self.model, self.perm)

        self.assertEqual(view_func(0), 'passed')
        self.assertEqual(type(decorated(view_func)(self.request, pk='1')), HttpResponseRedirect)
        self.assertEqual(type(decorated(view_func)(self.request, pk='2')), HttpResponseRedirect)

    # Перевірка цього декоратора для іншої моделі, а саме UserProfile:
    def test_author_or_permission_required_UserProfile_Perm_False(self):
        view_func = self.view_func

        self.user.has_perms.return_value = False

        DummyUser().create_dummy_profile(self.user, id=3)
        DummyUser().create_dummy_profile(self.user2, id=4)

        decorated = author_or_permission_required(UserProfile, "")

        self.assertEqual(view_func(0), 'passed')
        self.assertEqual(decorated(view_func)(self.request, pk='3'), 'passed')
        self.assertEqual(type(decorated(view_func)(self.request, pk='4')), HttpResponseRedirect)


