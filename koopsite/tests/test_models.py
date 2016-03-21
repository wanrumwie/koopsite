import os
from unittest.case import skip
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.test import TestCase
from PIL import Image
from flats.tests.test_base import DummyFlat
from functional_tests.koopsite.ft_base import get_test_files_cwd, create_dummy_miniature_file
from koopsite.functions import get_miniature_path
from koopsite.models import UserProfile
from koopsite.tests.test_base import DummyUser


class UserProfileModelTest(TestCase):

    # @skip
    def test_get_absolute_url(self):
        user = DummyUser().create_dummy_user(id=2)
        profile = DummyUser().create_dummy_profile(user, is_recognized=True)
        expected = reverse('adm-users-profile', kwargs={'pk': 2})
        self.assertEqual(profile.get_absolute_url(), expected)

    # @skip
    def test_Meta(self):
        self.assertEqual(UserProfile._meta.verbose_name, ('профіль користувача'))
        self.assertEqual(UserProfile._meta.verbose_name_plural, ('профілі користувачів'))
        self.assertEqual(UserProfile._meta.permissions, (
                        ('activate_account', 'Can activate/deactivate account'),
                        ('view_userprofile', 'Can view user profile'),
                        ))

    # @skip
    def test_empty_user_gives_error(self):
        p = UserProfile()
        with self.assertRaises(IntegrityError):
            p.save()

    @skip
    def test_saving_and_retrieving_files(self):
        user = DummyUser().create_dummy_user()
        file = SimpleUploadedFile("file.txt", b"file_content")
        expected = file.read()
        DummyUser().create_dummy_profile(user, picture=file)
        saved_profile = UserProfile.objects.first()
        # Вмісти збереженого файда і первинного співпадають?
        self.assertEqual(saved_profile.picture.read(), expected)
        # Чи правильний фактичний шлях до файла
        basename = os.path.basename(saved_profile.picture.path)
        self.assertEqual(basename, "1.jpg")
        # Видляємо з диска (бо файл по-чесному записався в /media/profile_images/1.jpg)
        saved_profile.picture.delete()


class UserProfileModelTest_resize_save_image(TestCase):

    def setUp(self):
        # Для прикладу беремо цей файл, з якого створимо мініатюру:
        self.full_path, \
        self.mini_path, \
        self.uploaded_big_file, \
        self.expected_mini_content \
            = create_dummy_miniature_file('example.jpg')

    def tearDown(self):
        # Видаляємо створений міні-файл
        os.unlink(self.mini_path)
        super().tearDown()

    # @skip
    def test_save_file_create_profile(self):
        user = DummyUser().create_dummy_user()

        # Створюємо профіль,  у полі picture вибираємо великий файл:
        DummyUser().create_dummy_profile(user, picture=self.uploaded_big_file)
        saved_profile = UserProfile.objects.first()
        # Вмісти збереженого файла і первинного мінімізованого до 200*200 співпадають?
        self.assertEqual(saved_profile.picture.read(), self.expected_mini_content)
        # Чи правильний фактичний шлях до файла
        basename = os.path.basename(saved_profile.picture.path)
        self.assertEqual(basename, "1.jpg")

        # Видляємо з диска (бо файл по-чесному записався в /media/profile_images/1.jpg)
        saved_profile.picture.delete()

    # @skip
    def test_save_file_update_profile_but_not_file(self):
        user = DummyUser().create_dummy_user()

        # Спочатку повторимо всі операції по створенню профілю:
        # Створюємо профіль,  у полі picture вибираємо великий файл:
        DummyUser().create_dummy_profile(user, picture=self.uploaded_big_file)

        profile = user.userprofile
        profile_id = profile.id

        # Тепер змінимо у профілі якесь поле (але не picture!) і збережемо:
        flat = DummyFlat().create_dummy_flat(flat_No='55', id=155)
        profile.flat = flat
        profile.save()
        saved_profile = UserProfile.objects.get(id=profile_id)

        # Вмісти збереженого файла і первинного мінімізованого до 200*200 співпадають?
        self.assertEqual(saved_profile.picture.read(), self.expected_mini_content)
        # Чи правильний фактичний шлях до файла
        basename = os.path.basename(saved_profile.picture.path)
        self.assertEqual(basename, "1.jpg")

        # Видляємо з диска (бо файл по-чесному записався в /media/profile_images/1.jpg)
        saved_profile.picture.delete()

    def test_save_file_update_profile_just_file(self):
        user = DummyUser().create_dummy_user()

        # Спочатку повторимо всі операції по створенню профілю:
        # Створюємо профіль,  у полі picture вибираємо великий файл:
        DummyUser().create_dummy_profile(user, picture=self.uploaded_big_file)

        profile = user.userprofile
        profile_id = profile.id
        saved_file_path = profile.picture.path

        # Тепер приготуємо інший файл:
        # Для прикладу беремо цей файл, з якого створимо мініатюру:
        full_path_2, \
        mini_path_2, \
        uploaded_big_file_2, \
        expected_mini_content_2 \
            = create_dummy_miniature_file('example_2.jpg')

        # Тепер змінимо у профілі поле picture і збережемо:
        profile.picture.name = 'example_2.jpg'
        profile.picture.file = uploaded_big_file_2
        profile.save()
        saved_profile = UserProfile.objects.get(id=profile_id)

        # Вмісти збереженого файла і другого мінімізованого до 200*200 співпадають?
        self.assertEqual(saved_profile.picture.read(), expected_mini_content_2)
        # Чи правильний фактичний шлях до файла
        basename = os.path.basename(saved_profile.picture.path)
        # self.assertEqual(basename, "1.jpg")

        # Видляємо з диска (бо файл по-чесному записався в /media/profile_images/1.jpg)
        saved_profile.picture.delete()

        # Видаляємо створений міні-файл
        os.unlink(mini_path_2)
        # Видаляємо перший файл
        os.unlink(saved_file_path)
