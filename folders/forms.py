from django import forms
from koopsite.forms import set_readonly_widget_attrs
from .models import Folder, Report


class FolderFormBase(forms.ModelForm):
    # Базова форма для роботи з теками
    required_css_class  = 'required'
    error_css_class     = 'error'

    # Трюк з полями readonly:
    READONLY_FIELDS = ()

    def __init__(self, *args, **kwargs):
        super(FolderFormBase, self).__init__(*args, **kwargs)
        set_readonly_widget_attrs(self.fields, self.READONLY_FIELDS)

    class Meta:
        model  = Folder
        fields = ('parent', 'name', 'created_on')


class FolderForm(FolderFormBase):
    # Форма для вводу тек
    class Meta:
        model  = Folder
        fields = ('parent', 'name', 'created_on')


class FolderFormInFolder(FolderFormBase):
    # Форма для створення теки у материнській теці
    READONLY_FIELDS = ('parent',)

    class Meta:
        model  = Folder
        fields = ('parent', 'name',)


class FolderDeleteForm(FolderFormBase):
    # Форма для видалення теки
    READONLY_FIELDS = ('parent', 'name', 'created_on')


class ReportFormBase(forms.ModelForm):
    # Форма для вводу даних про файл у відомій теці
    required_css_class  = 'required'
    error_css_class     = 'error'

    # Трюк з полями readonly:
    READONLY_FIELDS = []

    def __init__(self, *args, **kwargs):
        super(ReportFormBase, self).__init__(*args, **kwargs)
        set_readonly_widget_attrs(self.fields, self.READONLY_FIELDS)

    class Meta:
        model = Report
        fields = ('parent', 'filename', 'file')


class ReportForm(forms.ModelForm):
    # Форма для вводу даних про файл
    READONLY_FIELDS = ()

    class Meta:
        model = Report
        fields = ('parent', 'file')


class ReportFormInFolder(ReportFormBase):
    # Форма для вводу даних про файл у відомій теці
    READONLY_FIELDS = ('parent',)

    class Meta:
        model = Report
        fields = ('parent', 'file',)


class ReportUpdateForm(ReportFormBase):
    # Форма для редагування даних про файл
    READONLY_FIELDS = ()

    class Meta:
        model = Report
        fields = ('parent', 'filename', 'file')


#---------------- Кінець коду, охопленого тестуванням ------------------
