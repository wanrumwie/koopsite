from unittest.case import skip
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.timezone import now
from flats.tests.test_base import DummyFlat
from koopsite.forms import UserRegistrationForm, UserPersonDataForm, \
    UserPermsFullForm, UserPermsActivateForm, ProfileFullForm, \
    ProfilePermForm, ProfilePersonDataForm, Human_Check, \
    ProfileRegistrationForm, get_readonly_disabled_widget_type_list
from koopsite.functions import has_group, dict_print
from koopsite.models import UserProfile
from koopsite.tests.test_base import DummyUser


class UserRegistrationFormTest(TestCase):

    def setUp(self):
        self.cls_form = UserRegistrationForm
        self.cls_model = User
        self.expected_meta_fields = (
                'username',
                'first_name', 'last_name', 'email',
                 )
        self.expected_form_fields = (
                'username',
                'first_name', 'last_name', 'email',
                'password1', 'password2',
                 )
        self.initial_data = {
            'username': 'dummy_user',
            'password1': 'secret',
            'password2': 'secret',
            }
        self.empty_data = {}.fromkeys(self.expected_form_fields)

    def test_form_attributes(self):
        form = self.cls_form
        form_fields = tuple(getattr(form, 'base_fields').keys())
        self.assertEqual(form.required_css_class, 'required')
        self.assertEqual(form.error_css_class   , 'error')
        self.assertEqual(form.Meta.model, self.cls_model)
        self.assertEqual(form.Meta.fields, self.expected_meta_fields)
        self.assertEqual(form_fields, self.expected_form_fields)

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertIn('Ім&#39;я користувача', form.as_p())
        self.assertIn("Ім&#39;я", form.as_p())
        self.assertIn("Прізвище", form.as_p())
        self.assertIn('Email адреса', form.as_p())
        self.assertIn('Пароль', form.as_p())
        self.assertIn('Підтвердження пароля', form.as_p())

    def test_form_validation_for_blank_fields(self):
        form = self.cls_form(data=self.empty_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ["Це поле обов'язкове."])
        self.assertEqual(form.errors['password1'], ["Це поле обов'язкове."])
        self.assertEqual(form.errors['password2'], ["Це поле обов'язкове."])

    def test_form_validation_for_duplicate_fields(self):
        DummyUser().create_dummy_user(username='dummy_user')
        # Передаємо у форму неунікальне значення поля:
        data = {'username': "dummy_user"}
        form = self.cls_form(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ["Користувач з таким ім'ям вже існує."])

    def test_form_save(self):
        data = self.initial_data
        form = self.cls_form(data=data)
        new_record = form.save()
        self.assertEqual(new_record, self.cls_model.objects.last())


class UserPersonDataFormTest(TestCase):

    def setUp(self):
        self.cls_form = UserPersonDataForm
        self.cls_model = User
        self.expected_meta_fields = (
                  'first_name', 'last_name', 'email',
                 )
        self.expected_form_fields = (
                  'first_name', 'last_name', 'email',
                 )

    def test_form_attributes(self):
        form = self.cls_form
        form_fields = tuple(getattr(form, 'base_fields').keys())
        self.assertEqual(form.required_css_class, 'required')
        self.assertEqual(form.error_css_class   , 'error')
        self.assertEqual(form.Meta.model, self.cls_model)
        self.assertEqual(form.Meta.fields, self.expected_meta_fields)
        self.assertEqual(form_fields, self.expected_form_fields)

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertNotIn('Логін', form.as_p())
        self.assertIn("Ім&#39;я", form.as_p())
        self.assertIn("Прізвище", form.as_p())
        self.assertNotIn('Пароль', form.as_p())
        self.assertIn('Email адреса', form.as_p())
        self.assertNotIn('Активний', form.as_p())
        self.assertNotIn('У штаті', form.as_p())
        self.assertNotIn('Дата створення', form.as_p())
        self.assertNotIn('Дата попер.входу', form.as_p())
        self.assertNotIn('Групи:', form.as_p())


class UserPermsFullFormTest(TestCase):

    def setUp(self):
        self.cls_form = UserPermsFullForm
        self.cls_model = User
        self.expected_readonly_fields = (
                                        'first_name', 'last_name',
                                        'date_joined', 'last_login',
                                        )
        self.expected_meta_fields = (
                  # 'username',
                  'first_name', 'last_name',
                  'date_joined', 'last_login',
                  'is_active', 'is_staff',
                  'groups',
                 )
        self.expected_form_fields = (
                  # 'username',
                  'first_name', 'last_name',
                  'date_joined', 'last_login',
                  'is_active', 'is_staff',
                  'groups',
                  # 'has_perm_member',
                 )

    def test_form_attributes(self):
        form = self.cls_form
        form_fields = tuple(getattr(form, 'base_fields').keys())
        # self.assertEqual(form.required_css_class, 'required')
        # self.assertEqual(form.error_css_class   , 'error')
        self.assertEqual(form.READONLY_FIELDS, self.expected_readonly_fields)
        self.assertEqual(form.Meta.model, self.cls_model)
        self.assertEqual(form.Meta.fields, self.expected_meta_fields)
        self.assertEqual(form_fields, self.expected_form_fields)

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertNotIn("Ім&#39;я користувача", form.as_p())
        self.assertIn("Ім&#39;я", form.as_p())
        self.assertIn("Прізвище", form.as_p())
        self.assertNotIn('Пароль', form.as_p())
        self.assertNotIn('e-mail', form.as_p())
        self.assertIn('Активний', form.as_p())
        self.assertIn('Статус персоналу', form.as_p())
        self.assertIn('Дата приєднання', form.as_p())
        self.assertIn('Останній вхід', form.as_p())
        self.assertIn('Групи:', form.as_p())
        self.assertNotIn('Доступ члена коопертиву', form.as_p())

    def test_init(self):
        form = self.cls_form()
        for field in form.READONLY_FIELDS:
            widget = form.fields[field].widget
            if widget.__class__.__name__ in get_readonly_disabled_widget_type_list():
                self.assertEqual(widget.attrs['disabled'], 'disabled')
            else:
                self.assertEqual(widget.attrs['readonly'], 'readonly')

    def test_init_clear_help_texr(self):
        form = self.cls_form()
        for field in self.expected_form_fields:
            self.assertEqual(form.fields[field].help_text, "")



class UserPermsActivateFormTest(TestCase):

    def setUp(self):
        self.cls_form = UserPermsActivateForm
        self.cls_model = User
        self.expected_readonly_fields = (
                                        'first_name', 'last_name',
                                        'date_joined', 'last_login',
                                        )
        self.expected_meta_fields = (
                  # 'username',
                  'first_name', 'last_name',
                  'date_joined',
                  'is_active',
                 )
        self.expected_form_fields = (
                  # 'username',
                  'first_name', 'last_name',
                  'date_joined',
                  'is_active',
                  'has_perm_member',
                 )

    def test_form_attributes(self):
        form = self.cls_form
        form_fields = tuple(getattr(form, 'base_fields').keys())
        # self.assertEqual(form.required_css_class, 'required')
        # self.assertEqual(form.error_css_class   , 'error')
        self.assertEqual(form.READONLY_FIELDS, self.expected_readonly_fields)
        self.assertEqual(form.Meta.model, self.cls_model)
        self.assertEqual(form.Meta.fields, self.expected_meta_fields)
        self.assertEqual(form_fields, self.expected_form_fields)

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertNotIn('Ім&#39;я користувача', form.as_p())
        self.assertIn("Ім&#39;я", form.as_p())
        self.assertIn("Прізвище", form.as_p())
        self.assertNotIn('Пароль', form.as_p())
        self.assertNotIn('e-mail', form.as_p())
        self.assertIn('Активний', form.as_p())
        self.assertNotIn('У штаті', form.as_p())
        self.assertIn('Дата приєднання', form.as_p())
        self.assertNotIn('Останній вхід', form.as_p())
        self.assertNotIn('Групи:', form.as_p())
        self.assertIn('Доступ члена коопертиву', form.as_p())

    def test_init_and_get_is_member(self):
        form = self.cls_form()

        # empty form:
        self.assertFalse(form.is_member)
        self.assertFalse(form.fields['has_perm_member'].initial)

        dummy_user = DummyUser().create_dummy_user(username='dummy_user')

        # form with initial data
        initial_data = {
            'username': 'dummy_user',
            }
        form = self.cls_form(data=initial_data)
        self.assertFalse(form.is_member)
        self.assertFalse(form.fields['has_perm_member'].initial)

        # form with initial user instance:

        DummyUser().create_dummy_group(group_name='members')
        DummyUser().add_dummy_group(dummy_user, group_name='members')
        self.assertTrue(has_group(dummy_user, 'members'))
        form = self.cls_form(instance=dummy_user)
        self.assertTrue(form.is_member)
        self.assertEqual(form.fields['has_perm_member'].initial, form.is_member)

    def test_form_save(self):
        dummy_user = DummyUser().create_dummy_user(username='dummy_user')
        DummyUser().create_dummy_group(group_name='members')
        self.assertFalse(has_group(dummy_user, 'members'))

        # Створюємо форму з instance і data
        # (заповнюємо також required fields, бо super().save не зможе зберегти)
        data = {
            'username': 'dummy_userQQQ',
            'has_perm_member': True,
            'date_joined' : now()
            }
        form = self.cls_form(instance=dummy_user, data=data)
        saved_user = form.save()
        # Чи збережено?
        self.assertEqual(saved_user, User.objects.last())
        # Чи змінилось значення поля?
        self.assertTrue(has_group(dummy_user, 'members'))

        # Створюємо форму з user + додаткові data
        data = {
            'username': 'dummy_user',
            'has_perm_member': False,
            'date_joined' : now()
            }
        form = self.cls_form(instance=dummy_user, data=data)
        saved_user = form.save()
        # Чи збережено?
        self.assertEqual(saved_user, User.objects.last())
        # Чи змінилось значення поля?
        self.assertFalse(has_group(dummy_user, 'members'))




class ProfileFullFormTest(TestCase):

    def setUp(self):
        self.cls_form = ProfileFullForm
        self.cls_model = UserProfile
        self.expected_meta_fields = ('is_recognized', 'flat', 'picture')
        self.expected_form_fields = ('is_recognized', 'flat', 'picture')
        self.initial_data = {
            'flat': '1',
            }
        self.empty_data = {}.fromkeys(self.expected_meta_fields)
        user = DummyUser().create_dummy_user(username='dummy_user')
        flat = DummyFlat().create_dummy_flat(id=1, flat_No='25')
        self.profile = DummyUser().create_dummy_profile(user, flat=flat, is_recognized=True)

    def test_form_attributes(self):
        form = self.cls_form
        form_fields = tuple(getattr(form, 'base_fields').keys())
        # self.assertEqual(form.required_css_class, 'required')
        # self.assertEqual(form.error_css_class   , 'error')
        self.assertEqual(form.Meta.model, self.cls_model)
        self.assertEqual(form.Meta.fields, self.expected_meta_fields)
        self.assertEqual(form_fields, self.expected_form_fields)

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertIn('Підтверджений', form.as_p())
        self.assertIn("Квартира", form.as_p())
        self.assertIn("Аватар", form.as_p())

    def test_form_renders_values(self):
        form = self.cls_form(instance=self.profile)
        self.assertIn('option value="1" selected="selected">25', form.as_p())

    def test_form_save(self):
        form = self.cls_form(instance=self.profile, data=self.initial_data)
        new_record = form.save()
        self.assertEqual(new_record, self.cls_model.objects.last())


class ProfilePermFormTest(TestCase):

    def setUp(self):
        self.cls_form = ProfilePermForm
        self.cls_model = UserProfile
        self.expected_readonly_fields = ('flat',)
        self.expected_meta_fields = ('is_recognized', 'flat')
        self.expected_form_fields = ('is_recognized', 'flat')

    def test_form_attributes(self):
        form = self.cls_form
        form_fields = tuple(getattr(form, 'base_fields').keys())
        # self.assertEqual(form.required_css_class, 'required')
        # self.assertEqual(form.error_css_class   , 'error')
        self.assertEqual(form.READONLY_FIELDS, self.expected_readonly_fields)
        self.assertEqual(form.Meta.model, self.cls_model)
        self.assertEqual(form.Meta.fields, self.expected_meta_fields)
        self.assertEqual(form_fields, self.expected_form_fields)

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertIn('Підтверджений', form.as_p())
        self.assertIn("Квартира", form.as_p())
        self.assertNotIn("Аватар", form.as_p())

    def test_init(self):
        form = self.cls_form()
        for field in form.READONLY_FIELDS:
            widget = form.fields[field].widget
            if widget.__class__.__name__ in get_readonly_disabled_widget_type_list():
                self.assertEqual(widget.attrs['disabled'], 'disabled')
            else:
                self.assertEqual(widget.attrs['readonly'], 'readonly')



class ProfilePersonDataFormTest(TestCase):

    def setUp(self):
        self.cls_form = ProfilePersonDataForm
        self.cls_model = UserProfile
        self.expected_meta_fields = ('flat', 'picture')
        # self.expected_form_fields = ()

    def test_form_attributes(self):
        form = self.cls_form
        form_fields = tuple(getattr(form, 'declared_fields').keys())
        # self.assertEqual(form.required_css_class, 'required')
        # self.assertEqual(form.error_css_class   , 'error')
        # self.assertEqual(form.READONLY_FIELDS   , ('flat', ))
        self.assertEqual(form.Meta.model, self.cls_model)
        self.assertEqual(form.Meta.fields, self.expected_meta_fields)
        # self.assertEqual(sorted(form_fields), sorted(self.expected_form_fields))

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertNotIn('Підтверджений', form.as_p())
        self.assertIn("Квартира", form.as_p())
        self.assertIn("Аватар", form.as_p())


class Human_CheckTest(TestCase):

    def setUp(self):
        self.expected_taskPattern = "Видаліть із цієї стрічки %s слово"
        self.expected_numerals = {
           -1: "останнє",
            0: "перше",
            1: "друге",
            2: "третє",
            3: "четверте",
            4: "п'яте",
            5: "шосте",
        }

    def test_attributes(self):
        self.assertEqual(Human_Check.taskPattern, self.expected_taskPattern)
        self.assertEqual(Human_Check.numerals, self.expected_numerals)

    def test_init(self):
        # Випадкові значення:
        for i in range(100):
            hc = Human_Check()
            self.assertEqual(hc.task, hc.taskPattern % hc.numerals[hc.taskNo])
            self.assertIn(hc.taskNo, list(range(-1, 6)))

        # Фіксовані значення:
        for i in range(-1, 6):
            hc = Human_Check(i)
            self.assertEqual(hc.task, hc.taskPattern % hc.numerals[hc.taskNo])
            self.assertEqual(hc.taskNo, i)

    def test_validator(self):
        # Фіксовані значення:
        # Готуємо правильну відповідь:
        for i in range(-1, 6):
            hc = Human_Check(i)
            twords = hc.task.split()
            twords.pop(hc.taskNo)
            answer = ' '.join(twords)
            hc.validator(answer)    # помилки не повинно бути

        # Різні варіанти неправильної відповіді:
        # без змін:
        for i in range(-1, 6):
            hc = Human_Check(i)
            answer = hc.task
            with self.assertRaises(ValidationError):
                hc.validator(answer)

        # неправильні зміни:
        for i in range(-1, 6):
            hc = Human_Check(i)
            twords = hc.task.split()
            n = i + 1
            if n > 5: n = 0
            twords.pop(n)
            answer = ' '.join(twords)
            with self.assertRaises(ValidationError):
                hc.validator(answer)

        # порожній рядок:
        for i in range(-1, 6):
            hc = Human_Check(i)
            answer = ''
            with self.assertRaises(ValidationError):
                hc.validator(answer)

        # абракадабра:
        for i in range(-1, 6):
            hc = Human_Check(i)
            answer = 'абракадабра'
            with self.assertRaises(ValidationError):
                hc.validator(answer)

        # Режим, коли б-я відповідь - правильна:
        Human_Check.if_view_test = True
        for i in range(-1, 6):
            hc = Human_Check(i)
            twords = hc.task.split()
            twords.pop(hc.taskNo)
            answer = 'абракадабра'
            hc.validator(answer)    # помилки не повинно бути
        Human_Check.if_view_test = False


class ProfileRegistrationFormTest(TestCase):

    def setUp(self):
        self.cls_form = ProfileRegistrationForm
        self.cls_model = UserProfile
        self.expected_meta_fields = ('flat', 'picture')
        # self.expected_form_fields = ('human_check',)

    def test_form_attributes(self):
        form = self.cls_form
        form_fields = tuple(getattr(form, 'declared_fields').keys())
        self.assertEqual(form.required_css_class, 'required')
        self.assertEqual(form.error_css_class   , 'error')
        # self.assertEqual(form.READONLY_FIELDS   , ('flat', ))
        self.assertIsInstance(form.hc, Human_Check)
        self.assertEqual(form.Meta.model, self.cls_model)
        self.assertEqual(form.Meta.fields, self.expected_meta_fields)
        # self.assertEqual(sorted(form_fields), sorted(self.expected_form_fields))

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertNotIn('Підтверджений', form.as_p())
        self.assertIn("Квартира", form.as_p())
        self.assertIn("Аватар", form.as_p())
        self.assertIn("Доведіть, що Ви - людина", form.as_p())

    def test_form_validation_for_blank_fields(self):
        form = self.cls_form(data={'human_check': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['human_check'], ["Це поле обов'язкове."])

    def test_form_validation_for_non_human(self):
        form = self.cls_form(data={'human_check': 'abrakadabra'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['human_check'], ["Помилка!"])

    # TODO-не вдалося протестувати form для неправильного email
    @skip
    def test_form_validation_for_invalid_email(self):
        form = self.cls_form(data={'email': 'ab'})
        print(form.as_p())
        dict_print(form.errors, 'form.errors')
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ["Помилка!"])

    # TODO-не вдалося протестувати form для неправильного малюнка
    @skip
    def test_form_validation_for_invalid_picture(self):
        Human_Check.if_view_test = True
        file = SimpleUploadedFile("file.txt", b"file_content")
        form = self.cls_form(data={'human_check': 'abrakadabra',
                                   'file': file})
        self.assertFalse(form.is_valid())
        dict_print(form.errors, 'form.errors')
        self.assertEqual(form.errors['picture'], ["Завантажте правильний малюнок. Файл, який ви завантажили, не є малюнком, або є зіпсованим малюнком."])
        Human_Check.if_view_test = False



