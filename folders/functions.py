import os
import zipfile
from io import BytesIO
from django.http.response import HttpResponse
from django.utils.http import urlquote
from folders.models import Report, Folder
from koopsite.fileExtMimeTypes import get_mimeType
from koopsite.functions import transliterate
from koopsite.settings import MEDIA_ROOT, MAX_ZIP_FILE_SIZE


def get_recursive_path(report):
    # Отримуємо шлях, який складається з вкладених каталогів:
    # "1/5/7/", де числа - це значення Folder.id починаючи з батьківського
    # Використовується ТІЛЬКИ для друку (напр. в  admin.py).
    id = report.parent.id
    path = ''
    # цикл починається з найглибшого каталога
    while id:
        path = os.path.join(str(id), path)
        # print('id = %2s   path = %s' % (id, path))
        folder = Folder.objects.get(id=id)
        if folder.parent:   id = folder.parent.id
        else:               break
    return path

def get_parents(folder_or_report):
    # Отримуємо список - ланцюжок тек,
    # батьківських відносно теки folder або файла report
    parents_list = []
    # цикл починається з теки, безпосередньо материнської до folder_or_report
    parent = folder_or_report.parent
    while parent:                   # якщо материнська тека існує,
        parents_list.append(parent) # додаємо її до списку
        parent = parent.parent      # і перевіряємо "бабусю"
    # print('parents_list=', parents_list)
    parents_list.reverse()
    return parents_list

def get_full_named_path(folder_or_report):
    parents_list = get_parents(folder_or_report)
    name_list = []
    for p in parents_list:
        name_list.append(p.name)
    m = folder_or_report._meta.model_name
    n = None
    if m == 'folder': n = folder_or_report.name
    if m == 'report': n = folder_or_report.filename
    if not n: n = '--no-name--'
    name_list.append(n)
    path = '/'.join(name_list)
    return path

def get_subfolders(parent):
    # Отримуємо список, який складається з тек,
    # безпосередньо дочірніх відносно parent
    queryset = Folder.objects.filter(parent=parent)
    return queryset

def get_subreports(parent):
    # Отримуємо список, який складається з файлів,
    # безпосередньо дочірніх відносно parent
    queryset = Report.objects.filter(parent=parent)
    return queryset

def response_for_download(report, cd_value='attachment'):
    """
    Preparing response for downloading file
    Content-Disposition header field from http://tools.ietf.org/html/rfc2183
    :param:     report - instance of Report model
    :param:     cd_value - Content Disposition Value:
                    "attachment" - for download
                    "inline" - for preview
    :return:    HttpResponse with report.file and some parameters
    """
    path = report.file.path
    fileExt  = os.path.splitext(report.filename)[1]  # [0] returns path+filename
    ct = get_mimeType().get(fileExt.lower(), "application/octet-stream")
    filename = report.filename
    cdv = '%s; ' % cd_value
    fn = 'filename="%s"; ' % transliterate(filename)
    fns = "filename*=utf-8''%s; " % urlquote(filename)
    md = 'modification-date="%s"; ' % report.uploaded_on
    response = HttpResponse(content_type=ct)
    # content = report.file.read()
    with open(path, 'rb') as file:
        content = file.read()   # читаємо файл незалежно від report
                                # (інакше при тестуванні не завжди
                                # вдається видалити тимчасовий файл)
    response.write(content)
    response['Content-Disposition'] = cdv + fn + fns + md
    response['Content-Length'] = report.file.size
    return response

def response_for_download_zip(folder, maxFileSize = MAX_ZIP_FILE_SIZE):
    """
    Preparing response for downloading zip-file,
    consist of all files in folder (without recursion!)
    Content-Disposition header field from http://tools.ietf.org/html/rfc2183
    :param:     folder - instance of Folder model
    :return:    HttpResponse with zip file and some parameters
                Message in case of zip file overflow max size
    """
    zipSubdir = folder.name
    zipFilename = "%s.zip" % folder.name
    sio = BytesIO()  # Open StringIO to grab in-memory ZIP contents
    zipFile = zipfile.ZipFile(sio, "w")    # The zip compressor
    zipFileSize = 0
    msg = ""
    for report in Report.objects.filter(parent_id=folder.id):
        zipFileSize += report.file.size
        if zipFileSize > maxFileSize:
            msg = 'Завеликий zip. Решту файлів відкинуто'
            break
        filename = report.filename              # "людська" назва файла
        filepath = report.file.name             # шлях до файла на диску
        abs_path = os.path.join(MEDIA_ROOT, filepath)
        zipPath = os.path.join(zipSubdir, filename) # шлях в архіві
        zipFile.write(abs_path, zipPath)            # add file to zip
    zipFile.close() # Must close zip for all contents to be written
    fileExt  = ".zip"
    ct = get_mimeType().get(fileExt.lower(), "application/octet-stream")
    fn = ' filename="%s";' % transliterate(zipFilename)
    fns = " filename*=utf-8''%s;" % urlquote(zipFilename)
    # Grab ZIP file from in-memory, make response with correct MIME-type
    response = HttpResponse(sio.getvalue(), content_type=ct)
    response['Content-Disposition'] = 'attachment' + fn + fns
    response['Content-Length'] = len(sio.getbuffer())
    return response, zipFilename, msg

def wrap_li(folder, level=0, tab=' '*4):
    indent = tab * level
    li = indent + '<li id="%s">%s\n' % (folder.id, folder.name)
    qs = folder.children.all().order_by('name'.lower())
    if qs:
        li = li + wrap_ul(qs, level, tab)
    li = li + indent + '</li>\n'
    return li

def wrap_ul(qs, level=0, tab=' '*4):
    indent = tab * level
    ul = indent + tab + '<ul>\n'
    for f in qs:
        ul = ul + wrap_li(f, level+2, tab)
    ul = ul + indent + tab + '</ul>\n'
    return ul

def get_folders_tree_HTML(parent_qs=None, level=0, tab=' '*4):
    qs = parent_qs or Folder.objects.filter(parent=None).order_by('name'.lower())
    html = wrap_ul(qs, level, tab)
    return html


#---------------- Кінець коду, охопленого тестуванням ------------------
