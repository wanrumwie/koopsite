import json
import os
import types

from PIL import Image
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.db.utils import IntegrityError
from django.test import TestCase

from flats.models import Flat
from flats.tests.test_base import DummyFlat
from folders.models import Folder
from functional_tests.koopsite.ft_base import DummyUser
from koopsite.functions import round_up_division, AllFieldsMixin, \
    get_namespace_from_dict, get_iconPathForFolder, \
    get_iconPathByFileExt, \
    fileNameCheckInsert, scale_height, scale_width, \
    getSelections, getSelElementFromSession, setSelElementToSession, \
    parseClientRequest, parseXHRClientRequest, get_user_full_name, \
    get_user_flat_No, get_user_is_recognized, is_staff_only, get_or_none, \
    has_group_members, has_group, add_group, remove_group, \
    transliterate, get_thumbnail_url_path, get_flat_users, \
    has_flat_member, dict_from_json_str_or_bytes, get_miniature_path, CheckPathMatchMediaPattern
from koopsite.settings import MEDIA_ROOT
from koopsite.tests.test_viewsajax import DummyAjaxRequest, \
    DummyXHRrequest


class DifferentFunctionsTest(TestCase):

    def test_dict_from_decoded_json_str(self):
        # json_str = {"message": "\u0424\u0430\u0439\u043b \u0443\u0441\u043f\u0456\u0448\u043d\u043e \u0437\u0430\u0432\u0430\u043d\u0442\u0430\u0436\u0435\u043d\u043e!", "changes": {"0": {"model": "report", "id": "1", "name": "file.txt"}}, "supplement": {"fileType": "report", "iconPath": "/static/img/file-icons/32px/txt.png", "fileExt": ".txt"}, "type": "Normal", "title": "file.txt"}
        expected = {'1': 1, '2': '2', 'x': None, 'y': 'Альфа'}
        json_str = json.dumps(expected)
        d = dict_from_json_str_or_bytes(json_str)
        self.assertEqual(d, expected)
        d = dict_from_json_str_or_bytes(json_str.encode())
        self.assertEqual(d, expected)

    def test_get_or_none(self):
        flat = DummyFlat().create_dummy_flat(id=1, flat_No="1")
        self.assertEqual(get_or_none(Flat, id=1), flat)
        self.assertEqual(get_or_none(Flat, id=1, flat_No="1"), flat)
        self.assertFalse(get_or_none(Flat, id=1, flat_No="2"))

    def test_get_or_none_gives_error_if_multiple(self):
        DummyFlat().create_dummy_building()
        with self.assertRaises(MultipleObjectsReturned):
            get_or_none(Flat, floor_No="2")

    def test_round_up_division(self):
        self.assertEqual(round_up_division(5, 5), 1)
        self.assertEqual(round_up_division(101, 100), 2)
        self.assertEqual(round_up_division(200, 100), 2)
        self.assertEqual(round_up_division(100.001, 100), 2)
        self.assertEqual(round_up_division(100.001, 100.001), 1)

    def test_get_iconPathForFolder(self):
        self.assertEqual(get_iconPathForFolder(True), 'img/open_folder.png')
        self.assertEqual(get_iconPathForFolder(False), 'img/folder.png')

    def test_get_iconPathByFileExt(self):
        self.assertEqual(get_iconPathByFileExt(""), "img/file-icons/32px/_page.png")
        self.assertEqual(get_iconPathByFileExt(".doc"), 'img/file-icons/32px/doc.png')


class FileNameCheckInsertTest(TestCase):

    def setUp(self):
        self.fileNameList = ['alfa.txt', 'beta.txt', 'beta (1).txt',
                             'gama.txt', 'gama (1).txt', 'gama (2).txt']

    def test_fileNameCheckInsert_1(self):
        fileName = 'delta.txt'
        expected = 'delta.txt'
        self.assertEqual(fileNameCheckInsert(fileName, self.fileNameList), expected)

    def test_fileNameCheckInsert_2(self):
        fileName = 'alfa.txt'
        expected = 'alfa (1).txt'
        self.assertEqual(fileNameCheckInsert(fileName, self.fileNameList), expected)

    def test_fileNameCheckInsert_3(self):
        fileName = 'beta.txt'
        expected = 'beta (2).txt'
        self.assertEqual(fileNameCheckInsert(fileName, self.fileNameList), expected)

    def test_fileNameCheckInsert_4(self):
        fileName = 'gama.txt'
        expected = 'gama (3).txt'
        self.assertEqual(fileNameCheckInsert(fileName, self.fileNameList), expected)


class Scale_height_width_Test(TestCase):

    def test_scale_width(self):
        self.assertEqual(scale_width(100, 100, 1000), (100, 100))
        self.assertEqual(scale_width(100, 100,    0), (  0,   0))
        self.assertEqual(scale_width(  0, 100,    0), (  0,   0))
        self.assertEqual(scale_width(100, 100,   30), ( 30,  30))

    def test_scale_height(self):
        self.assertEqual(scale_height(100, 100, 1000), (100, 100))
        self.assertEqual(scale_height(100, 100,    0), (  0,   0))
        self.assertEqual(scale_height(100,   0,    0), (  0,   0))
        self.assertEqual(scale_height(100, 100,   30), ( 30,  30))


class GetSelectionsTest(TestCase):

    def setUp(self):
        self.session = {}

    def test_getSelections(self):
        expected = {'foldertab':
                         {'1':
                             {'model'       : Folder,
                              'id'          : id,
                              'selRowIndex' : 55,
                             },
                         },
                    }
        self.session['Selections'] = expected
        self.assertEqual(getSelections(self.session), expected)

    def test_getSelections_2(self):
        self.session['Selections'] = None
        self.assertEqual(getSelections(self.session), {})

    def test_getSelections_3(self):
        self.session['q'] = 'a'
        self.assertEqual(getSelections(self.session), {})

    def test_getSelections_4(self):
        self.session['Selections'] = [1,]
        self.assertEqual(getSelections(self.session), {})

# @skip
class GetSelElementFromSessionTest(TestCase):

    def setUp(self):
        self.session = {}
        self.session['Selections'] = {'foldertab':
                                         {'1':
                                             {'model'       : Folder,
                                              'id'          : 12,
                                              'selRowIndex' : 55,
                                             },
                                         },
                                    }

    def test_selElementFromSessionTest(self):
        expected = {'model'       : Folder,
                    'id'          : 12,
                    'selRowIndex' : 55,
                    }
        b = 'foldertab'
        p = 1
        self.assertEqual(getSelElementFromSession(self.session, b, p), expected)

    def test_selElementFromSessionTest2(self):
        expected = {'model'       : None,
                    'id'          : None,
                    'selRowIndex' : None,
                    }
        b = 'usertab'
        p = 1
        self.assertEqual(getSelElementFromSession(self.session, b, p), expected)

    def test_selElementFromSessionTest3(self):
        expected = {'model'       : None,
                    'id'          : None,
                    'selRowIndex' : None,
                    }
        b = 'foldertab'
        p = 2
        self.assertEqual(getSelElementFromSession(self.session, b, p), expected)

    def test_selElementFromSessionTest4(self):
        expected = {'model'       : None,
                    'id'          : None,
                    'selRowIndex' : None,
                    }
        b = 'foldertab'
        self.assertEqual(getSelElementFromSession(self.session, b), expected)


class SetSelElementToSessionTest(TestCase):

    def setUp(self):
        self.session = {}

    def test_selElementToSessionTest(self):
        b = 'foldertab'
        p = 1
        s = {'model'      : Folder,
            'id'          : 12,
            'selRowIndex' : 55,
            }
        expected = {'foldertab':
                         {'1':
                             {'model'       : Folder,
                              'id'          : 12,
                              'selRowIndex' : 55,
                             },
                         },
                    }
        setSelElementToSession(self.session, b, p, s)
        self.assertEqual(self.session['Selections'], expected)
        p = '1'
        setSelElementToSession(self.session, b, p, s)
        self.assertEqual(self.session['Selections'], expected)

    def test_selElementToSessionTest_2(self):
        b = 'foldertab'
        p = 1
        expected = {'foldertab':
                         {'1':
                             {'model'       : None,
                              'id'          : None,
                              'selRowIndex' : None,
                             },
                         },
                    }
        setSelElementToSession(self.session, b, p)
        self.assertEqual(self.session['Selections'], expected)
        # TODO-нагадати собі, для чого зберігати в сесії дані з id=""? Бо наступний тест не проходить:
        # setSelElementToSession(self.session, b)
        # self.assertEqual(self.session['Selections'], expected)


class ParseClientRequestTest(TestCase):

    def test_parseClientRequest(self):
        kwargs = {
                    'browTabName' :'users_table',
                    'parent_id'   :None,
                    'sendMail'    :None,
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'1',
                    'name'        :'fred',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        expected = kwargs
        self.assertEqual(parseClientRequest(request.POST), expected)

    def test_parseClientRequest_not_full_data(self):
        kwargs = {
                    'browTabName' :'users_table',
                    'model'       :'user',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        expected = {
                    'browTabName' :'users_table',
                    'model'       :'user',
                }
        self.assertEqual(parseClientRequest(request.POST), expected)

    def test_parseClientRequest_can_expand_d(self):
        kwargs = {
                    'EXTRA': 'extra',
                    'browTabName' :'users_table',
                    'parent_id'   :None,
                    'sendMail'    :None,
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'1',
                    'name'        :'fred',
                }

        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        expected = kwargs
        self.assertEqual(parseClientRequest(request.POST), expected)

    def test_parseClientRequest_raise_error_if_model_table_mismatch(self):
        kwargs = {
                    'browTabName' :'users_table',
                    'model'       :'folder',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        with self.assertRaises(ValueError):
            parseClientRequest(request.POST)

    def test_parseClientRequest_raise_error_if_no_table(self):
        kwargs = {
                    'browTabName' :'',
                    'model'       :'folder',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        with self.assertRaises(ValueError):
            parseClientRequest(request.POST)

    def test_parseClientRequest_raise_error_if_unknown_table(self):
        kwargs = {
                    'browTabName' :'TABLE',
                    'model'       :'folder',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        with self.assertRaises(ValueError):
            parseClientRequest(request.POST)

    def test_parseClientRequest_if_no_model(self):
        kwargs = {
                    'browTabName' :'users_table',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        expected = {
                    'browTabName' :'users_table',
                }
        self.assertEqual(parseClientRequest(request.POST), expected)


class ParseXHRClientRequestTest(TestCase):
    # для тесту взято дані, роздруковані в ході виконання report download

    def test_parseXHRClientRequest(self):
        request = self.client.request()
        request.META = {'PYTHONIOENCODING': 'UTF-8', 'HTTP_X_CLIENT_REQUEST': '%7B%22browTabName%22%3A%22folders_contents%22%2C%22parent_id%22%3A%227%22%2C%22selRowIndex%22%3A%222%22%2C%22model%22%3A%22report%22%2C%22id%22%3A%22130%22%2C%22name%22%3A%22%D0%92%D1%96%D0%B4%D1%80%D1%8F%D0%B4%D0%B6%D0%B5%D0%BD%D0%BD%D1%8F.tif%22%7D', }
        expected = {'model': 'report', 'browTabName': 'folders_contents', 'selRowIndex': '2', 'id': '130', 'parent_id': '7', 'name': 'Відрядження.tif'}
        self.assertEqual(parseXHRClientRequest(request.META), expected)

    def test_parseXHRClientRequest_2(self):
        kwargs = {
                    'browTabName' :'users_table',
                    'parent_id'   :None,
                    'sendMail'    :None,
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'1',
                    'name'        :'fred',
                }
        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        expected = kwargs
        self.assertEqual(parseXHRClientRequest(request.POST), expected)

    def test_parseXHRClientRequest_not_full_data(self):
        kwargs = {
                    'browTabName' :'users_table',
                    'model'       :'user',
                }
        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        expected = {
                    'browTabName' :'users_table',
                    'model'       :'user',
                }
        self.assertEqual(parseXHRClientRequest(request.POST), expected)

    def test_parseXHRClientRequest_can_expand_d(self):
        kwargs = {
                    'EXTRA': 'extra',
                    'browTabName' :'users_table',
                    'parent_id'   :None,
                    'sendMail'    :None,
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'1',
                    'name'        :'fred',
                }

        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        expected = kwargs
        self.assertEqual(parseXHRClientRequest(request.POST), expected)

    def test_parseXHRClientRequest_raise_error_if_model_table_mismatch(self):
        kwargs = {
                    'browTabName' :'users_table',
                    'model'       :'folder',
                }
        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        with self.assertRaises(ValueError):
            parseXHRClientRequest(request.POST)

    def test_parseXHRClientRequest_raise_error_if_no_table(self):
        kwargs = {
                    'browTabName' :'',
                    'model'       :'folder',
                }
        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        with self.assertRaises(ValueError):
            parseXHRClientRequest(request.POST)

    def test_parseXHRClientRequest_raise_error_if_unknown_table(self):
        kwargs = {
                    'browTabName' :'TABLE',
                    'model'       :'folder',
                }
        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        with self.assertRaises(ValueError):
            parseXHRClientRequest(request.POST)

    def test_parseXHRClientRequest_if_no_model(self):
        kwargs = {
                    'browTabName' :'users_table',
                }
        ajax_data = DummyXHRrequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        expected = {
                    'browTabName' :'users_table',
                }
        self.assertEqual(parseXHRClientRequest(request.POST), expected)


class Get_namespace_from_dictTest(TestCase):

    def setUp(self):
        self.ns = types.SimpleNamespace(a   = None,
                                        b   = None,
                                        c   = None,
                                        )

    def test_get_namespace_from_dict_1(self):
        d = {'a':1, 'b':2}
        expected = types.SimpleNamespace(a=1, b=2, c= None)
        ns = get_namespace_from_dict(d, self.ns)
        self.assertEqual(ns, expected)

    def test_get_namespace_from_dict_2(self):
        d = {'a':1, 'b':2, 'd':4}
        expected = types.SimpleNamespace(a=1, b=2, c= None)
        ns = get_namespace_from_dict(d, self.ns)
        self.assertEqual(ns, expected)

    def test_get_namespace_from_dict_3(self):
        d = {'a':1, 'b':2}
        expected = types.SimpleNamespace(a=1, b=2, c= None)
        ns = get_namespace_from_dict(d, self.ns, True)
        self.assertEqual(ns, expected)

    def test_get_namespace_from_dict_4(self):
        d = {'a':1, 'b':2, 'd':4}
        expected = types.SimpleNamespace(a=1, b=2, c= None, d= 4)
        ns = get_namespace_from_dict(d, self.ns, True)
        self.assertEqual(ns, expected)


class UserDifferentAttributesTest(TestCase):

    def setUp(self):
        self.user = DummyUser().create_dummy_user()

    def test_get_user_full_name_gives_empty_str(self):
        self.assertEqual(get_user_full_name(self.user), "")

    def test_get_user_full_name_gives_capitelized_names(self):
        user = DummyUser().create_dummy_user(username='AB', first_name='alfa', last_name='beta')
        self.assertEqual(get_user_full_name(user), "Beta Alfa")

    def test_get_user_full_name_gives_stripped_names(self):
        user = DummyUser().create_dummy_user(username='AB', first_name=' alfa ', last_name=' be ta ')
        self.assertEqual(get_user_full_name(user), "Be ta Alfa")

    def test_get_user_flat_No_gives_empty_str(self):
        self.assertEqual(get_user_flat_No(self.user), "")

    def test_get_user_flat_No_gives_proper_value(self):
        flat = DummyFlat().create_dummy_flat(flat_No='11a')
        DummyUser().create_dummy_profile(self.user, flat=flat)
        self.assertEqual(get_user_flat_No(self.user), "11a")

    def test_get_user_is_recognized_gives_empty_str(self):
        self.assertEqual(get_user_is_recognized(self.user), "")

    def test_get_user_is_recognized_gives_proper_value(self):
        DummyUser().create_dummy_profile(self.user, is_recognized=True)
        self.assertEqual(get_user_is_recognized(self.user), True)

    def test_is_staff_only_gives_true(self):
        DummyUser().create_dummy_group(group_name='staff')
        DummyUser().add_dummy_group(self.user, group_name='staff')
        self.assertTrue(is_staff_only(self.user))

    def test_is_staff_only_gives_false_for_enother_group(self):
        DummyUser().create_dummy_group(group_name='STAFF')
        DummyUser().add_dummy_group(self.user, group_name='STAFF')
        self.assertFalse(is_staff_only(self.user))

    def test_is_staff_only_gives_false_for_two_groups(self):
        DummyUser().create_dummy_group(group_name='staff')
        DummyUser().add_dummy_group(self.user, group_name='staff')
        DummyUser().create_dummy_group(group_name='STAFF')
        DummyUser().add_dummy_group(self.user, group_name='STAFF')
        self.assertFalse(is_staff_only(self.user))

    def test_has_group_member(self):
        DummyUser().create_dummy_group(group_name='members')
        DummyUser().add_dummy_group(self.user, group_name='members')
        self.assertTrue(has_group_members(self.user))

    def test_has_group_member_gives_false(self):
        DummyUser().create_dummy_group(group_name='stuff')
        DummyUser().add_dummy_group(self.user, group_name='stuff')
        self.assertFalse(has_group_members(self.user))

    def test_has_group(self):
        DummyUser().create_dummy_group(group_name='members')
        DummyUser().add_dummy_group(self.user, group_name='members')
        self.assertTrue(has_group(self.user, 'members'))

    def test_has_group_gives_false(self):
        self.assertFalse(has_group(self.user, 'members'))

    def test_add_group(self):
        DummyUser().create_dummy_group(group_name='members')
        add_group(self.user, 'members')
        self.assertTrue(has_group(self.user, 'members'))

    def test_add_group_gives_error_if_no_group(self):
        with self.assertRaises(IntegrityError):
            add_group(self.user, 'members')

    def test_remove_group(self):
        DummyUser().create_dummy_group(group_name='members')
        add_group(self.user, 'members')
        self.assertTrue(has_group(self.user, 'members'))
        remove_group(self.user, 'members')
        self.assertFalse(has_group(self.user, 'members'))

    def test_remove_group_gives_false_if_no_group(self):
        remove_group(self.user, 'members')
        self.assertFalse(has_group(self.user, 'members'))


    def test_get_flat_users(self):
        john, paul, george, ringo, freddy = DummyUser().create_dummy_beatles()
        flat_1, flat_2 = DummyUser().set_flats_to_beatles(john, paul, george, ringo, freddy)
        flat_3 = Flat()
        self.assertEqual(get_flat_users(flat_1), [john,])
        self.assertEqual(get_flat_users(flat_2), [paul, george, ringo])
        self.assertEqual(get_flat_users(flat_3), [])
        self.assertEqual(get_flat_users(None), [])
        self.assertEqual(get_flat_users(User()), [])

    def test_has_flat_member(self):
        john, paul, george, ringo, freddy = DummyUser().create_dummy_beatles()
        flat_1, flat_2 = DummyUser().set_flats_to_beatles(john, paul, george, ringo, freddy)
        flat_3 = Flat()
        DummyUser().create_dummy_group(group_name='members')
        DummyUser().add_dummy_group(john, group_name='members')
        self.assertEqual(has_flat_member(flat_1), True)
        self.assertEqual(has_flat_member(flat_2), False)
        self.assertEqual(has_flat_member(flat_3), False)
        self.assertEqual(has_flat_member(None), False)
        self.assertEqual(has_flat_member(User()), False)



class AllFieldsMixinTest(TestCase):
    # Тестуємо клас, базовий для AllFieldsView і AllRecordsAllFieldsView

    def test_attributes(self):
        cls = AllFieldsMixin
        self.assertIsNone(cls.model)
        self.assertEqual(cls.fields, ())
        self.assertEqual(cls.exclude, ())

    def test_val_repr(self):
        cls = AllFieldsMixin()
        self.assertEqual(cls.val_repr(5), 5)
        self.assertEqual(cls.val_repr(5.1), 5.1)
        self.assertEqual(cls.val_repr(5.12), 5.12)
        self.assertEqual(cls.val_repr(5.123), 5.12)
        self.assertEqual(cls.val_repr(5.126), 5.13)
        self.assertEqual(cls.val_repr(5.126, 1), 5.1)
        self.assertEqual(cls.val_repr(0), "")
        self.assertEqual(cls.val_repr("qwe"), "qwe")

    def test_get_field_keys_verbnames_gives_all_fields_for_Flat(self):
        cls = AllFieldsMixin()
        cls.model = Flat
        cls.fields = ()
        cls.exclude = ('id',)
        key_list, verbname_list = cls.get_field_keys_verbnames()
        # Списки мають мати довжину == кількості полів у моделі Flat
        self.assertEqual(len(key_list), 23)
        self.assertEqual(len(verbname_list), 23)
        # id не входить до списку
        self.assertNotIn('id', key_list)
        # Вибіркова перевірка:
        self.assertEqual(key_list[0], "flat_No")
        self.assertEqual(verbname_list[0], "Квартира №")
        self.assertEqual(key_list[5], "room1_S")
        self.assertEqual(verbname_list[5], "кімната")
        self.assertEqual(key_list[22], "listing")
        self.assertEqual(verbname_list[22], "Список")

    def test_get_field_keys_verbnames_gives_some_fields_for_Flat(self):
        cls = AllFieldsMixin()
        cls.model = Flat
        cls.fields = ("flat_No", "room1_S", "listing")
        cls.exclude = ('id',)
        key_list, verbname_list = cls.get_field_keys_verbnames()
        # Списки мають мати довжину == кількості полів у self.fields
        self.assertEqual(len(key_list), 3)
        self.assertEqual(len(verbname_list), 3)
        # id не входить до списку
        self.assertNotIn('id', key_list)
        # Вибіркова перевірка:
        self.assertEqual(key_list[0], "flat_No")
        self.assertEqual(verbname_list[0], "Квартира №")
        self.assertEqual(key_list[1], "room1_S")
        self.assertEqual(verbname_list[1], "кімната")
        self.assertEqual(key_list[2], "listing")
        self.assertEqual(verbname_list[2], "Список")

    def test_get_value_list_gives_proper_values_for_Flat(self):
        cls = AllFieldsMixin()
        cls.model = Flat
        flat = Flat(id=5, flat_No='5', floor_No=1, entrance_No=2)
        flat.save()
        key_list = ("flat_No", "floor_No", "entrance_No")
        value_list = cls.get_value_list(flat, key_list)
        # Списки мають мати довжину
        self.assertEqual(len(value_list), 3)
        # Перевірка значень:
        self.assertEqual(value_list[0], '5')
        self.assertEqual(value_list[1], 1)
        self.assertEqual(value_list[2], 2)

    def test_get_label_value_list_gives_list_of_tuples(self):
        cls = AllFieldsMixin()
        key_list = ("flat_No", "floor_No", "entrance_No")
        value_list = ('1', 2, 3)
        kv_list = cls.get_label_value_list(key_list, value_list)

        # Список має мати довжину:
        self.assertEqual(len(kv_list), 3)
        # Перевірка значень:
        self.assertEqual(kv_list[0], ("flat_No", '1'))
        self.assertEqual(kv_list[1], ("floor_No", 2))
        self.assertEqual(kv_list[2], ("entrance_No", 3))


class TestTransliterate(TestCase):

    def setUp(self):
        self.examples_KMU = [
            ('Алушта      ', 'Alushta'),
            ('Борщагівка  ', 'Borshchahivka'),
            ('Вишгород    ', 'Vyshhorod'),
            ('Гадяч       ', 'Hadiach'),
            ('Згорани     ', 'Zghorany'),
            ('Ґалаґан     ', 'Galagan'),
            ('Дон         ', 'Don'),
            ('Рівне       ', 'Rivne'),
            ('Єнакієве    ', 'Yenakiieve'),
            ('Наєнко      ', 'Naienko'),
            ('Житомир     ', 'Zhytomyr'),
            ('Закарпаття  ', 'Zakarpattia'),
            ('Медвин      ', 'Medvyn'),
            ('Іршава      ', 'Irshava'),
            ('Їжакевич    ', 'Yizhakevych'),
            ('Кадіївка    ', 'Kadiivka'),
            ('Йосипівка   ', 'Yosypivka'),
            ('Стрий       ', 'Stryi'),
            ('Київ        ', 'Kyiv'),
            ('Лебедин     ', 'Lebedyn'),
            ('Миколаїв    ', 'Mykolaiv'),
            ('Ніжин       ', 'Nizhyn'),
            ('Одеса       ', 'Odesa'),
            ('Полтава     ', 'Poltava'),
            ('Ромни       ', 'Romny'),
            ('Суми        ', 'Sumy'),
            ('Тетерів     ', 'Teteriv'),
            ('Ужгород     ', 'Uzhhorod'),
            ('Фастів      ', 'Fastiv'),
            ('Харків      ', 'Kharkiv'),
            ('Біла Церква ', 'Bila Tserkva'),
            ('Чернівці    ', 'Chernivtsi'),
            ('Шостка      ', 'Shostka'),
            ('Гоща        ', 'Hoshcha'),
            ('Юрій        ', 'Yurii'),
            ('Крюківка    ', 'Kriukivka'),
            ('Яготин      ', 'Yahotyn'),
            ('Ічня        ', 'Ichnia'),
        ]
        self.examples = [
            ('йцукенгшщзхї',    'ytsukenhshshchzkhi'),
            ('ЙЦУКЕНГШЩЗХЇ',    'YTsUKENHShShchZKhI'),
            ('фівапролджє',     'fivaproldzhie'),
            ('ФІВАПРОЛДЖЄ',     'FIVAPROLDZhIe'),
            ('ячсмитьбюґ',      'yachsmytbiug'),
            ('ЯЧСМИТЬБЮҐ',      'YaChSMYTBIuG'),
            ('"`1234567890-=',  '"`1234567890-='),
            ('~!@#$%^&*()_+',   '~!@#$%^&*()_+'),
            (";:',<.>/?|",       ";:',<.>/?|"),
            ('ЪъЫыЭэ',          '______'),
        ]

    def test_KMU_examples(self):
        for e in self.examples_KMU:
            ukr = e[0].strip()
            eng = e[1]
            trans = transliterate(ukr)
            self.assertEqual(trans, eng)

    def test_other_examples(self):
        for e in self.examples:
            ukr = e[0].strip()
            eng = e[1]
            trans = transliterate(ukr)
            self.assertEqual(trans, eng)


class Get_thumbnail_url_path_Test(TestCase):

    def test_get_miniature_path(self):
        user = DummyUser().create_dummy_user()
        picture_path=os.path.join("koopsite","tests","profile_image.jpg")
        mini_path = get_miniature_path(picture_path)
        self.assertEqual(mini_path, 'koopsite\\tests\\profile_image_30x24.jpg')
        mini_path = get_miniature_path(picture_path, "200x100")
        self.assertEqual(mini_path, 'koopsite\\tests\\profile_image_200x100.jpg')

    # @skip
    def test_thumbnail_for_file(self):
        user = DummyUser().create_dummy_user()
        picture_path="koopsite/tests/profile_image.jpg"
        DummyUser().create_dummy_profile(user, picture_path=picture_path)
        picture = user.userprofile.picture
        expected_url = '/media/profile_images/1_30x24.jpg'
        expected_path = os.path.join(MEDIA_ROOT, r"profile_images\1_30x24.jpg")
        mini_url, mini_path = get_thumbnail_url_path(picture)
        self.assertEqual(mini_url, expected_url)
        self.assertEqual(mini_path, expected_path)

        expected_url = '/media/profile_images/1_200x100.jpg'
        expected_path = os.path.join(MEDIA_ROOT, r"profile_images\1_200x100.jpg")
        mini_url, mini_path = get_thumbnail_url_path(picture, "200x100")
        self.assertEqual(mini_url, expected_url)
        self.assertEqual(mini_path, expected_path)

        os.remove('media/profile_images/1.jpg')
        os.remove('media/profile_images/1_30x24.jpg')
        os.remove('media/profile_images/1_200x100.jpg')

    # @skip
    def test_thumbnail_for_path(self):
        user = DummyUser().create_dummy_user()
        picture_path="koopsite/tests/profile_image.jpg"
        mini_url = get_thumbnail_url_path(picture_path)[0]
        self.assertEqual(mini_url, 'koopsite/tests/profile_image_30x24.jpg')
        mini_url = get_thumbnail_url_path(picture_path, "200x100")[0]
        self.assertEqual(mini_url, 'koopsite/tests/profile_image_200x100.jpg')
        os.remove('koopsite/tests/profile_image_30x24.jpg')
        os.remove('koopsite/tests/profile_image_200x100.jpg')

    # @skip
    def test_thumbnail_for_file_3(self):
        user = DummyUser().create_dummy_user()
        # picture_path="koopsite/tests/profile_image_3.jpg"
        picture_path=os.path.join("koopsite","tests","profile_image_3.jpg")
        DummyUser().create_dummy_profile(user, picture_path=picture_path)
        picture = user.userprofile.picture
        expected_url = '/media/profile_images/1_30x24.jpg'
        expected_path = os.path.join(MEDIA_ROOT, "profile_images", "1_30x24.jpg")
        mini_url, mini_path = get_thumbnail_url_path(picture)
        self.assertEqual(mini_url, expected_url)
        self.assertEqual(mini_path, expected_path)

        image = Image.open(expected_path)
        size = image.size
        self.assertEqual(size, (30, 16))
        image.close()

        os.remove(os.path.join('media','profile_images','1.jpg'))
        os.remove(os.path.join('media','profile_images','1_30x24.jpg'))


class CheckPathMatchMediaPatternTest(TestCase):

    def test_default_pattern(self):
        path = os.path.join('profile_images', 'XYZ')

        path = os.path.join('profile_images', '1.jpg')
        self.assertTrue(CheckPathMatchMediaPattern(path))

        path = os.path.join('profile_images', '1_4mYRZqN.jpg')
        self.assertTrue(CheckPathMatchMediaPattern(path))

        path = os.path.join('profile_images', '13_HGTfooq_200x200.jpg')
        self.assertTrue(CheckPathMatchMediaPattern(path))

        path = os.path.join('profile_images', '1_30x24.jpg')
        self.assertTrue(CheckPathMatchMediaPattern(path))

        path = os.path.join('profile_images', '111111.jpg')
        self.assertTrue(CheckPathMatchMediaPattern(path))

        path = os.path.join('profile_images', '1_.jpg')
        self.assertTrue(CheckPathMatchMediaPattern(path))

        path = os.path.join('profile_images', 'a1.jpg')
        self.assertFalse(CheckPathMatchMediaPattern(path))

        path = os.path.join('profile_images', '1.jpeg')
        self.assertFalse(CheckPathMatchMediaPattern(path))

        path = '1.jpg'
        self.assertFalse(CheckPathMatchMediaPattern(path))

        path = 'a1.jpg'
        self.assertFalse(CheckPathMatchMediaPattern(path))

        path = '111.jpeg'
        self.assertFalse(CheckPathMatchMediaPattern(path))

