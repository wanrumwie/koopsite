import json
import types
from django.http.response import HttpResponse, HttpResponseBadRequest
from koopsite.functions import  getSelElementFromSession, \
                        setSelElementToSession, \
                        parseClientRequest, dict_print

# Константа для типів повідомлення,
# яке сервер посилає клієнту через AJAX:
msgType = types.SimpleNamespace(
                Change        = "Change",
                DeleteRow     = "DeleteRow",
                Error         = "Error",
                Forbidden     = "Forbidden",
                IncorrectData = "IncorrectData",
                MoveElement   = "MoveElement",
                NewRow        = "NewRow",
                NoChange      = "NoChange",
                Normal        = "Normal",
                Rename        = "Rename",
                Group         = "Group",
                )

#################################################################
# jQuery ajax functions:
#################################################################

def ajaxSelRowIndexToSession(request):
    if 'client_request' in request.POST:
        # Розбираємо дані від клієнта:
        try:
            d = parseClientRequest(request.POST)
        except ValueError as err:
            # запит від клієнта містить невідповідні дані:
            print('ajaxSelRowIndexToSession:', err.args)
            s = 'ajaxSelRowIndexToSession: %s %s %s' % err.args
            return HttpResponseBadRequest(s)
        browTabName = d.get('browTabName')
        parent_id   = d.get('parent_id')
        # Формуємо дані для зберігання в сесії:
        selElement = {}
        selElement['model'      ] = d.get('model'      )
        selElement['id'         ] = d.get('id'         )
        selElement['selRowIndex'] = d.get('selRowIndex')
        # Записуємо в сесію:
        setSelElementToSession(request.session,
                                            browTabName=browTabName,
                                            parent_id=parent_id,
                                            selElement=selElement)
        # Посилаємо відповідь клієнту:
        response_dict = {'server_response': selElement }
        # return JsonResponse(response_dict)    # дає помилку в pythonanywhere.com
        return HttpResponse(json.dumps(response_dict), content_type="application/json")
    else:
        return HttpResponseBadRequest("ajaxSelRowIndexToSession: "
                                      "No 'client_request' in request.POST")

def ajaxStartRowIndexFromSession(request):
    if 'client_request' in request.POST:
        # Розбираємо дані від клієнта:
        try:
            d = parseClientRequest(request.POST)
        except ValueError as err:
            # запит від клієнта містить невідповідні дані:
            print('ajaxStartRowIndexFromSession:', err)
            s = 'ajaxStartRowIndexFromSession: %s %s %s' % err.args
            return HttpResponseBadRequest(s)
        browTabName = d.get('browTabName')
        parent_id   = d.get('parent_id')
        # Беремо з сесії масив параметрів виділеного елемента
        # для даної таблиці і для даного parent_id (якщо є):
        selElement = getSelElementFromSession(request.session,
                                            browTabName=browTabName,
                                            parent_id=parent_id)
        # Посилаємо відповідь клієнту:
        response_dict = {'server_response': selElement }
        # return JsonResponse(response_dict)    # дає помилку в pythonanywhere.com
        return HttpResponse(json.dumps(response_dict), content_type="application/json")
    else:
        return HttpResponseBadRequest("ajaxStartRowIndexFromSession: "
                                      "No 'client_request' in request.POST")



#################################################################
# Базовий клас для формування 2D таблиці, яка поступає в шаблон
# одночасно з синхронним рендерингом, і дозволяє оперативно
# змінювати дані з допомогою jQuery ajax:
# Виклик:
# bta = BrowseTableArray()
# qs_array, sel_index = bta.get_qs_array(qs, sel_model_id)
# qs_array            = bta.get_qs_array(qs)
# headers = bta.get_table_headers()
#################################################################

class BrowseTableArray():
    columnsNumber   = 8        # number of columns in table

    def get_qs_array(self, qs, sel_model_id = None):
        """
        Визначає двомірний масив даних таблиці.
        Цей масив передається в шаблон синхронно при відкритті таблиці.
        Масив зберігається в невидимому полі шаблону
        і використовується для сортування таблиці
        (а також перейменування, додавання, видалення елементів)
        без перезавантаження сторінки.
        Формат масиву:
         arr[i][j] ,
         де i - номер рядка в таблиці (поч. з 0)
            j - номер колонки в таблиці (поч. з 1)
            arr[i][0] - словник з даними про примірник:
                        {'id': u.id, 'model': m, 'name': name}
        :param qs: queryset - послідовність примірників user
        :param sel_model_id: {'id': f.id, 'model': m} параметри вибраного рядка
        :return arr: 2D-масив значень таблиці + службова 0-ва колонка
        :return sel_index: порядковий номер вибраного рядка
        """
        # Власне таблиця (з службовою колонкою j=0)
        arr = {}
        if sel_model_id:        # є параметри пошуку => треба шукати
            need_search = True
        else:                   # вибириємо 0 => шукати не треба
            need_search = False
        sel_index = 0           # зміниться, якщо буде знайдено
        i = 0
        for u in qs:
            row = self.get_row(u)
            arr[i] = row
            if need_search:
                if (sel_model_id.get('id'   ) == row.get(0).get('id'   )) and \
                   (sel_model_id.get('model') == row.get(0).get('model')):
                    sel_index = i           # знайдено
                    need_search = False
            i += 1
        if sel_model_id != None:        # були параметри пошуку
            return arr, sel_index
        else:                   # параметрів пошуку не було
            return arr

    def get_table_headers(self):
        # Цей метод потрібно переозначити в дочірньому класі
        # Шапка таблиці для кожної колонки, починаючи з 1.
        # Нульова колонка - службова
        cap = {}
        cap[0] = ""
        cap[1] = "Name"
        return cap

    # Всі наступні методи можуть працювати незалежно від створення
    # таблиці qs_array і дозволяють працювати з окремими примірниками
    # класів (напр. Users, Folder, Report)
    # Виклик (наприклад):
    # changes = BrowseTableArray.get_cell_changes(old, new):

    def get_row(self, u):
        # Цей метод потрібно переозначити в дочірньому класі
        """
        Визначає один рядок у двомірному масиві даних таблиці.
        Формат рядка:
         row - словник {j: val},
         де j - номер колонки в таблиці (поч. з 1)
            val - значення j-ї клітинки
         Службове поле:
            row[0] - словник з даними про примірник:
                        {'id': u.id, 'model': m, 'name': name}
        :param u: примірник user
        :return row: одновимірний словник
        """
        if u:
            row = {}
            row[0] = self.get_model_id_name(u)
        else: # елемента нема => рядок таблиці має бути None
            row = None
        return row

    def get_model_id_name(self, u):
        # Цей метод потрібно переозначити в дочірньому класі
        """
        Визначає назву моделі та id примірника u
        :param u: примірник моделі
        :return: {'id': u.id, 'model': m, 'name': name}
        """
        try:
            m = u._meta.model_name
            m_id_n = {
                'id'    : str(u.id),
                'model' : m,
                'name'  : "%s" % u
                }
        except:
            m_id_n = {}
        return m_id_n

    def get_cell(self, u, col):
        """
        Визначає одну клітинку у двомірному масиві даних таблиці.
        :param u: примірник user
        :param col: номер колонки в таблиці (поч. з 1)
        :return cell: вміст клітинки
        """
        row = self.get_row(u)
        cell = row.get(col)
        return cell

    def get_cell_changes(self, old, new):
        """
        Визначає змінені клітинки в одному рядку таблиці
        шляхом порівняння старого рядка з новим
        Формат рядка:
         row[j] ,
         де j - номер колонки в таблиці (поч. з 1)
            row[0] - словник з даними про примірник:
                        {'id': f.id, 'model': m}
        :param old: старий рядок таблиці
        :param new: змінений рядок
        :return changes: словник {j: new[j], ...}
                         для всіх колонок із зміненим значенням
        """
        # print('old=', old)
        # print('new=', new)
        if new:
            changes = {}        # тут будуть змінені значення
            n = self.columnsNumber + 1 # к-сть колонок (вкл. з нульовою)
            for j in range(n):
                if j == 0:      # нульовий елемент беремо без перевірки
                    changes[j] = new.get(j)
                else:
                    if old.get(j) != new.get(j): # знайдено змінений елемент
                        changes[j] = new.get(j)
        else: # нового рядка немає
            changes = None
        return changes

    def get_supplement_data(self, f):
        # Цей метод потрібно переозначити в дочірньому класі
        # Повертає додаткові дані для передачі в шаблон через XHR,
        # які простіше отримати в Python і використати в js
        # для зміни / створення нового рядка в таблиці
        data = {}
        return data

#---------------- Кінець коду, охопленого тестуванням ------------------

