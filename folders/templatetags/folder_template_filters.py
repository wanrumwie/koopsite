'''
Означення власних "фільтрів", якими можна користатися в шаблонах
'''
import os
from django import template
from folders.functions import get_full_named_path
from koopsite.fileExtMimeTypes import get_mimeType
from koopsite.functions import get_iconPathForFolder, \
                               get_iconPathByFileExt

register = template.Library()

@register.filter
def filename(f):
    # Фільтр для назви файла
    try:    n = os.path.basename(f.filename)
    except: n = ""
    return n

@register.filter
def fileext(f):
    # Фільтр для розширення файла
    try:    e = os.path.splitext(f.filename)[1]  # [0] returns path+filename
    except: e = ""
    return e

@register.filter
def file_media_type(f):
    # Фільтр для медіатипу файла
    try:
        e = os.path.splitext(f.filename)[1]  # [0] returns path+filename
        mt = get_mimeType().get(e.lower(), "")
    except: mt = ""
    return mt

# Фільтр для назви файла-іконки (для моделей folder і report)
@register.filter
def iconpath(f):
    m = f._meta.model_name
    if m == 'folder':
        p = get_iconPathForFolder()
    elif m == 'report' and f.file:
        try:    e = os.path.splitext(f.filename)[1]  # [0] returns path+filename
        except: e = ""
        p = get_iconPathByFileExt(e)
    else:
        p = ''
    return p

@register.filter
def full_named_path(f):
    # Фільтр для повного шляху файла чи теки у структурі каталогу
    # Імена беруться з folder.name i report.filename
    try:    n = get_full_named_path(f)
    except: n = ""
    return n

#---------------- Кінець коду, охопленого тестуванням ------------------
