from itertools import chain
from django.contrib.auth.decorators import login_required, permission_required
from django.http import *
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from folders.forms import ReportUpdateForm, FolderForm, \
    FolderFormInFolder, ReportForm, ReportFormInFolder, \
    FolderDeleteForm
from folders.functions import response_for_download, \
    response_for_download_zip, get_subfolders, get_subreports, \
    get_full_named_path
from folders.models import Folder, Report
from koopsite.decorators import author_or_permission_required
from koopsite.fileExtIconPath import get_viewable_extension_list
from koopsite.views import AllFieldsView


class FolderList(ListView):
    model = Folder
    # paginate_by = 5
    ordering = 'name'
    template_name = 'folders/folder_list.html'


class FolderDetail(AllFieldsView):
    model = Folder
    template_name = 'folders/folder_detail.html'
    paginate_by = 12
    # exclude = ('id',)   # Поля, які виключаються із списку виводу.
    context_self_object_name = 'folder' # додатковий ідентифікатор для об'єкта self.object
    context_object_name = 'obj_details'  # додатковий ідентифікатор для списку self.object_list

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FolderDetail, self).dispatch(request, *args, **kwargs)


class ReportList(ListView):
    model = Report
    # paginate_by = 20
    ordering = 'filename'
    template_name = 'folders/report_list.html'


class ReportDetail(AllFieldsView):
    model = Report
    template_name = 'folders/report_detail.html'
    paginate_by = 12
    # exclude = ('id',)   # Поля, які виключаються із списку виводу.
    context_self_object_name = 'report'  # додатковий ідентифікатор для об'єкта self.object
    context_object_name = 'obj_details'  # додатковий ідентифікатор для списку self.object_list

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ReportDetail, self).dispatch(request, *args, **kwargs)


class ReportPreview(DetailView):
    model = Report
    template_name = 'folders/report_preview.html'
    # url_name='report-preview'

    @method_decorator(permission_required('folders.view_report'))
    def dispatch(self, request, *args, **kwargs):
        return super(ReportPreview, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ReportPreview, self).get_context_data(**kwargs)
        # Значення передадуться в шаблон:
        context['viewable_extension_list'] = get_viewable_extension_list()
        return context


class FolderCreate(CreateView):
    model = Folder
    form_class = FolderForm
    template_name = 'folders/folder_create.html'

    @method_decorator(permission_required('folders.add_folder'))
    def dispatch(self, *args, **kwargs):
        return super(FolderCreate, self).dispatch(*args, **kwargs)

    # def get_success_url(self):
    #     return reverse('folders:folder-list-all')


class FolderCreateInFolder(CreateView):
    # Створюємо теку у відомій материнській теці
    model = Folder
    form_class = FolderFormInFolder
    template_name = 'folders/folder_create.html'
    kwargs = {}

    @method_decorator(permission_required('folders.add_folder'))
    def dispatch(self, *args, **kwargs):
        self.kwargs.update({'parent': kwargs.get('parent') or 1}) # ОТРИМАННЯ даних з URLconf
        return super(FolderCreateInFolder, self).dispatch(*args, **kwargs)

    def get_initial(self):
        # Початкові дані, які відомі наперед:
        parent = Folder.objects.get(id=self.kwargs.get('parent'))
        self.initial = {'parent': parent, }
        return self.initial.copy()

    def post(self, request, *args, **kwargs):
        self.object = None
        # POST не передає поля disabled (яким є наше поле parent типу select)
        # Тому форма створюється вручну із даних request + initial
        # спеціально для валідації:
        data = request.POST.copy()
        parent = Folder.objects.get(id=self.kwargs.get('parent'))
        data['parent'] = parent.id
        form = self.form_class(data=data)
        if form.is_valid():
            folder = form.save(commit=False)    # збережений ще "сирий" примірник
            folder.created_on = timezone.now()  # не використовуємо auto_now
            folder.save()                       # остаточне збереження
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class FolderDelete(DeleteView):
    model = Folder
    form_class = FolderDeleteForm
    template_name = 'folders/folder_delete.html'

    @method_decorator(permission_required('folders.delete_folder'))
    def dispatch(self, *args, **kwargs):
        return super(FolderDelete, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        folder = self.get_object()
        if get_subfolders(folder) or get_subreports(folder):
            return HttpResponseRedirect(reverse('folders:folder-not-empty'))
        else:
            folder.delete()
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('folders:folder-list-all')


class ReportDelete(DeleteView):
    model = Report
    form_class = ReportForm
    template_name = 'folders/report_delete.html'

    @method_decorator(author_or_permission_required(model, 'folders.delete_report'))
    def dispatch(self, *args, **kwargs):
        return super(ReportDelete, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.file.delete()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('folders:folder-list-all')


class FolderUpdate(UpdateView):
    model = Folder
    form_class = FolderForm
    template_name = 'folders/folder_update.html'

    @method_decorator(permission_required('folders.change_folder'))
    def dispatch(self, *args, **kwargs):
        return super(FolderUpdate, self).dispatch(*args, **kwargs)


class ReportUpdate(UpdateView):
    model = Report
    form_class = ReportUpdateForm
    template_name = 'folders/report_update.html'

    @method_decorator(author_or_permission_required(model, 'folders.change_report'))
    def dispatch(self, *args, **kwargs):
        return super(ReportUpdate, self).dispatch(*args, **kwargs)


class ReportUpload(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'folders/report_upload.html'

    @method_decorator(permission_required('folders.add_report'))
    def dispatch(self, *args, **kwargs):
        return super(ReportUpload, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            report = form.save(commit=False)    # збережений ще "сирий" примірник
            report.user = request.user
            report.save()                       # остаточне збереження
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ReportUploadInFolder(CreateView):
    # Завантажуємо файл у відому материнську теку
    model = Report
    form_class = ReportFormInFolder
    template_name = 'folders/report_upload.html'
    kwargs = {}

    @method_decorator(permission_required('folders.add_report'))
    def dispatch(self, *args, **kwargs):
        self.kwargs.update({'parent': kwargs.get('parent') or 1}) # ОТРИМАННЯ даних з URLconf
        return super(ReportUploadInFolder, self).dispatch(*args, **kwargs)

    def get_initial(self):
        # Початкові дані, які відомі наперед:
        parent = Folder.objects.get(id=self.kwargs.get('parent'))
        self.initial = {'parent': parent, }
        return self.initial.copy()

    def post(self, request, *args, **kwargs):
        self.object = None
        # POST не передає поля disabled (яким є наше поле parent типу select)
        # Тому форма створюється вручну із даних request + initial
        # спеціально для валідації:
        data = request.POST.copy()
        parent = Folder.objects.get(id=self.kwargs.get('parent'))
        data['parent'] = parent.id
        form = self.form_class(data=data, files=request.FILES)
        if form.is_valid():
            report = form.save(commit=False)    # збережений ще "сирий" примірник
            report.user = request.user
            report.save()                       # остаточне збереження
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@permission_required('folders.download_folder')
def folderDownload(request, *args, **kwargs):
    # Завантаження zip-файла, який складається з всіх файлів теки
    folder_id = kwargs.get('pk')
    folder = Folder.objects.get(id=folder_id)
    response, zipFilename, msg = response_for_download_zip(folder)
    return response

@permission_required('folders.download_report')
def reportDownload(request, *args, **kwargs):
    report_id = kwargs.get('pk')
    report = Report.objects.get(id=report_id)
    response = response_for_download(report, cd_value='attachment')
    return response


class FolderParentList(ListView):
    # Перегляд тек, які не є дочірніми (тобто, кореневих тек)
    queryset = Folder.objects.filter(parent=None)
    # paginate_by = 20
    template_name = 'folders/folder_parents.html'


class FolderReportList(ListView):
    # paginate_by = 15
    template_name = 'folders/folder_list_all.html'
    # context_object_name = "all_list" # додатковий ідентифікатор для списку self.object_list

    def get_queryset(self):
        # Дочірні об'єкти:
        # два queryset з різних моделей об'єднується в один qs,
        # який обробляється в template як одне ціле
        fs = Folder.objects.all()
        rs = Report.objects.all()
        qs = list(chain(fs, rs))
        qs = sorted(qs, key=lambda x: get_full_named_path(x))
        return qs


#---------------- Кінець коду, охопленого тестуванням ------------------

import csv
from django.http import HttpResponse

def txt_view(request):
    '''
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'inline; filename="somefilename.txt"'
    response['Content-Disposition'] = 'render; filename="somefilename.txt"'
    # response['Content-Disposition'] = 'inline;'
    # response['Content-Disposition'] = 'attachment; filename="somefilename.txt"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
    return response
    '''

    text_data = "Long-long text"
    response = HttpResponse(text_data, content_type="text/plain")
    response['Content-Disposition'] = 'inline; filename="somefilename.txt"'
    print('response =', response)
    print('response =', response.__dict__)
    for i in response.__dict__:
        print('%-30s : %s' % (i, getattr(response, i, None)))
    return response


class DisplayPDFView(View):

    def get_context_data(self, **kwargs):  # Exec 1st
        context = {}
        # context logic here
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        image_data = open("example.pdf", "rb").read()
        response = HttpResponse(image_data, content_type="application/pdf")
        response['Content-Disposition'] = 'inline; filename="somefilename.txt"'
        print('response =', response)
        print('response =', response.__dict__)
        for i in response.__dict__:
            print('%-30s : %s' % (i, getattr(response, i, None)))
        return response

def some_view(request):

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'inline; filename="somefilename.txt"'
    response['Content-Disposition'] = 'render; filename="somefilename.txt"'
    # response['Content-Disposition'] = 'inline;'
    # response['Content-Disposition'] = 'attachment; filename="somefilename.txt"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response


@permission_required('folders.view_report')
def reportPreview(request, pk):
    report_id = pk
    report = Report.objects.get(id=report_id)
    # print('report=', report.id, report.filename, report.file)
    response = response_for_download(report, cd_value='inline')
    return response


# @owner_or_perm_required('folders.view_report')
def reportDecorView(request, pk):
    report_id = pk
    report = Report.objects.get(id=report_id)
    print('report=', report.id, report)
    response = response_for_download(report, cd_value='inline')
    return response

