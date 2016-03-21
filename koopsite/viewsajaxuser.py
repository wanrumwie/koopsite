from collections import OrderedDict
from copy import deepcopy
import json
import types
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.list import ListView
from koopsite.models import UserProfile
from koopsite.settings import EMAIL_HOST_USER, STATIC_URL, SITE_ADDRESS
from koopsite.functions import has_group, add_group, \
                        remove_group, is_staff_only, \
                        get_user_full_name, get_user_flat_No, \
                        get_user_is_recognized, get_or_none, \
                        get_browTabName_models
from koopsite.functions import  getSelElementFromSession, \
                        setSelElementToSession, \
                        parseClientRequest
from koopsite.templatetags.koop_template_filters import icon_yes_no_unknown
from koopsite.viewsajax import msgType, BrowseTableArray


#################################################################
# Дочірній клас для формування 2D таблиці, яка поступає в шаблон
# koop_adm_users_table.html одночасно з синхронним рендерингом,
# і дозволяє оперативно змінювати дані з допомогою jQuery ajax:
#################################################################

class UsersTableArray(BrowseTableArray):
    columnsNumber   = 8        # number of columns in table

    def get_table_headers(self):
        # Шапка таблиці для кожної колонки, починаючи з 1.
        # Нульова колонка - службова
        cap = {
            0: "",
            1: "Логін",
            2: "Користувач",
            3: "Кв.",
            4: "e-mail",
            5: "Дата ств.",
            6: "Підтв.",
            7: "Актив.",
            8: "Чл.кооп.",
            }
        return cap

    def get_model_id_name(self, u):
        """
        Визначає назву моделі та id примірника u
        :param u: примірник моделі
        :return: {'id': u.id, 'model': m, 'name': name}
        """
        try:
            m_id_n = {
                    'id'    : str(u.id),
                    'model' : u._meta.model_name,
                    'name'  : u.username,
                    }
        except:
            m_id_n = {}
        return m_id_n

    def get_row(self, u):
        """
        Визначає один рядок у двомірному масиві даних таблиці.
        Формат рядка:
         row[j] - елемент словника row = {...},
         де j - номер колонки в таблиці (поч. з 1)
            row[0] - словник з даними про примірник:
                        {'id': f.id, 'model': m}
        :param u: примірник user
        :return row: одновимірний масив
        """
        if u:
            row = {}
            row[0] = self.get_model_id_name(u)
            row[1] = u.username
            row[2] = get_user_full_name(u)
            row[3] = get_user_flat_No(u)
            row[4] = u.email
            # row[5] = u.date_joined.isoformat() if u.date_joined else ""
            row[5] = u.date_joined if u.date_joined else ""
            row[6] = get_user_is_recognized(u)
            row[7] = u.is_active
            row[8] = has_group(u, 'members')
        else: # елемента нема => рядок таблиці має бути None
            row = None
        return row

    def get_supplement_data(self, u):
        # додаткові дані для передачі в шаблон через XHR,
        # які простіше отримати в Python і використати в js
        # для зміни / створення нового рядка в таблиці
        if u:
            row = self.get_row(u)
            data = {}
            iconPath = {}
            for j in [6, 7, 8]:
                iconPath[j] = STATIC_URL + icon_yes_no_unknown(row[j])
            data['iconPath'] = iconPath
        else:
            data = None
        return data


class UsersTable(ListView):
    model = User
    template_name = 'koop_adm_users_table.html'

    @method_decorator(permission_required('koopsite.activate_account'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Материнська тека
        context = super().get_context_data(**kwargs)
        browTabName = 'users_table'    # назва таблиці (для сесії і ajax)
        # Беремо з сесії масив параметрів виділеного елемента
        # parent_id='' у даному випадку
        selElement = getSelElementFromSession(self.request.session,
                                            browTabName)
        selElementModel = selElement.get('model')
        selElementID    = selElement.get('id')
        if selElementModel and selElementID:
            # відомі параметри виділеного рядка
            sel_model_id = {'id': selElementID, 'model': selElementModel}
        else:
            # вперше відвідуємо цю таблицю
            sel_model_id = {}
        # TODO-використати цей фрагмент для новостворених словників/ключів
        # if self.session_id is not None:
        #     if not params:
        #         params = {'sessionId': self.session_id}
        #     elif 'sessionId' not in params:
        #         params['sessionId'] = self.session_id

        # Готуємо 2D-масив всіх даних таблиці
        # Одночасно шукаємо порядковий номер виділеного рядка
        bta = UsersTableArray()
        arr, sel_index = bta.get_qs_array(self.qs, sel_model_id)
        cap = bta.get_table_headers()

        # Значення передадуться в шаблон:
        context['browTabName']      = browTabName

        context['selRowIndex']      = sel_index
        context['selElementModel']  = sel_model_id.get('model')
        context['selElementID']     = sel_model_id.get('id')

        context['cap'] = cap    # список заголовків таблиці
        context['arr'] = arr    # 2D-масив даних таблиці:

        # Одночасно передаємо цей же 2D-масив для обробки js.
        # Але дату в ньому необхідно перетворити в isoformat,
        # прийнятний для JSON.
        j_arr = deepcopy(arr)   # arr - змінюваний об'єкт!
        for i in j_arr:
            if j_arr[i][5]: j_arr[i][5] = j_arr[i][5].isoformat()
        json_arr = json.dumps(j_arr)
        context['json_arr'] = json_arr

        # Записуємо в сесію:
        selElement['selRowIndex'] = sel_index
        selElement['model']       = sel_model_id.get('model')
        selElement['id']          = sel_model_id.get('id')
        setSelElementToSession(self.request.session,
                                            browTabName,
                                            selElement=selElement)
        return context

    def get_queryset(self):
        self.qs = User.objects.all().order_by('username'.lower())
        # Якщо авторизований користувач не належить до групи staff,
        # то він не може бачити тих, хто належить ТІЛЬКИ до staff:
        if not self.request.user.is_staff:
            self.qs = [u for u in self.qs if not is_staff_only(u)]
        return self.qs


#################################################################
# jQuery ajax base class for single Account:
#################################################################

class AjaxAccountViewBase(View):
    """
    CBV - базовий суперклас для обробки AJAX-запитів з таблиці.
    Від класу View використовується:
        метод as_view() - для виклику в urls.py,
        метод dispatch - для декорування в субкласах.
    Метод dispatch повністю замінений викликом функції handler
    Метод dispatch декорується у дочірніх класах.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.msg = types.SimpleNamespace(title   = "",
                                        type    = "",
                                        message = "",
                                        )
        self.sendMail = False

    def dispatch(self, request, *args, **kwargs):
        return self.handler(request)


    def handler(self, request):
        if 'client_request' in request.POST:
            # Розбираємо дані від клієнта:
            user, profile = self.get_request_data(request)
            if not user:
                print("There is no user in request.POST")
                return HttpResponseBadRequest("There is no user in request.POST")
            # Елемент - рядок таблиці ДО змін:
            old_element = UsersTableArray().get_row(user)

            user, msg = self.processing(user, profile, self.msg)

            # Елемент - рядок таблиці ПІСЛЯ змін (якщо були):
            new_element = UsersTableArray().get_row(user)
            # Зміни рядка в таблиці:
            if msg.type == msgType.NewRow:
                changes = new_element
            else:
                changes = UsersTableArray().get_cell_changes(old_element,
                                                             new_element)
            supplement = UsersTableArray().get_supplement_data(user)
            # Формуємо словник для передачі в шаблон через XHR:
            response_cont = vars(msg)
            response_cont['changes'] = changes
            response_cont['supplement'] = supplement
            # Посилаємо відповідь клієнту:
            # return JsonResponse(response_cont)
            return HttpResponse(json.dumps(response_cont), content_type="application/json")
        else:
            print("There is no 'client_request' in request.POST")
            return HttpResponseBadRequest("There is no 'client_request' in request.POST")

    def get_request_data(self, request):
        # Розбираємо дані від клієнта:
        try:
            d = parseClientRequest(request.POST)
        except ValueError as err:
            # запит від клієнта містить невідповідні дані:
            print('get_request_data:', err.args)
            return None, None
        self.sendMail = d.get('sendMail')
        user_id = d.get('id')                   # id of selected user
        if d.get('model') == "user":
            user = get_or_none(User, id=user_id)    # selected user
            profile = get_or_none(UserProfile, user=user)  # profile
            return user, profile
        else:
            return None, None

    def processing(self, user, profile, msg):
        """
        Цей метод треба переозначити у дочірньому класі.
        Тут наводиться як приклад.
        """
        # Умови при яких зміни не відбудуться:
        if profile and profile.is_recognized == True:
            msg.title   = user.username
            msg.type    = msgType.NoChange
            msg.message = "Акаунт раніше вже був підтверджений!"
        else:
            # Робимо зміни:
            if not profile:
                profile = UserProfile(user=user)
            profile.is_recognized = True
            profile.save()
            user.userprofile = profile
            msg.title       = user.username
            msg.type        = msgType.Change
            msg.message     = "Акаунт підтверджено!"
            e_msg_body = "Ваш акаунт на сайті підтверджено!"
            self.send_e_mail(user, e_msg_body)
        return user, msg

    def send_e_mail(self, user, e_msg_body):
        if self.sendMail:
            email = user.email
            if email:
                subject="KoopSite administrator"
                message = "Шановний %s,\n" \
                        "%s\n" \
                        "З повагою, адміністратор сайта %s\n" \
                        "%s" % (user.username, e_msg_body,
                                SITE_ADDRESS, EMAIL_HOST_USER)
                send_mail(subject, message, EMAIL_HOST_USER, [email])


#################################################################
# jQuery ajax CBV for single Account:
#################################################################

class AjaxRecognizeAccount(AjaxAccountViewBase):
    """
    Підтвердження акаунту.
    """
    # raise_exception=True - для ajax. Виняток обробить xhrErrorHandler (js).
    @method_decorator(permission_required('koopsite.activate_account', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def processing(self, user, profile, msg):
        # Умови при яких зміни не відбудуться:
        if profile and profile.is_recognized == True:
            msg.title   = user.username
            msg.type    = msgType.NoChange
            msg.message = "Акаунт раніше вже був підтверджений!"
        else:
            # Робимо зміни:
            if not profile:
                profile = UserProfile(user=user)
            profile.is_recognized = True
            profile.save()
            user.userprofile = profile
            msg.title   = user.username
            msg.type    = msgType.Change
            msg.message = "Акаунт підтверджено!"
            e_msg_body = "Ваш акаунт на сайті підтверджено!"
            self.send_e_mail(user, e_msg_body)
        return user, msg


class AjaxDenyAccount(AjaxAccountViewBase):
    """
    Підтвердження акаунту.
    """
    @method_decorator(permission_required('koopsite.activate_account', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def processing(self, user, profile, msg):
        # Умови при яких зміни не відбудуться:
        if profile and profile.is_recognized == False:
            msg.title   = user.username
            msg.type    = msgType.NoChange
            msg.message = "Акаунт раніше вже був відхилений!"
        else:
            # Робимо зміни:
            if not profile:
                profile = UserProfile(user=user)
            profile.is_recognized = False
            profile.save()
            user.userprofile = profile
            user.is_active = False
            user.save()
            msg.title   = user.username
            msg.type    = msgType.Change
            msg.message = "Акаунт відхилено і деактивовано!"
            e_msg_body = "Ваш акаунт на сайті відхилено і деактивовано."
            self.send_e_mail(user, e_msg_body)
        return user, msg


class AjaxActivateAccount(AjaxAccountViewBase):
    """
    Активація акаунту.
    """
    @method_decorator(permission_required('koopsite.activate_account', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def processing(self, user, profile, msg):
        # Умови при яких зміни не відбудуться:
        if user.is_active:
            msg.title   = user.username
            msg.type    = msgType.NoChange
            msg.message = "Акаунт вже активний!"
        elif profile and profile.is_recognized == False:
            msg.title   = user.username
            msg.type    = msgType.Error
            msg.message = "Відхилений Акаунт не можна активувати!"
        else:
            # Робимо зміни:
            user.is_active = True
            user.save()
            msg.title   = user.username
            msg.type    = msgType.Change
            msg.message = "Акаунт активовано!"
            e_msg_body = "Ваш акаунт на сайті активовано."
            self.send_e_mail(user, e_msg_body)
        return user, msg


class AjaxDeactivateAccount(AjaxAccountViewBase):
    """
    Деактивація акаунту.
    """
    @method_decorator(permission_required('koopsite.activate_account', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def processing(self, user, profile, msg):
        # Умови при яких зміни не відбудуться:
        if not user.is_active:
            msg.title   = user.username
            msg.type    = msgType.NoChange
            msg.message = "Акаунт вже неактивний!"
        else:
            # Робимо зміни:
            user.is_active = False
            user.save()
            msg.title   = user.username
            msg.type    = msgType.Change
            msg.message = "Акаунт деактивовано!"
            e_msg_body = "Ваш акаунт на сайті деактивовано."
            self.send_e_mail(user, e_msg_body)
        return user, msg


class AjaxSetMemberAccount(AjaxAccountViewBase):
    """
    Додавання користувача до групи 'members'.
    """
    @method_decorator(permission_required('koopsite.activate_account', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def processing(self, user, profile, msg):
        # Умови при яких зміни не відбудуться:
        if has_group(user, 'members'):
            msg.title   = user.username
            msg.type    = msgType.NoChange
            msg.message = "Акаунт вже має ці права доступу!"
        elif profile and profile.is_recognized == False:
            msg.title   = user.username
            msg.type    = msgType.Error
            msg.message = "Відхилений Акаунт не може отримати права доступу!"
        elif (not profile) or (profile and profile.is_recognized == None):
            msg.title   = user.username
            msg.type    = msgType.Error
            msg.message = "Непідтверджений Акаунт не може отримати права доступу!"
        else:
            # Робимо зміни:
            add_group(user, 'members')
            user.save()
            msg.title   = user.username
            msg.type    = msgType.Change
            msg.message = "Права доступу встановлено!"
            e_msg_body = "Ваш акаунт на сайті отримав права доступу " \
                         "члена кооперативу."
            self.send_e_mail(user, e_msg_body)
        return user, msg


class AjaxDenyMemberAccount(AjaxAccountViewBase):
    """
    Видалення користувача з групи 'members'.
    """
    @method_decorator(permission_required('koopsite.activate_account', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def processing(self, user, profile, msg):
        # Умови при яких зміни не відбудуться:
        if not has_group(user, 'members'):
            msg.title   = user.username
            msg.type    = msgType.NoChange
            msg.message = "Акаунт вже позбавлений цього права доступу!"
        else:
            # Робимо зміни:
            remove_group(user, 'members')
            user.save()
            msg.title   = user.username
            msg.type    = msgType.Change
            msg.message = "Право доступу вилучено!"
            e_msg_body = "Ваш акаунт на сайті позбавлений права доступу " \
                         "члена кооперативу."
            self.send_e_mail(user, e_msg_body)
        return user, msg


class AjaxDeleteAccount(AjaxAccountViewBase):
    """
    Видалення акаунту.
    """
    @method_decorator(permission_required('auth.delete_user', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def processing(self, user, profile, msg):
        # Умови при яких зміни не відбудуться:
        if user.is_active:
            msg.title   = user.username
            msg.type    = msgType.Error
            msg.message = "Активний акаунт не можна видалити!"
        elif (not profile) or (profile.is_recognized != False):
            msg.title   = user.username
            msg.type    = msgType.Error
            msg.message = "Видалити можна лише відхилений акаунт!"
        else:
            # Робимо зміни:
            msg.title   = user.username
            profile.delete()
            user.delete()
            msg.type    = msgType.DeleteRow
            msg.message = "Акаунт видалено!"
            # msg.message = "Акаунт НЕ видалено (DEBUGGING)!"
            e_msg_body = "Ваш акаунт на сайті видалено."
            # TODO-як відправити email на видалений акаунт?
            # self.send_e_mail(user, e_msg_body)
            user = None
        return user, msg
        # return None, msg


#################################################################
# jQuery ajax base class for GROUP of Accounts:
#################################################################

class AjaxAllAccountsViewBase(View):
    """
    CBV - базовий суперклас для обробки AJAX-запитів з таблиці.
    Від класу View використовується:
        метод as_view() - для виклику в urls.py,
        метод dispatch - для декорування в субкласах.
    Метод dispatch повністю замінений викликом функції handler
    Метод dispatch декорується у дочірніх класах.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.empty_msg = types.SimpleNamespace(title   = "",
                                        type    = "",
                                        message = "",
                                        )
        self.group_msg = deepcopy(self.empty_msg)
        self.sendMail = False
        self.init_counter()

    def init_counter(self):
        self.group_msg.title   = "Активація групи акаунтів"
        self.group_msg.type    = msgType.Group
        self.group_msg.message = ""
        self.counter = OrderedDict()
        self.counter["активовано"    ] = 0
        self.counter["вже активні"   ] = 0
        self.counter["відхилені"     ] = 0
        self.counter["непідтверджені"] = 0

    def dispatch(self, request, *args, **kwargs):
        return self.group_handler(request)

    def group_handler(self,request):
        if 'client_request' in request.POST:
            # Розбираємо дані від клієнта:
            users_set = self.get_request_data_set(request)

            # Перевіряємо і вносимо зміни у всі елементи.
            group_response_set = self.group_processing(users_set)

            # Формуємо словник для передачі в шаблон через XHR:
            pattern = '<tr><td>%20s:</td><td>%3s</td></tr>'
            s = pattern % ('Оброблено акаунтів', len(users_set))
            for k, v in self.counter.items():
                s += pattern % (k, v)
            self.group_msg.message = s
            group_response_cont = vars(self.group_msg)
            group_response_cont['group'] = group_response_set
            # Посилаємо відповідь клієнту:
            # return JsonResponse(group_response_cont)
            return HttpResponse(json.dumps(group_response_cont), content_type="application/json")
        else:
            print("There is no 'client_request' in request.POST")
            return HttpResponse()
            # return render(self, request, self.no_request_template)

    def get_request_data_set(self, request):
        # Розбираємо дані від клієнта:
        try:
            d = parseClientRequest(request.POST)
        except ValueError as err:
            # запит від клієнта містить невідповідні дані:
            print('get_request_data_set:', err.args)
            return None
        browTabName = d.get('browTabName')
        if browTabName != 'users_table':
            return None
        self.sendMail = d['sendMail']
        elemSet = d.get('elemSet')
        users_set = []
        if elemSet:
            for elem in elemSet:
                model = elem.get('model')
                if model:
                    if model not in get_browTabName_models().get(browTabName):
                        print('Error data in request.POST: model name in elemSet does not correspond to table name', model, browTabName)
                        return None
                if model == "user":
                    user_id = elem.get('id')
                    user = get_or_none(User, id=user_id)    # selected user
                    if user:
                        users_set.append(user)
        return users_set

    def group_processing(self, users_set):
        response_set = []
        for user in users_set:
            msg = deepcopy(self.empty_msg)
            profile = get_or_none(UserProfile, user=user)  # profile
            # Елемент - рядок таблиці ДО змін:
            old_element = UsersTableArray().get_row(user)

            # dict_print(old_element, 'old_element')

            user, msg = self.processing(user, profile, msg)

            # Елемент - рядок таблиці ПІСЛЯ змін (якщо були):
            new_element     = UsersTableArray().get_row(user)

            # dict_print(new_element, 'new_element')

            # Зміни рядка в таблиці:
            if msg.type == msgType.NewRow:
                changes = new_element
            else:
                changes = UsersTableArray().get_cell_changes(old_element,
                                                             new_element)
            supplement = UsersTableArray().get_supplement_data(user)
            # Формуємо словник для передачі в шаблон через XHR:
            response_cont = vars(msg)
            response_cont['model'] = user._meta.model_name
            response_cont['id'] = str(user.id)
            response_cont['changes'] = changes
            response_cont['supplement'] = supplement
            response_set.append(response_cont)
        return response_set

    def processing(self, user, profile, msg):
        """
        Цю функцію треба переозначити у дочірньому класі.
        Тут наводиться як приклад.
        """
        # Умови при яких зміни не відбудуться:
        if user.is_active:
            msg.title   = user.username
            msg.type    = msgType.NoChange
            msg.message = "Акаунт вже активний!"
            self.counter["вже активні"] += 1
        elif profile and profile.is_recognized == False:
            msg.title   = user.username
            msg.type    = msgType.Error
            msg.message = "Відхилений Акаунт не можна активувати!"
            self.counter["відхилені"] += 1
        elif (not profile) or (profile and profile.is_recognized == None):
            msg.title   = user.username
            msg.type    = msgType.Error
            msg.message = "Непідтверджений Акаунт не можна активувати!"
            self.counter["непідтверджені"] += 1
        else:
            # Робимо зміни:
            user.is_active = True
            user.save()
            msg.title   = user.username
            msg.type    = msgType.Change
            msg.message = "Акаунт активовано!"
            self.counter["активовано"] += 1
        return user, msg

    # TODO-2016 02 01 Ф-ція send_e_mail двічі описана у цьому файлі: DRY!
    def send_e_mail(self, user, e_msg_body):
        if self.sendMail:
            email = user.email
            if email:
                subject="KoopSite administrator"
                message = "Шановний %s,\n" \
                        "%s\n" \
                        "З повагою, адміністратор сайта %s\n" \
                        "%s" % (user.username, e_msg_body,
                                SITE_ADDRESS, EMAIL_HOST_USER)
                send_mail(subject, message, EMAIL_HOST_USER, [email])



#################################################################
# jQuery ajax CBV for GROUP of Accounts:
#################################################################

class AjaxActivateAllAccounts(AjaxAllAccountsViewBase):
    """
    Активація всіх акаунтів з фільтрованого списку.
    """
    def init_counter(self):
        self.group_msg.title   = "Активація групи акаунтів"
        self.group_msg.type    = msgType.Group
        self.group_msg.message = ""
        self.counter = OrderedDict()
        self.counter["активовано"    ] = 0
        self.counter["вже активні"   ] = 0
        self.counter["відхилені"     ] = 0
        self.counter["непідтверджені"] = 0

    @method_decorator(permission_required('koopsite.activate_account', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return self.group_handler(request)

    def processing(self, user, profile, msg):
        # Умови при яких зміни не відбудуться:
        if user.is_active:
            msg.title   = user.username
            msg.type    = msgType.NoChange
            msg.message = "Акаунт вже активний!"
            self.counter["вже активні"] += 1
        elif profile and profile.is_recognized == False:
            msg.title   = user.username
            msg.type    = msgType.Error
            msg.message = "Відхилений Акаунт не можна активувати!"
            self.counter["відхилені"] += 1
        elif (not profile) or (profile and profile.is_recognized == None):
            msg.title   = user.username
            msg.type    = msgType.Error
            msg.message = "Непідтверджений Акаунт не можна активувати!"
            self.counter["непідтверджені"] += 1
        else:
            # Робимо зміни:
            user.is_active = True
            user.save()
            msg.title   = user.username
            msg.type    = msgType.Change
            msg.message = "Акаунт активовано!"
            self.counter["активовано"] += 1
            e_msg_body = "Ваш акаунт на сайті активовано!"
            self.send_e_mail(user, e_msg_body)
        return user, msg


class AjaxSetMemberAllAccounts(AjaxAllAccountsViewBase):
    """
    Приєднання до групи members всіх акаунтів з фільтрованого списку.
    """
    def init_counter(self):
        self.group_msg.title   = "Надання права доступу групі акаунтів"
        self.group_msg.type    = msgType.Group
        self.group_msg.message = ""
        self.counter = OrderedDict()
        self.counter["встановлено"   ] = 0
        self.counter["доступ вже є"  ] = 0
        self.counter["відхилені"     ] = 0
        self.counter["непідтверджені"] = 0

    @method_decorator(permission_required('koopsite.activate_account', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return self.group_handler(request)

    def processing(self, user, profile, msg):
        # Умови при яких зміни не відбудуться:
        if has_group(user, 'members'):
            msg.title   = user.username
            msg.type    = msgType.NoChange
            msg.message = "Акаунт вже має ці права доступу!"
            self.counter["доступ вже є"] += 1
        elif profile and profile.is_recognized == False:
            msg.title   = user.username
            msg.type    = msgType.Error
            msg.message = "Відхилений Акаунт не може отримати права доступу!"
            self.counter["відхилені"] += 1
        elif (not profile) or (profile and profile.is_recognized == None):
            msg.title   = user.username
            msg.type    = msgType.Error
            msg.message = "Непідтверджений Акаунт не може отримати права доступу!"
            self.counter["непідтверджені"] += 1
        else:
            # Робимо зміни:
            add_group(user, 'members')
            user.save()
            msg.title   = user.username
            msg.type    = msgType.Change
            msg.message = "Права доступу встановлено!"
            self.counter["встановлено"] += 1
            e_msg_body = "Ваш акаунт на сайті отримав права доступу " \
                         "члена кооперативу."
            self.send_e_mail(user, e_msg_body)
        return user, msg


#---------------- Кінець коду, охопленого тестуванням ------------------
