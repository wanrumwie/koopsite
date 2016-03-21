from random import randrange
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from koopsite.functions import has_group_members, \
                                add_group, remove_group
from koopsite.models import UserProfile


def get_readonly_disabled_widget_type_list():
    """
    Повертає список типів віджетів, які не мають властивості readonly,
    тому їх при потребі потрібно блокувати
    встановленням атрибуту disabled
    """
    readonly_disabled_widget_type_list = [
        'Select',
        'SelectMultiple',
        'NullBooleanSelect',
        # 'RadioSelect',
        'SelectDateWidget',
        ]
    return readonly_disabled_widget_type_list

def set_readonly_widget_attrs(fields, readonly_fields):
    """
    Встановлення полям форми властивості readonly.
    Для віджетів, які не мають ції властивості, встановлюється disabled.
    :param fields: список об'єктів полів форми
    :param readonly_fields: список назв полів, які мають бути readonly
    :return:
    """
    for field in readonly_fields:
        if field in fields:
            widget = fields[field].widget
            if widget.__class__.__name__ in get_readonly_disabled_widget_type_list():
                widget.attrs['disabled'] = 'disabled'
            else:
                widget.attrs['readonly'] = 'readonly'

def clear_help_text(fields):
    """
    Занулення тексту-підказки для всіх полів
    :param fields: список об'єктів полів форми
    :return:
    """
    for field in fields:
        fields[field].help_text = ""


class UserRegistrationForm(UserCreationForm):
    # Форма для реєстрації (створення нового) користувача

    required_css_class  = 'required'
    error_css_class     = 'error'

    class Meta:
        model = User
        fields = (
                'username',
                'first_name', 'last_name', 'email',
                )


class UserPersonDataForm(forms.ModelForm):
    # Коротка Форма для редагування персональних даних користувача.

    required_css_class  = 'required'
    error_css_class     = 'error'

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserPermsFullForm(forms.ModelForm):
    # Форма для редагування всіх даних стосовно доступу користувача

    # required_css_class  = 'required'
    # error_css_class     = 'error'

    # Трюк з полями readonly:
    READONLY_FIELDS = (
                        # 'username',
                        'first_name', 'last_name',
                        'date_joined', 'last_login',
                        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_readonly_widget_attrs(self.fields, self.READONLY_FIELDS)
        clear_help_text(self.fields)

    class Meta:
        model = User
        fields = (
                  # 'username',
                  'first_name', 'last_name',
                  'date_joined', 'last_login',
                  'is_active', 'is_staff',
                  'groups',
                )

class UserPermsActivateForm(UserPermsFullForm):
    # Форма для редагуванння даних стосовно активації доступу користувача

    # Додаємо поля, яких немає в моделі:
    has_perm_member = forms.NullBooleanField(
                            label="Доступ члена коопертиву",
                            widget=forms.CheckboxInput(),
                            # initial=get_is_member,
                            required=False,
                            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        # instance - примірник збереженої форми, у даному випадку
        # примірник моделі User
        self.is_member = None
        if instance:
            self.is_member = has_group_members(instance)
            self.fields['has_perm_member'].initial = self.is_member


    def get_is_member(self):
        return self.is_member

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('has_perm_member'):
            add_group(instance, 'members')
        else:
            remove_group(instance, 'members')
        if commit:
            instance.save()
        return instance

    class Meta:
        model = User
        fields = (
                  # 'username',
                  'first_name', 'last_name',
                  'date_joined',
                  'is_active',
                )


class ProfileFullForm(forms.ModelForm):
    # Повна Форма для вводу профілю - ВСІХ додаткових даних користувача.
    # УВАГА! Використовувати лише для адміністратора!
    is_recognized = forms.NullBooleanField(
                            label="Підтверджений",
                            widget=forms.CheckboxInput(),
                            required=False,
                            )

    class Meta:
        model = UserProfile
        fields = ('is_recognized', 'flat', 'picture')


class ProfilePermForm(ProfileFullForm):
    # Декларативно видаляємо деякі успадковані поля:
    picture = None

    # Трюк з полями readonly:
    READONLY_FIELDS = ('flat', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_readonly_widget_attrs(self.fields, self.READONLY_FIELDS)

    class Meta:
        model = UserProfile
        fields = ('is_recognized', 'flat')


class ProfilePersonDataForm(ProfileFullForm):
    # Декларативно видаляємо деякі успадковані поля:
    is_recognized = None

    class Meta:
        model = UserProfile
        fields = ('flat', 'picture')


class Human_Check:
    """
    Для перевірки, чи користувач є людиною.
    У простому реченні користувач повинен витерти одне із слів
    (номер слова обирається випадково).
    Перед відкриттям форми створюється примірник цього класу,
    а, отже, і речення-завдання, і потрібна відповідь.
    Речення-завдання task поступає у поле форми
    Метод validator цього класу присвоюється
    параметру validators поля форми.
    При неправильній відповіді у формі з'являється відповідне повідомлення.
    """
    if_view_test = False # встановити True в тестах, де ця перевірка заважатиме
    # TODO-зробити, щоб після неправильної відповіді або генерувалося нове речення-завдання, або взагалі виходилося з форми.
    taskPattern = "Видаліть із цієї стрічки %s слово"
    numerals = {
       -1: "останнє",
        0: "перше",
        1: "друге",
        2: "третє",
        3: "четверте",
        4: "п'яте",
        5: "шосте",
    }
    def __init__(self, n=None):
        if n == None:
            self.taskNo = randrange(-1, 6)
        else:
            self.taskNo = n
        self.task = self.taskPattern % self.numerals[self.taskNo]

    def validator(self, answer):
        twords = self.task.split()
        twords.pop(self.taskNo)
        awords = answer.split()
        check = twords == awords
        check = check or self.if_view_test
        if not check:
            raise ValidationError("Помилка!")


class ProfileRegistrationForm(ProfileFullForm):
    # Форма для реєстрації користувача
    # Модифікуємо деякі успадковані поля:
    is_recognized = None
    # Декларативно видаляємо деякі успадковані поля:

    # Додаємо поля, яких немає в батьківській формі:
    hc = Human_Check()  # примірник класу перевірки на "людяність"
    human_check = forms.CharField(
                    label='Доведіть, що Ви - людина',
                    initial=hc.task,        # речення-завдання
                    validators=[hc.validator],
                    required=True,
                    # інакше валідатор пропустить порожнє поле
                    # бо Django не перевіряє порожніх текстових полів!
                    )

    # У формі в тегах буде додано назву відповідного класу CSS:
    required_css_class  = 'required'
    error_css_class     = 'error'

    class Meta:
        model = UserProfile
        fields = ('flat', 'picture')

#---------------- Кінець коду, охопленого тестуванням ------------------

class UserSetMemberForm(UserPermsActivateForm):
    # Форма для редагуванння даних стосовно прав члена кооперативу
    READONLY_FIELDS = (
                        # 'username',
                        'first_name', 'last_name',
                        'date_joined', 'last_login',
                        )


