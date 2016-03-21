"""
Означення власних "фільтрів", якими можна користатися в шаблонах
"""

from django.template import Library
from koopsite.functions import get_user_full_name, get_user_flat_No, get_thumbnail_url_path, get_flat_users, \
    has_flat_member, has_group_members

register = Library()

@register.filter()
def get_at_index(list, index):
    # Фільтр для отримання елемента списку за його індексом
    try:    val = list[index]
    except: val = None
    return val

@register.filter()
def get_item_by_key(dictionary, key):
    # Фільтр для отримання значення словника за його ключем
    try:    val = dictionary.get(key)
    except: val = None
    return val

@register.filter()
def range_of(n):
    # Фільтр для отримання ітератора range(n) в шаблоні
    try:    val = range(n)
    except: val = None
    return val

@register.filter()
def model_name(f):
    # Фільтр для назви моделі
    m = f._meta.model_name
    return m

@register.filter()
def user_full_name(user):
    # Фільтр для повного імені користувача
    fn = get_user_full_name(user)
    return fn

@register.filter()
def user_flat_No(user):
    # Фільтр для номера квартири з профілю користувача
    fn = get_user_flat_No(user)
    return fn

# TODO 2016 01 17 не вдалося зробити thumbnail filter для path (а не тільки для file)
@register.filter()
def thumbnail(picture, size='30x24'):
    """
    A filter to resize a ImageField on demand, a use case could be:
    <img src="{{ object.image.url }}" alt="original image">
    <img src="{{ object.image|thumbnail }}" alt="image resized to default 104x104 format">
    <img src="{{ object.image|thumbnail:200x300 }}" alt="image resized to 200x300">
    Original http://www.djangosnippets.org/snippets/955/
    :param picture: image object (ImageField instance)
                        or image file path (str)
    :param size:    size for thumbnail
    :return:        thumbnail url
    """
    return get_thumbnail_url_path(picture, size)[0]

@register.filter()
def icon_yes_no_unknown(bool_val):
    """
    # Фільтр представлення поля NullBooleanField іконкою.
    """
    if   bool_val == True:  miniature_url = 'admin/img/icon-yes.gif'
    elif bool_val == False: miniature_url = 'admin/img/icon-no.gif'
    else:                   miniature_url = 'admin/img/icon-unknown.gif'
    return miniature_url

@register.filter()
def flat_user_CSS_class(flat):
    # Фільтр визначає CSS-клас для комірки з flat
    # залежно від користувачів, повязаних з цією квартирою
    css_class = ""
    users = get_flat_users(flat)
    if users:
        css_class = "flat-has-users"
        if has_flat_member(flat):
            css_class = "flat-has-member"
    return css_class

@register.filter()
def has_member_perms(user):
    # Фільтр визначає CSS-клас для комірки з flat
    # залежно від користувачів, повязаних з цією квартирою
    return has_group_members(user)

#---------------- Кінець коду, охопленого тестуванням ------------------

