from glob import glob
import os
import os.path
from pathlib import Path
from tkinter import Tk, mainloop
from comboform import ComboForm
from koopsite.settings import INSTALLED_APPS, BASE_DIR

fname = 'manage-test_select.data'

def get_test_list(start_path):
    # path_pattern = os.path.join(start_path, "*\\test*.py")
    path_pattern = "**/test*.py"
    # print('path_pattern =', path_pattern)
    path_list = Path(start_path).glob(path_pattern)
    test_list = set()
    for i in path_list:
        # print('i =', i)
        # r = os.path.relpath(i, start=start_path)
        r = i.relative_to(start_path)
        r = str(r)
        d, b = os.path.split(r)
        n, e = os.path.splitext(b)
        d = d.replace('\\', '.')
        test_list.add(d)
        f = '.'.join([d,n])
        test_list.add(f)
    return sorted(test_list)

def exec_test(arg1, arg2, arg3):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "koopsite.settings")
    from django.core.management import execute_from_command_line
    # execute_from_command_line(sys.argv)
    print('execute_from_command_line([%s, %s, %s])' % (arg1, arg2, arg3))
    execute_from_command_line([arg1, arg2, arg3])

def get_defaults(fname):
    try:
        with open(fname) as infile:
            line = infile.readline()
            args = line.split()
    except:
        args = []
    return args

def save_defaults(fname, *args):
    line = ''
    for s in args:
        line += s + ' '
    with open(fname, 'w') as outfile:
        outfile.write(line)


class ManageComboForm(ComboForm):

    def onSubmit(self):
        # отримуємо з Форми параметри:
        arg1 = self.content[arg1Label].get()
        arg2 = self.content[arg2Label].get()
        arg3 = self.content[arg3Label].get()
        save_defaults(fname, arg1, arg2, arg3)
        exec_test(arg1, arg2, arg3)



if __name__ == '__main__':

    test_list = get_test_list(BASE_DIR)
    # for t in test_list:
    #     print(t)

    args = get_defaults(fname)

    root = Tk()

    # Заголовок
    topText='Введіть аргументи до виконання для функції execute_from_command_line'
    # execute_from_command_line(['manage.py','test', 'koopsite'])

    # Назви полів вводу Label
    arg1Label = 'Перший аргумент'
    arg2Label = 'Другий аргумент'
    arg3Label = 'Третій аргумент'

    # Початкові дані в Entry
    arg1    = 'manage.py'
    arg2    = 'test'
    arg3def = test_list[0] if test_list else ''
    arg3    = test_list

    if args and len(args) == 3:
        arg1    = args[0]
        arg2    = args[1]
        arg3def = args[2]

    # Формування labels - області вводу даних
    # Кожен з labels має віджети Label і Entry
    # і може мати віджети Button і Checkbutton
    labels = []
    labels.append({'text'   : arg1Label,
                   'default': arg1,
                   })
    labels.append({'text'   : arg2Label,
                   'default': arg2,
                   })
    labels.append({'text': arg3Label,
                   'default': arg3def,
                   'combobox': arg3,
                   })

    ManageComboForm(parent=root, topText=topText, labels=labels)
    mainloop()
