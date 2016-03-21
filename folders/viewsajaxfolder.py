import os
import json
import types
from itertools import chain
from django.contrib.auth.decorators import permission_required
from django.core.files.base import ContentFile
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView
from folders.functions import response_for_download, \
                        response_for_download_zip, \
                        get_folders_tree_HTML, get_parents, \
                        get_subfolders, get_subreports
from folders.models import Folder, Report
from koopsite.decorators import author_or_permission_required
from koopsite.functions import fileNameCheckInsert, \
                        get_namespace_from_dict, \
                        get_iconPathForFolder, get_iconPathByFileExt, \
                        get_or_none, \
                        getSelElementFromSession, \
                        setSelElementToSession, \
                        parseClientRequest, \
                        parseXHRClientRequest, dict_print
from koopsite.settings import STATIC_URL, MAX_FILE_SIZE
from koopsite.viewsajax import msgType, BrowseTableArray


#################################################################
# Дочірній клас для формування 2D таблиці, яка поступає в шаблон
# folder_contents.html одночасно з синхронним рендерингом,
# і дозволяє оперативно змінювати дані з допомогою jQuery ajax
# Крім того ряд методів використовується "назовні":
#################################################################

class FolderContentsArray(BrowseTableArray):
    columnsNumber   = 4        # number of columns in table

    def get_table_headers(self):
        # Шапка таблиці для кожної колонки, починаючи з 1.
        # Нульова колонка - службова
        cap = {
            0: "",
            1: "Тип",
            2: "Найменування",
            3: "Дата",
            4: "Розмір",
            }
        return cap

    def get_model_id_name(self, f):
        """
        Визначає назву моделі та id примірника u
        :param f: примірник моделі
        :return: {'id': f.id, 'model': m}
        """
        try:
            m = f._meta.model_name
            if   m == 'folder': n = f.name
            elif m == 'report': n = f.filename
            else:               n = ""
            m_id_n = {
                'id'    : str(f.id),
                'model' : m,
                'name'  : n,
                }
        except:
            m_id_n = {}
        return m_id_n

    def get_row(self, f):
        """
        Визначає один рядок у двомірному масиві даних таблиці.
        Формат рядка:
         row - словник {j: val},
         де j - номер колонки в таблиці (поч. з 1)
            val - значення j-ї клітинки
         Службове поле:
            row[0] - словник з даними про примірник:
                        {'id': f.id, 'model': m, 'name': name}
        :param f: примірник qs
        :return row: одновимірний словник
        """
        if f:
            row = {}
            m = f._meta.model_name
            row[0] = self.get_model_id_name(f)
            row[1] = m
            if m == 'folder':
                row[2] = f.name
                row[3] = f.created_on.isoformat() \
                                if f.created_on else ""
                row[4] = ""
            if m == 'report':
                row[2] = f.filename
                row[3] = f.uploaded_on.isoformat() \
                                if f.uploaded_on else ""
                row[4] = f.file.size if f.file else ""
        else: # елемента нема => рядок таблиці має бути None
            row = None
        return row

    def get_supplement_data(self, f):
        # додаткові дані для передачі в шаблон через XHR,
        # які простіше отримати в Python і використати в js
        # для зміни / створення нового рядка в таблиці
        if f:
            data = {}
            fileExt  = None
            fileType = None
            iconPath = None
            m = f._meta.model_name
            if m == 'folder':
                fileExt  = ""
                fileType = "folder"
                iconPath = STATIC_URL + get_iconPathForFolder()
            if m == 'report':
                (name, ext) = os.path.splitext(f.filename)
                fileExt  = ext
                fileType = "report"
                iconPath = STATIC_URL + get_iconPathByFileExt(ext)
            data['iconPath'] = iconPath
            data['fileExt' ] = fileExt
            data['fileType'] = fileType
        else:
            data = None
        return data


class FolderContents(SingleObjectMixin, ListView):
    # Вміст теки: дочіні теки і файли
    # Авторизація не потрібна. Перевірка буде на етапі
    # спроби завантаження чи створення.
    # paginate_by = 12
    template_name = 'folders/folder_contents.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Folder.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Материнська тека
        context = super().get_context_data(**kwargs)
        context['folder'] = self.object
        context['parents'] = get_parents(self.object)
        parent_id = self.object.id
        browTabName = 'folders_contents'    # назва таблиці (для сесії і ajax)
        # Беремо з сесії масив параметрів виділеного елемента
        # для даного parent_id:
        selElement = getSelElementFromSession(self.request.session,
                                            browTabName,
                                            parent_id=parent_id)
        selElementModel = selElement.get('model')
        selElementID    = selElement.get('id')
        if selElementModel and selElementID:
            # відомі параметри виділеного рядка
            sel_model_id = {'id': selElementID, 'model': selElementModel}
        else:
            # вперше відвідуємо цю теку
            sel_model_id = {}
        # Готуємо 2D-масив всіх даних таблиці
        # Одночасно шукаємо порядковий номер виділеного рядка
        bta = FolderContentsArray()
        arr, sel_index = bta.get_qs_array(self.qs, sel_model_id)
        cap = bta.get_table_headers()

        # Значення передадуться в шаблон:
        context['browTabName']      = browTabName

        context['selRowIndex']      = sel_index
        context['selElementModel']  = sel_model_id.get('model')
        context['selElementID']     = sel_model_id.get('id')

        context['cap'] = cap    # список заголовків таблиці
        # context['arr'] = arr    # 2D-масив даних таблиці:
        # Одночасно передаємо цей же 2D-масив для обробки js.
        # Дата ще на етапі формування масиву вже перетворена
        # в isoformat, прийнятний для JSON.
        json_arr = json.dumps(arr)
        context['json_arr'] = json_arr

        # Записуємо в сесію:
        selElement['selRowIndex'] = sel_index
        selElement['model'] = sel_model_id.get('model')
        selElement['id'] = sel_model_id.get('id')
        setSelElementToSession(self.request.session,
                                            browTabName,
                                            parent_id=parent_id,
                                            selElement=selElement)
        return context

    def get_queryset(self):
        # Дочірні об'єкти:
        # два queryset з різних моделей об'єднується в один qs,
        # який обробляється в template як одне ціле (в т.ч. з Paginator'ом)
        fs = self.object.children.all().order_by('name'.lower())
        rs = Report.objects.filter(parent=self.object).order_by('filename'.lower())
        self.qs = list(chain(fs, rs))
        return self.qs


#################################################################
# jQuery ajax base class for single row from BrowTable:
#################################################################

class AjaxTableRowViewBase(View):
    """
    CBV - базовий суперклас для обробки AJAX-запитів з таблиці.
    Від класу View використовується:
        метод as_view() - для виклику в urls.py,
        метод dispatch - для декорування в субкласах.
    Метод dispatch зводиться до виклику функції handler
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Простір імен для додаткових даних з запиту клієнта:
        self.rqst = types.SimpleNamespace(
                                            parent_id   = None,
                                            model       = None,
                                            id          = None,
                                            name        = None,
                                            target_id   = None,
                                            )
        # Простір імен для повідомлень клієнту:
        self.msg = types.SimpleNamespace(
                                            title   = "",
                                            type    = "",
                                            message = ""
                                            )

    def dispatch(self, request, *args, **kwargs):
        return self.handler(request)

    def handler(self, request):
        """
        Основний обробних даних. Порядок виконання:
        - дані з request.POST зберігаємо у rqst, і визначаємо
            element - примірник моделі, над яким слід зробити дії;
        - запам'ятовуємо рядок таблиці ДО змін;
        - перевіряємо можливість дій, виконуємо їх і отримуємо
            змінений element з відповідним повідомленням msg;
        - отримуємо changes - масив змінених даних для рядка таблиці;
            які потрібно змінити
            Елемент - рядок таблиці ПІСЛЯ змін (якщо були):
            Зміни рядка в таблиці:
        - формуємо словник response_cont для передачі в шаблон через XHR;
        - посилаємо відповідь клієнту (з перетворенням JSON):
        self.rqst і self.msg як порожні шаблони використовуються
        у якості вхідних параметрів двох функцій нижче:
        """
        if 'client_request' in request.POST:
            element, rqst = self.get_request_data(request, self.rqst)
            if not element:
                print("There is no element in request.POST")
                return HttpResponse()
            old_element = FolderContentsArray().get_row(element)
            element, msg = self.processing(element, rqst, self.msg)
            new_element = FolderContentsArray().get_row(element)
            if msg.type == msgType.NewRow:
                changes = new_element
            else:
                changes = FolderContentsArray().get_cell_changes(old_element, new_element)
            supplement = FolderContentsArray().get_supplement_data(element)
            response_cont = vars(msg)
            response_cont['changes'] = changes
            response_cont['supplement'] = supplement
            # return JsonResponse(response_cont)
            return HttpResponse(json.dumps(response_cont), content_type="application/json")
        else:
            print("There is no 'client_request' in request.POST")
            return HttpResponse()

    def get_request_data(self, request, rqst):
        # Розбираємо дані від клієнта:
        try:
            d = parseClientRequest(request.POST)
        except ValueError as err:
            # запит від клієнта містить невідповідні дані:
            print('get_request_data:', err.args)
            return None, None
        rqst = get_namespace_from_dict(d, rqst)
        # rqst.parent_id            = d.get('parent_id')
        # rqst.model                = d.get('model')
        # rqst.id                   = d.get('id')
        # rqst.name                 = d.get('name')
        # rqst.target_id            = d.get('target_id')
        if rqst.model == "folder":
            element = Folder.objects.get(id=rqst.id)
        elif rqst.model == "report":
            element = Report.objects.get(id=rqst.id)
        else:
            return None, None
        if not element:
            rqst = None
        return element, rqst

    def processing(self, element, rqst, msg):
        """
        Цю функцію треба переозначити у дочірньому класі.
        Тут наводиться як ПРИКЛАД.
        """
        f_name_list = [f.name for f
                            in Folder.objects.filter(parent_id=rqst.parent_id)]
        # Умови при яких зміни не відбудуться:
        if not rqst.name or rqst.name == "":
            msg.type    = msgType.IncorrectData
            msg.title   = "Нова тека"
            msg.message = "Ви не вказали назву теки!"
        elif rqst.name in f_name_list:
            msg.type    = msgType.IncorrectData
            msg.title   = "Нова тека"
            msg.message = "Тека з такою назвою вже існує!"
        else:
            # Робимо зміни:
            folder            = Folder()
            folder.name       = rqst.name
            folder.parent     = Folder.objects.get(id=rqst.parent_id)
            folder.created_on = timezone.now()  # не використовуємо auto_now
            folder.save()                       # остаточне збереження
            msg.title   = folder.name
            msg.type    = msgType.NewRow
            msg.message = "Тека створена!"
            element = folder
        return element, msg


#################################################################
# jQuery ajax CBV for single row:
#################################################################

class AjaxFolderCreate(AjaxTableRowViewBase):
    # raise_exception=True - для ajax.
    # Тоді виняток обробить xhrErrorHandler (js).

    @method_decorator(permission_required('folders.add_folder', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def processing(self, folder, rqst, msg):
        # Список існуючих імен в теці:
        f_name_list = [f.name for f
                       in Folder.objects.filter(parent_id=rqst.parent_id)]
        # Умови при яких зміни не відбудуться:
        if not rqst.name or rqst.name == "":
            msg.type    = msgType.IncorrectData
            msg.title   = "Нова тека"
            msg.message = "Ви не вказали назву теки!"
        elif rqst.name in f_name_list:
            msg.type    = msgType.IncorrectData
            msg.title   = "Нова тека"
            msg.message = "Тека з такою назвою вже існує!"
        else:
            # Робимо зміни:
            folder            = Folder()        # новий примірник
            folder.name       = rqst.name
            folder.parent     = Folder.objects.get(id=rqst.parent_id)
            folder.created_on = timezone.now()  # не використовуємо auto_now
            folder.save()                       # остаточне збереження
            msg.title   = folder.name
            msg.type    = msgType.NewRow
            msg.message = "Теку створено!"
        return folder, msg


class AjaxFolderRename(AjaxTableRowViewBase):
    # Перейменовуємо обрану теку у відомій теці з доп. AJAX

    @method_decorator(permission_required('folders.change_folder', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def processing(self, folder, rqst, msg):
        # Список існуючих імен в теці:
        f_name_list = [f.name for f
           in Folder.objects.filter(parent_id=rqst.parent_id) \
                                .exclude(id=rqst.id)]
        # Умови при яких зміни не відбудуться:
        if not rqst.name or rqst.name == "":
            msg.type    = msgType.IncorrectData
            msg.title   = folder.name
            msg.message = "Ви не вказали назву теки!"
        elif rqst.name in f_name_list:
            msg.type    = msgType.IncorrectData
            msg.title   = folder.name
            msg.message = "Тека з такою назвою вже існує!"
        elif rqst.name == folder.name:
            msg.title   = folder.name
            msg.type    = msgType.NoChange
            msg.message = "Ви не змінили назву теки!"
        else:
            # Робимо зміни:
            folder.name       = rqst.name
            folder.save()                       # остаточне збереження
            msg.title   = folder.name
            msg.type    = msgType.Rename
            msg.message = "Теку перейменовано!"
        return folder, msg


class AjaxReportRename(AjaxTableRowViewBase):
    # Перейменовуємо обрану теку у відомій теці з доп. AJAX

    @method_decorator(permission_required('folders.change_report', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def processing(self, report, rqst, msg):
        # Список існуючих імен в теці:
        f_name_list = [f.filename for f
           in Report.objects.filter(parent_id=rqst.parent_id) \
                                .exclude(id=rqst.id)]
        # Умови при яких зміни не відбудуться:
        if not rqst.name or rqst.name == "":
            msg.type    = msgType.IncorrectData
            msg.title   = report.filename
            msg.message = "Ви не вказали нову назву файла!"
        elif rqst.name in f_name_list:
            msg.type    = msgType.IncorrectData
            msg.title   = report.filename
            msg.message = "Файл з такою назвою вже існує!"
        elif rqst.name == report.filename:
            msg.title   = report.filename
            msg.type    = msgType.NoChange
            msg.message = "Ви не змінили назву файла!"
        else:
            # Робимо зміни:
            report.filename  = rqst.name
            report.save()                       # остаточне збереження
            msg.title   = report.filename
            msg.type    = msgType.Rename
            msg.message = "Файл перейменовано!"
        return report, msg


class AjaxElementMove(AjaxTableRowViewBase):
    # Переміщуємо обраний елемент в іншу теку з доп. AJAX

    @method_decorator(permission_required('folders.change_folder', raise_exception=True))
    @method_decorator(permission_required('folders.change_report', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def processing(self, element, rqst, msg):
        # Список існуючих імен в теці призначення:
        if rqst.model == "folder":
            target_name_list = [f.name for f
               in Folder.objects.filter(parent_id=rqst.target_id)]
        elif rqst.model == "report":
            target_name_list = [f.filename for f
               in Report.objects.filter(parent_id=rqst.target_id)]
        else: target_name_list = None
        target = get_or_none(Folder, id=rqst.target_id)
        # Умови при яких зміни не відбудуться:
        if not rqst.target_id or rqst.target_id in (0, '0'):
            msg.title   = rqst.name
            msg.type    = msgType.IncorrectData
            msg.message = "Ви не обрали місце призначення!"
        elif rqst.target_id == rqst.parent_id:
            msg.title   = rqst.name
            msg.type    = msgType.NoChange
            msg.message = "Ви не змінили розташування!"
        elif rqst.model == 'folder' and rqst.target_id == rqst.id:
            msg.title   = rqst.name
            msg.type    = msgType.IncorrectData
            msg.message = "Не можна перемістити теку саму в себе :)"
        elif rqst.name in target_name_list:
            msg.title   = rqst.name
            msg.type    = msgType.IncorrectData
            msg.message = "В обраному місці призначення є %s з такою назвою!" % \
                            ("тека" if rqst.model == 'folder' else "файл")
        elif not element or not target:
            msg.title   = rqst.name
            msg.type    = msgType.Error
            msg.message = "Не вдалося змінити розташування! " \
                            "Можливо обране місце призначення не існує."
        else:
            # Робимо зміни:
            element.parent = target
            element.save()       # збереження в базі
            msg.title   = rqst.name
            msg.type    = msgType.MoveElement
            msg.message = "%s переміщено!" % \
                          ("Теку" if rqst.model == 'folder' else "Файл")
        return element, msg


class AjaxFolderDelete(AjaxTableRowViewBase):
    # Перейменовуємо обрану теку у відомій теці з доп. AJAX
    @method_decorator(permission_required('folders.delete_folder', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def processing(self, folder, rqst, msg):
        # Умови при яких зміни не відбудуться:
        if get_subfolders(folder) or get_subreports(folder):
            msg.title   = rqst.name
            msg.type    = msgType.Forbidden
            msg.message = "Обрана тека не порожня! Спершу слід видалити вміст теки."
        else:
            # Робимо зміни:
            folder.delete() # тека видалена з бази даних
            msg.title   = rqst.name
            msg.type    = msgType.DeleteRow
            msg.message = "Теку видалено!"
        return None, msg


class AjaxReportDelete(AjaxTableRowViewBase):
    # Перейменовуємо обрану теку у відомій теці з доп. AJAX

    @method_decorator(author_or_permission_required(Report, 'folders.delete_report', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def processing(self, report, rqst, msg):
        # Умови при яких зміни не відбудуться:
        if False: # перевірка відбувається раніше декоратором
            msg.title   = rqst.name
            msg.type    = msgType.Forbidden
            msg.message = "У Вас немає доступу для видалення обраного файла."
        else:
            # Робимо зміни:
            report.file.delete()    # файл видалено з диска
            report.delete()         # файл видалено з бази даних
            msg.title   = rqst.name
            msg.type    = msgType.DeleteRow
            msg.message = "Файл видалено!"
        return None, msg


#################################################################
# XMLHttpRequest base class for single row from BrowTable:
#################################################################

class XHRTableRowView(View):
    """
    CBV - базовий суперклас для обробки XHR-запитів з таблиці.
    Від класу View використовується:
        метод as_view() - для виклику в urls.py,
        метод dispatch - для декорування в субкласах.
    Метод dispatch зводиться до виклику функції handler
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Простір імен для додаткових даних з запиту клієнта:
        self.rqst = types.SimpleNamespace(
                            parent_id   = None,
                            model       = None,
                            id          = None,
                            name        = None,
                            target_id   = None,
                            fileName             = None,
                            fileSize             = None,
                            fileType             = None,
                            fileLastModifiedDate = None,
                            )

        # Простір імен для повідомлень клієнту:
        self.msg = types.SimpleNamespace(title   = "",
                                    type    = "",
                                    message = ""
                                    )


    def dispatch(self, request, *args, **kwargs):
        return self.handler(request)

    def get_XHR_data(self, request, rqst):
        # Розбираємо дані від клієнта:
        try:
            d = parseXHRClientRequest(request.META)
        except ValueError as err:
            # запит від клієнта містить невідповідні дані:
            print('get_XHR_data:', err.args)
            return None, None
        rqst = get_namespace_from_dict(d, rqst, True)
        # rqst.parent_id            = d.get('parent_id')
        # rqst.model                = d.get('model')
        # rqst.id                   = d.get('id')
        # rqst.name                 = d.get('name')
        # rqst.target_id            = d.get('target_id')
        # rqst.fileName             = d.get('fileName')
        # rqst.fileSize             = d.get('fileSize')
        # rqst.fileType             = d.get('fileType')
        # rqst.fileLastModifiedDate = d.get('fileLastModifiedDate')
        if rqst.model == "folder":
            element = Folder.objects.get(id=rqst.id)
        elif rqst.model == "report":
            element = Report.objects.get(id=rqst.id)
        else:
            return None, None
        if not element:
            rqst = None
        return element, rqst

    def handler(self,request):
        if "HTTP_X_CLIENT_REQUEST" in request.META:
            element, rqst = self.get_XHR_data(request, self.rqst)
            if not element:
                print("There is no element in request.META")
                return HttpResponseBadRequest("There is no element in request.META")

            old_element = FolderContentsArray().get_row(element)

            element, msg, response = \
                self.processing(request, element, rqst, self.msg)

            new_element = FolderContentsArray().get_row(element)
            if msg.type == msgType.NewRow:
                changes = new_element
            else:
                changes = FolderContentsArray().get_cell_changes(old_element, new_element)
            supplement = FolderContentsArray().get_supplement_data(element)

            # Посилаємо відповідь клієнту:
            response_cont = vars(msg)
            response_cont['changes'] = changes
            response_cont['supplement'] = supplement
            json_s = json.dumps(response_cont)
            response['server_response'] = json_s
            print('class: %-30s %s' % (self.__class__.__name__, '-'*30))
            dict_print(response, 'response')
            return response
        else:
            print("There is no 'HTTP_X_CLIENT_REQUEST' in request.META")
            return HttpResponseBadRequest("There is no 'HTTP_X_CLIENT_REQUEST' in request.META")

    def processing(self, request, report, rqst, msg):
        """
        Цю функцію треба переозначити у дочірньому класі.
        Тут наводиться як ПРИКЛАД.
        """
        # Умови при яких зміни не відбудуться:
        if False: # Тут вставити перевірку на право завантаження файла
            msg.title   = rqst.name
            msg.type    = msgType.Forbidden
            msg.message = "У Вас немає доступу для завантаження обраного файйла."
            response = HttpResponse()
        else:
            # Downloading file:
            response = response_for_download(report)
            msg.title   = rqst.name
            msg.type    = msgType.Normal
            msg.message = "Файл успішно завантажено!"
        return report, msg, response

#################################################################
# XMLHttpRequest jQuery ajax CBV for single row:
#################################################################

class XHRReportDownload(XHRTableRowView):
    # Завантажуємо обраний файл з доп. XMLHttpRequest

    @method_decorator(permission_required('folders.download_report', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def processing(self, request, report, rqst, msg):
        # Умови при яких зміни не відбудуться:
        if False: # Тут вставити перевірку на право завантаження файла
            msg.title   = rqst.name
            msg.type    = msgType.Forbidden
            msg.message = "У Вас немає доступу для завантаження обраного файла."
            response = HttpResponse()
        else:
            # Downloading file:
            response = response_for_download(report)
            msg.title   = rqst.name
            msg.type    = msgType.Normal
            msg.message = "Файл успішно завантажено!"
            dict_print(response, 'XHRReportDownload: response' )
        return report, msg, response


class XHRFolderDownload(XHRTableRowView):
    # Завантажуємо всі файли з обраної теки з доп. XMLHttpRequest

    @method_decorator(permission_required('folders.download_folder', raise_exception=True))
    @method_decorator(permission_required('folders.download_report', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def processing(self, request, folder, rqst, msg):
        # Умови при яких зміни не відбудуться:
        if False: # Тут вставити перевірку на право завантаження теки
            msg.title   = rqst.name
            msg.type    = msgType.Forbidden
            msg.message = "У Вас немає доступу для завантаження обраної теки."
            response = HttpResponse()
        else:
            response, zipFilename, msg_message = \
                                    response_for_download_zip(folder)
            msg.title   = zipFilename
            msg.type    = msgType.Normal
            msg.message = msg_message or "Вміст теки успішно завантажено!"
        return folder, msg, response


class XHRReportUpload(XHRTableRowView):
    # Заладовуємо новий файл у відому теку з доп. XMLHttpRequest

    @method_decorator(permission_required('folders.add_report', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def processing(self, request, report, rqst, msg):
        maxFileSize = MAX_FILE_SIZE
        report_name_list = [f.filename for f in
                            Report.objects.filter(parent_id=rqst.parent_id)]
        # Умови при яких зміни не відбудуться:
        if not rqst.fileName or rqst.fileName == "":
            msg.title   = "Заладування файла"
            msg.type    = msgType.IncorrectData
            msg.message = "Ви не вказали назву файла!"
        elif int(rqst.fileSize) > maxFileSize:
            msg.title   = "Заладування файла"
            msg.type    = msgType.Forbidden
            msg.message = "Розмір файла %s перевищує дозволене значення %s!" \
                          % (rqst.fileSize, maxFileSize)
        else:
            # Починаємо заладування:
            rqst.fileName = fileNameCheckInsert(rqst.fileName, report_name_list)

            report           = Report()
            report.parent    = Folder.objects.get(id=rqst.parent_id)
            report.save()    # зберігаємо "сирий" примірник щоб отримати id
                             # при цьому файл ще не зберігається
            rqst.id = report.id

            # Файл буде збережено під кодовою назвою
            # Схоже, що ця назва не береться до уваги,
            # бо в моделі працює upload_to
            codedFileName = str(report.pk) + ".upl"

            # Збереження власне файла
            try:
                report.file.save(codedFileName, ContentFile(request.body))
            except:
                # Помилка збереження, найімовірніше - файл завеликий
                print('Saving error. Probably file too large')
                # Видаляємо з бази і з диска недозбережений файл:
                try:
                    report.file.delete()    # файл видалено з диска
                    print('file deleted')
                except:
                    print('file was not saved')
                report.delete()         # файл видалено з бази даних
                print('report deleted')
                msg.title   = rqst.fileName
                msg.type    = msgType.Error
                msg.message = "Заладування на сервер прининене!" \
                                   "Очевидно, файл занадто великий."
            else:
                # Завантаження пройшло без помилок
                report.filename  = rqst.fileName
                fileSizeFact     = report.file.size

                if fileSizeFact == int(rqst.fileSize):
                    # Файл завантажено повністю
                    report.uploaded_on = rqst.fileLastModifiedDate or timezone.now()

                    report.save()    # остаточне збереження примірника моделі

                    # Витягуємо щойно збережене з бази, щоб мати
                    # правильно відформатовані дані, зокрема дату
                    report = Report.objects.get(id=rqst.id)
                    # TODO-перевірити чому filesize.js для NewRow показує розмір без одиниць виміру
                    msg.title   = rqst.fileName
                    msg.type    = msgType.NewRow
                    msg.message = "Файл успішно заладовано на сервер!"
                else:
                    # Файл завантажено частково - клієнт послав xhr.abort()
                    print('Error: fileSizeFact <> fileSize')
                    # Видаляємо з бази і з диска недозбережений файл:
                    report.file.delete()    # файл видалено з диска
                    print('file deleted')
                    report.delete()         # файл видалено з бази даних
                    print('report deleted')
                    msg.title   = rqst.fileName
                    msg.type    = msgType.Error
                    msg.message = "Заладування на сервер перерване!"
        response = HttpResponse()
        return report, msg, response


#################################################################
# jQuery ajax functions:
#################################################################

def ajaxFoldersTreeFromBase(request):
    if 'client_request' in request.POST:
        # Формуємо дерево тек у вигляді HTML для роботи jsTree :
        folderTree = get_folders_tree_HTML()
        # Посилаємо відповідь клієнту:
        response_dict = {'server_response': folderTree }
        # return JsonResponse(response_dict)
        return HttpResponse(json.dumps(response_dict), content_type="application/json")
    else:
        print("There is no 'client_request' in request.POST")
        return HttpResponse()

#---------------- Кінець коду, охопленого тестуванням ------------------
