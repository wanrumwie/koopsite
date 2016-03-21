from fnmatch import fnmatch
import json
import os
import re
import string
from urllib.parse import unquote
from django.contrib.auth.models import Group, Permission
from django.core.mail import send_mail
from math import ceil
from PIL import Image
from flats.models import Flat
from koopsite.fileExtIconPath import get_iconPath
from koopsite.settings import EMAIL_HOST_USER, TRACE_CONDITION


def trace_print(*args):
    """
    Умовний друк, залежно від значення параметра TRACE_CONDITION з settings.py
    :param args:
    :return:
    """
    if TRACE_CONDITION:
        print(*args)

def list_print(list, name=''):
    print(name, 'len =', len(list))
    for i in list: print(i)

def dict_print(d, name='', *args):
    if d:
        try:    length = len(d)
        except: length = len(d.__dict__)
        print(name, 'len =', length, *args)
        try: # d - готовий словник:
            for k, v in sorted(d.items()): print('%-20s : %s' % (k, v))
        except:
            try: # перетворимо d у словник:
                for k, v in sorted(d.__dict__.items()): print('%-20s : %s' % (k, v))
            except:
                print('Error in dict_print() with args:', d, name, *args)
    else:
        print(name, d)

def user_permissions_print(user):
    print('='*50)
    print('user:', user)
    print('-'*50)
    print('get_all_permissions:')
    user_permissions = user.get_all_permissions()
    for p in sorted(user_permissions):
        print(p)
    print('-'*50)
    print('groups:')
    for g in user.groups.all():
        print(g.name)
    print('-'*50)
    print('Permission.objects.all():')
    for p in Permission.objects.all():
        print('%-30s %-20s %-20s %s' % (p.name, p.content_type, p.codename, p))
    print('-'*50)


def dict_from_json_str_or_bytes(json_str):
    """
    Допоміжна функція: перетворює json-стрічку в словник
    Відтворює аналогічну процедуру, яку виконує ф-ція ajax.js
    Використовується в тестах для перевірки правильності формування
    відповіді сервера
    :param json_str: json-string або byte
    :return: d - словник
    """
    if isinstance(json_str, bytes):
        json_str = json_str.decode()
    d = json.loads(json_str)
    return d

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
    except ValueError:
        return None

def round_up_division(a, b):
    """
    :param a: чисельник
    :param b: знаменник
    :return: частка, заокруглена до більшого цілого
    """
    r = ceil(float(a)/b)
    return r

def get_iconPathForFolder(openFlag=False):
    if openFlag: p = 'img/open_folder.png'
    else:        p = 'img/folder.png'
    return p

def get_iconPathByFileExt(ext):
    p = get_iconPath().get(ext)
    if not p: p = "_page.png"
    directory = 'img/file-icons/32px/'
    p = directory + p
    return p

def fileNameCheckInsert(fileName, fileNameList):
    '''
    Функція для визначення нового імені файла при його завантаженні
    Повне ім'я файла порівнюється із списком наявних імен.
    При співпадінні ім'я файла (перед розширенням) доповнюється
    номером копії у дужках, наприклад "qwerty (1).py"
    Якщо виявиться, що подібні назви вже існуть, буде знайдено
    найбільший номер копії, наприклад "qwerty (3).py"
    Функція повертає нову або стару назву файла
    а також доповнює змінюваний список файлів.
    '''
    if fileName in fileNameList:
        (name, ext) = os.path.splitext(fileName)
        pattern = '\((?P<xxx>\d+)\)'.join((re.escape(name+" "), re.escape(ext)))
        pattern = re.compile(pattern)
        i = 0
        for f in fileNameList:
            s = re.search(pattern, f)
            if s:
                j = int(s.group('xxx'))
                i = max(i,j)
        s = " (%s)" % (i+1)
        fileName = s.join((name, ext))
    fileNameList.append(fileName)
    return fileName

def scale_height(width, height, hmax):
    if height > hmax or hmax == 0:
        ratio = hmax*1./height if height != 0 else 0
        width = int(width*ratio)
        height = int(height*ratio)
    return (width, height)

def scale_width(width, height, wmax):
    if width > wmax or wmax == 0:
        ratio = wmax*1./width if width != 0 else 0
        width = int(width*ratio)
        height = int(height*ratio)
    return (width, height)

def get_emptyElement():
    emptyElement = {'model'       : None,
                    'id'          : None,
                    'selRowIndex' : None,
                    }
    return emptyElement

def getSelections(session):
    """
    Отримання даних про виділені елементи всіх таблиць з сесії.
    :param session: request.session
    :return: selections = {parent_id: selElement, ...}
    Формат даних в сесії:
    session = { ... ,
               'Selections':
                    {browTabName:
                         {parent_id:
                             {'model'       : model,
                              'id'          : id,
                              'selRowIndex' : selRowIndex,
                             },
                         },
                    },
               }
    де  browTabName: назва таблиці, напр. 'folders_contents', 'users_list'
        parent_id:  str(Folder.id) - ідентифікатор теки, яка відображається
        model: _meta.model_name - назва моделі виділеного елемента
        id: id виділеного елемента
        selRowIndex: порядковий номер виділеного елемента в таблиці
    """
    # Пробуємо отримати значення з сесії:
    selections = session.get('Selections')
    trace_print('getSelections: session =', session.items())
    if (not selections) or (type(selections) != type({})):
        # якщо selections не існує або не є словником,
        # створюємо новий порожній словник:
        selections      = {}
        # Записуємо в сесію:
        session['Selections'] = selections
    return selections

def getSelElementFromSession(session, browTabName, parent_id=''):
    """
    Отримання параметрів виділеного елемента таблиці folder_content
    з даних сесії.
    :param session: request.session
    :param browTabName: назва таблиці, у якій виділено елемент
    :param parent_id: ідентифікатор теки (якщо є),
                      яка відображається в таблиці
    :return selElement: словник з параметрами виділеного елемента
                { 'model'       : model,
                  'id'          : id,
                  'selRowIndex' : selRowIndex,
                } для теки з parent_id в таблиці browTabName
    """
    parent_id = str(parent_id)  # key in session must be str
    # Пробуємо отримати значення з сесії:
    selections = getSelections(session)
    tableSelections = selections.get(browTabName, {})
    selElement = tableSelections.get(parent_id, get_emptyElement())
    return selElement

def setSelElementToSession(session, browTabName, parent_id='',
                           selElement=get_emptyElement()):
    """
    Запис в сесію параметрів виділеного елемента таблиці folder_content
    :param session: request.session
    :param browTabName: назва таблиці, у якій виділено елемент
    :param parent_id: ідентифікатор теки (якщо є),
                      яка відображається в таблиці
    :param selElement: словник з параметрами виділеного елемента
                { 'model'       : model,
                  'id'          : id,
                  'selRowIndex' : selRowIndex,
                } для теки з parent_id в таблиці browTabName
    """
    parent_id = str(parent_id)  # key in session must be str
    # Пробуємо отримати значення з сесії:
    selections = getSelections(session)
    tableSelections = selections.get(browTabName, {})
    # Встановлюємо нові значення:
    tableSelections[parent_id] = selElement
    selections[browTabName] = tableSelections
    # Записуємо в сесію:
    session['Selections'] = selections

def get_browTabName_models():
    """
    Повертає словник, який пов'язує між собою назви таблиць і моделей.
    Назва таблиці, яка надсилає ajax-запити,
    має корелювати з назвами моделей.
    """
    browTabName_models = {
            'folders_contents'  : ('folder', 'report', ),
            'users_table'       : ('user',),
            }
    return browTabName_models

def parseClientRequest(requestPOST):
    """
    Розбираємо запит від клієнта
    :param requestPOST: request.POST
    :return  d: одновимірний словник
    Формат запиту від клієнта:
    {'client_request' : json_s}
    json_s --> розкодування --> d - словник з даними про материнську
                                    теку і виділений елемент
    Формат d: { 'browTabName'   : browTabName,
                'parent_id'     : parent_id,
                'model'         : model,
                'id'            : id,
                'selRowIndex'   : selRowIndex,
                'name'          : name,
               }
    Кожна ф-ція ajax...view (.py) витягне з цього словника необхідні дані,
    в тому числі і якщо ajax... (.js) пошле додатковий елемент,
    що не входить до "стандартного" набору keys.
    """
    # Отримуємо запит з даними від клієнта:
    json_s = requestPOST['client_request']
    # Розкодовуємо стрічку JSON в звичайний словник
    d = json.loads(json_s)
    browTabName = d.get('browTabName')
    model       = d.get('model')
    # Перевіряємо правильність вхідних даних і при потребі
    #    активуємо помилку яку відслідкуємо у викликаючій процедурі
    # Назва таблиці повинна бути в запиті
    if not browTabName:
        raise ValueError('\n Bad data in request.POST: no table name',
                         '\n model=%s' % model,
                         '\n browTabName=%s' % browTabName)
    # Назва таблиці повинна бути в словнику browTabName_models
    if browTabName not in get_browTabName_models():
        raise ValueError('\n Bad data in request.POST: unknown table name',
                         '\n model=%s' % model,
                         '\n browTabName=%s' % browTabName)
    # Якщо є назва моделі, то вона повинна корелювати з назвою таблиці
    if model:
        if model not in get_browTabName_models().get(browTabName):
            raise ValueError('\n Bad data in request.POST: model name does not correspond to table name',
                             '\n model=%s' % model,
                             '\n browTabName=%s' % browTabName)
    # Помилок у вхідних даних немає
    return d

def parseXHRClientRequest(requestMETA):
    """
    Розбираємо xhr запит від клієнта
    :param requestMETA: request.META
    :return:  d - словник з даними про материнську теку і інш.
    Формат запиту від клієнта:
    encoded_json_string знаходиться у заголовку "X-client-request"
    Кожна ф-ція xhr ajax...view витягне з словника d необхідні дані
    """
    # Отримуємо запит з даними від клієнта:
    encoded_json_s = requestMETA.get("HTTP_X_CLIENT_REQUEST")
    # Розкодовуємо в UTF8:
    json_s = unquote(encoded_json_s)
    # Розкодовуємо стрічку JSON в звичайний словник
    d = json.loads(json_s)
    browTabName = d.get('browTabName')
    model       = d.get('model')
    # Перевіряємо правильність вхідних даних і при потребі
    #    активуємо помилку яку відслідкуємо у викликаючій процедурі
    # Назва таблиці повинна бути в запиті
    if not browTabName:
        raise ValueError('\n Bad data in request.META: no table name',
                         '\n model=%s' % model,
                         '\n browTabName=%s' % browTabName)
    # Назва таблиці повинна бути в словнику browTabName_models
    if browTabName not in get_browTabName_models():
        raise ValueError('\n Bad data in request.META: unknown table name',
                         '\n model=%s' % model,
                         '\n browTabName=%s' % browTabName)
    # Якщо є назва моделі, то вона повинна корелювати з назвою таблиці
    if model:
        if model not in get_browTabName_models().get(browTabName):
            raise ValueError('\n Bad data in request.META: model name does not correspond to table name',
                             '\n model=%s' % model,
                             '\n browTabName=%s' % browTabName)
    # Помилок у вхідних даних немає
    return d

def get_namespace_from_dict(d, ns, extend=False):
    """
    Функція, яка заповнює простір імен типу SimpleNameSpace
    даними звичайного словника.
    :param d: словник з даними
    :param ns: простір імен, який слід заповнити
    :param extend: при True простір імен доповнюється ключами з d
    :return: ns - заповнений даними словника простір імен,
            з яким можна оперувати у такий спосіб: ns.key замість d['key']
    """
    if extend:  # namespace will extend by dict fields
        keys = d.keys()
    else:       # namespace will not extend by dict fields
        keys = vars(ns).keys()
    for k in keys:
        vars(ns)[k] = d.get(k)
    return ns

def get_user_full_name(user):
    fn = (x.strip().capitalize() for x in (user.last_name, user.first_name))
    s = ' '.join(fn)
    return s.strip()

def get_user_flat_No(user):
    try:
        s = user.userprofile.flat.flat_No
    except:
        s = ""
    return s

def get_user_is_recognized(user):
    try:
        s = user.userprofile.is_recognized
    except:
        s = ""
    return s

def is_staff_only(user):
    groups = user.groups.all()
    staff  = get_or_none(Group, name='staff')
    return staff in groups and len(groups) == 1

def has_group_members(user):
    return has_group(user, 'members')

def has_group(user, group_name):
    group = get_or_none(Group, name=group_name)
    return group in user.groups.all()

def add_group(user, group_name):
    group = get_or_none(Group, name=group_name)
    user.groups.add(group)

def remove_group(user, group_name):
    group = get_or_none(Group, name=group_name)
    user.groups.remove(group)

def get_flat_users(flat):
    # Повертає список користувачів, у профілях яких вказано цю квартиру
    users_list = []
    if flat and isinstance(flat, Flat):
        for profile in flat.userprofiles.all():
            user = profile.user
            users_list.append(user)
    return users_list

def has_flat_member(flat):
    # Повертає True, якщо серед користувачів, у профілях яких
    # вказано цю квартиру, є користувач з правами доступу "member"
    flag = False
    if flat and isinstance(flat, Flat):
        for profile in flat.userprofiles.all():
            user = profile.user
            if has_group_members(user):
                flag = True
                break
    return flag


class AllFieldsMixin():
    """
    Базовий клас, який робить вибірку ВСІХ полів будь-якого одного
    запису або всіх записів моделі. Методи класу формують дані
    у вигляді списків, зручних до використання в шаблонах.
    Підмішуючи цей клас до CBV і переозначуючи там лише
    get_context_data() можна отримати клас-представлення для всіх
    полів одного запису або всіх полів всіх записів обраної моделі.
    """
    model   = None  # модель слід зазначити у дочірньому класі
    fields  = ()    # Поля, які будуть виведені. Якщо порожній, то всі.
    exclude = ()    # Поля, які виключаються із списку виводу.

    def val_repr(self, v, decimal=2):
        """
        Представлення значення у шаблоні.
        Заокруглює число. Для нуля повертає "".
        У дочірньому класі можна переозначити для специфічних потреб,
        """
        try:    v = round(v, decimal)
        except: pass
        if v == 0: v = ""
        return v

    def get_field_keys_verbnames(self):
        """
        Визначення списку пар: (name, verbose_name) для кожного
          поля моделі self.model. Маючи цей перелік легко отримати
          список значень всіх полів для будь-якого-запису моделі.
        :return keys: список ідентифікаторів полів моделі за мінусом excluded
        :return verb: список людських найменувань полів моделі за мінусом excluded
        """
        keys = []
        verb = []
        if self.fields:
            for k in self.fields:
                if k not in self.exclude:
                    fo = self.model._meta.get_field(k)
                    vn = fo.verbose_name
                    keys.append(k)
                    verb.append(vn)
        else:
            for fo in self.model._meta.fields:
                k = fo.name
                vn = fo.verbose_name
                if k not in self.exclude:
                    keys.append(k)
                    verb.append(vn)
        return keys, verb

    def get_value_list(self, record, keys):
        """
        Отримання списку значень полів
        :param record: об'єкт моделі
        :param keys: список полів, синхронно якому створиться список значень
        :return: values - список значень
        """
        values = []
        for k in keys:
            v = getattr(record, k)
            v = self.val_repr(v, 2)
            values.append(v)
        return values

    def get_label_value_list(self, keys, values):
        """
        Отримання списку, що складається з кортежів (key, value)
        :param keys: список ідентифікаторів полів моделі
        :param values: список значень полів моделі
        :return: [(k, v), ...]
        """
        return [(k, v) for k, v in zip(keys, values)]


def transliterate(s, lang_from='uk', lang_to='en'):
    """
    Функція транслітерації. За промовчанням призначена для
    запису українських літер латинськими за правилами,
    встановленими постановою КМУ від 2010р.
    :param s: вхідна стрічка
    :param lang_from: мова вхідної стрічки
    :param lang_to: мова вихідної стрічки
    :return: транслітерована стрічка
    Параметри мов вставлені на перспективу. Потрібно буде змінити
    значення map, diphthong_map та word_start_map.
    Неукраїнські літери і символи, які не входять до складу
    списку string.printable будуть замінені на символ підкреслення '_'.
    """
    # Загальні правила заміни літер:
    map = {
            'А': 'A',
            'Б': 'B',
            'В': 'V',
            'Г': 'H',
            'Д': 'D',
            'Е': 'E',
            'Ж': 'Zh',
            'З': 'Z',
            'И': 'Y',
            'Й': 'I',
            'К': 'K',
            'Л': 'L',
            'М': 'M',
            'Н': 'N',
            'О': 'O',
            'П': 'P',
            'Р': 'R',
            'С': 'S',
            'Т': 'T',
            'У': 'U',
            'Ф': 'F',
            'Х': 'Kh',
            'Ц': 'Ts',
            'Ч': 'Ch',
            'Ш': 'Sh',
            'Щ': 'Shch',
            'Ь': '',
            'Ю': 'Iu',
            'Я': 'Ia',
            'Є': 'Ie',
            'І': 'I',
            'Ї': 'I',
            'Ґ': 'G',
            'а': 'a',
            'б': 'b',
            'в': 'v',
            'г': 'h',
            'д': 'd',
            'е': 'e',
            'ж': 'zh',
            'з': 'z',
            'и': 'y',
            'й': 'i',
            'к': 'k',
            'л': 'l',
            'м': 'm',
            'н': 'n',
            'о': 'o',
            'п': 'p',
            'р': 'r',
            'с': 's',
            'т': 't',
            'у': 'u',
            'ф': 'f',
            'х': 'kh',
            'ц': 'ts',
            'ч': 'ch',
            'ш': 'sh',
            'щ': 'shch',
            'ь': '',
            'ю': 'iu',
            'я': 'ia',
            'є': 'ie',
            'і': 'i',
            'ї': 'i',
            'ґ': 'g',
    }
    # Правила заміни літер на початку слова:
    word_start_map = {
            'Й': 'Y',
            'Ю': 'Yu',
            'Я': 'Ya',
            'Є': 'Ye',
            'Ї': 'Yi',
            'й': 'y',
            'ю': 'yu',
            'я': 'ya',
            'є': 'ye',
            'ї': 'yi',
    }
    # Правила заміни дифтонгів (в українській мові для цілей
    # транслітерації під дифтонгом розуміється лише буквосполучення 'зг'.
    diphthong_map = {
            'ЗГ': 'ZGh',
            'Зг': 'Zgh',
            'зг': 'zgh',
    }
    if lang_from == 'uk' and lang_to == 'en':
        # Спочатку обробка дифтонгів:
        for a in diphthong_map:
            s = s.replace(a, diphthong_map[a])

        # Обробка початків слів:
        words = s.split()
        for i in range(len(words)):
            word = words[i]
            for a in word_start_map:
                if word.startswith(a):
                    b = word_start_map[a]
                    word = word.replace(a, b, 1)
                    words[i] = word
                    break
        s = ' '.join(words)

        # Обробка основної маси літер:
        trans = []
        for a in s:
            if a in map:
                b = map[a]
            elif not a in string.printable:
                b = '_'
            else:
                b = a
            trans.append(b)
        s = ''.join(trans)
    return s

def get_miniature_path(path, size='30x24'):
    """
    A function to get file name for image miniature
    :param path:    full path of image file
    :param size:    size for thumbnail
    :return:        thumbnail file full path
    """
    filehead, filetail = os.path.split(path)
    basename, format = os.path.splitext(filetail)
    miniature = basename + '_' + size + format
    miniature_path = os.path.join(filehead, miniature)
    return miniature_path

def get_thumbnail_url_path(picture, size='30x24'):
    """
    A function to resize a ImageField on demand, a use case could be:
    <img src="{{ object.image.url }}" alt="original image">
    <img src="{{ object.image|thumbnail }}" alt="image resized to default 104x104 format">
    <img src="{{ object.image|thumbnail:200x300 }}" alt="image resized to 200x300">
    Original http://www.djangosnippets.org/snippets/955/
    :param picture: image object (ImageField instance)
                        or image file path (str)
    :param size:    size for thumbnail
    :return:        thumbnail url, thumbnail file full path
    """
    # defining the size
    x, y = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    if isinstance(picture, str):   # вхідним параметром є url == path (relative)
        filename = picture
        fileurl  = picture
    else:
        filename = picture.path
        fileurl  = picture.url

    filehead, filetail = os.path.split(filename)
    basename, format = os.path.splitext(filetail)
    miniature = basename + '_' + size + format
    miniature_filename = os.path.join(filehead, miniature)

    filehead, filetail = os.path.split(fileurl)
    miniature_url = filehead + '/' + miniature

    # remove a miniature file if miniature is older then main image file:
    if os.path.exists(miniature_filename) and \
            os.path.getmtime(filename) > os.path.getmtime(miniature_filename):
        os.unlink(miniature_filename) # unlink() == remove()
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename):
        try:
            image = Image.open(filename)
            image.thumbnail([x, y], Image.ANTIALIAS)
            try:
                image.save(miniature_filename, image.format, quality=90, optimize=1)
            except:
                image.save(miniature_filename, image.format, quality=90)
        except:
            pass
    return miniature_url, miniature_filename

#---------------- Кінець коду, охопленого тестуванням ------------------



def sendMailToUser(user, subject="KoopSite administrator", message=""):
    email    = user.email
    send_mail(subject, message, EMAIL_HOST_USER, [email])
    # send_mail('Subject', 'Message.', 'from@example.com',
    #             ['john@example.com', 'jane@example.com'])

def CheckPathMatchMediaPattern(path, patt_list=None):
    '''
    Перевірка, чи шлях файла відповідає хоч котромусь із списка шаблонів.
    Використовується у методі save() моделі UserProfile для перевірки
    файла перед збереженням: якщо з форми приходить новий файл, то
    його шлях не відповідатиме шаблону profile_images/[0-9]*.jpg
    :param path: шлях до файла
    :param patt_list: список шаблонів, допустимих для fnmatch (не re!)
    :return: True або False
    '''
    if not patt_list:
        # Формуємо список шаблонів по-замовчуванню:
        patt_list = []
        pattern = os.path.join('profile_images', "[0-9]*.jpg")
        patt_list.append(pattern)
    # Якщо вхідний параметр - єдиний:
    if patt_list.__class__.__name__  not in ('list', 'tuple'):
        patt_list = [patt_list]
    check = False
    for pattern in patt_list:
        check = check or fnmatch(path, pattern)
    return check

