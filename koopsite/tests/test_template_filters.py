import os
from django.contrib.auth.models import User
from django.test import TestCase
from flats.models import Flat
from flats.tests.test_base import DummyFlat
from folders.models import Folder
from koopsite.templatetags.koop_template_filters import get_at_index, get_item_by_key, range_of, model_name, \
    user_full_name, user_flat_No, thumbnail, icon_yes_no_unknown, flat_user_CSS_class, has_member_perms
from koopsite.tests.test_base import DummyUser

"""
Необхідність перевірки фільтрів виникає тому,
що Django не показує звичайних Python помилок у фільтрах,
бо вони працюють при рендерінгу шаблонів, коли, очевидно,
умови перевірки менш жорсткі, ніж Python.
Разом з тим, при тестуванні з доп. Selenium ці помилки виявляються.
Наприклад:
@register.filter()
def get_at_index(list, index):
    # Фільтр для отримання елемента списку за його індексом
    return list[index]


"""

class TemplateFiltersTest(TestCase):

    def test_get_at_index(self):
        list = [0,1,2,3]
        self.assertEqual(get_at_index(list, 0), 0)
        self.assertEqual(get_at_index('0123', 3), '3')
        self.assertIsNone(get_at_index(1234, 0))
        self.assertIsNone(get_at_index(list, 4))

    def test_get_item_by_key(self):
        d = {'1': 1, '2': 2}
        self.assertEqual(get_item_by_key(d, '1'), 1)
        self.assertIsNone(get_item_by_key(d, '3'))
        self.assertIsNone(get_item_by_key(d, 1))
        self.assertIsNone(get_item_by_key((1,2), 1))

    def test_range_of(self):
        self.assertEqual(range_of(1), range(1))
        self.assertEqual(range_of(-2), range(-2))
        self.assertIsNone(range_of((1,)))

    def test_model_name(self):
        self.assertEqual(model_name(Folder), "folder")
        self.assertEqual(model_name(Folder()), "folder")

    def test_user_full_name(self):
        user = DummyUser().create_dummy_user(first_name="ringo", last_name="starr")
        self.assertEqual(user_full_name(user), "Starr Ringo")

    def test_user_flat_No(self):
        user = DummyUser().create_dummy_user()
        flat = DummyFlat().create_dummy_flat(flat_No="55")
        DummyUser().create_dummy_profile(user, flat=flat)
        self.assertEqual(user_flat_No(user), "55")

    def test_thumbnail_for_file(self):
        user = DummyUser().create_dummy_user()
        picture_path = "koopsite/tests/profile_image.jpg"
        DummyUser().create_dummy_profile(user, picture_path=picture_path)
        mini_url = thumbnail(user.userprofile.picture)
        self.assertEqual(mini_url, '/media/profile_images/1_30x24.jpg')
        mini_url = thumbnail(user.userprofile.picture, "200x100")
        self.assertEqual(mini_url, '/media/profile_images/1_200x100.jpg')
        os.remove('media/profile_images/1.jpg')
        os.remove('media/profile_images/1_30x24.jpg')
        os.remove('media/profile_images/1_200x100.jpg')

    def test_thumbnail_for_path(self):
        user = DummyUser().create_dummy_user()
        picture_path = "koopsite/tests/profile_image.jpg"
        mini_url = thumbnail(picture_path)
        self.assertEqual(mini_url, 'koopsite/tests/profile_image_30x24.jpg')
        mini_url = thumbnail(picture_path, "200x100")
        self.assertEqual(mini_url, 'koopsite/tests/profile_image_200x100.jpg')
        os.remove('koopsite/tests/profile_image_30x24.jpg')
        os.remove('koopsite/tests/profile_image_200x100.jpg')

    def test_icon_yes_no_unknown(self):
        self.assertEqual(icon_yes_no_unknown(True),  'admin/img/icon-yes.gif')
        self.assertEqual(icon_yes_no_unknown(False), 'admin/img/icon-no.gif')
        self.assertEqual(icon_yes_no_unknown(None),  'admin/img/icon-unknown.gif')


    def test_flat_user_CSS_class(self):
        john, paul, george, ringo, freddy = DummyUser().create_dummy_beatles()
        flat_1, flat_2 = DummyUser().set_flats_to_beatles(john, paul, george, ringo, freddy)
        flat_3 = Flat()
        DummyUser().create_dummy_group(group_name='members')
        DummyUser().add_dummy_group(john, group_name='members')
        self.assertEqual(flat_user_CSS_class(flat_1), "flat-has-member")
        self.assertEqual(flat_user_CSS_class(flat_2), "flat-has-users")
        self.assertEqual(flat_user_CSS_class(flat_3), "")
        self.assertEqual(flat_user_CSS_class(None), "")
        self.assertEqual(flat_user_CSS_class(User()), "")

    def test_has_members_perms(self):
        john, paul, george, ringo, freddy = DummyUser().create_dummy_beatles()
        DummyUser().create_dummy_group(group_name='members')
        DummyUser().add_dummy_group(john, group_name='members')
        self.assertTrue(has_member_perms(john))
        self.assertFalse(has_member_perms(paul))
