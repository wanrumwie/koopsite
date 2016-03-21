__author__ = 'Мирослава'
'''
УВАГА!
Ця програмка заповнює базу db.sqlite3 даними з акцесівської
бази mdb
З файла models.py беруться:
mdbTable - назва таблиці в базі access
mdbFields - словник відповідності між назвами полів у базах mdb i sqlite3

Програмку запускати лише один раз!!!
у момент, коли файл db.sqlite3 вже створено
Про всяк випадок рядки виклику вкінці цього файла закоментовані!!!
'''
import pypyodbc
from mdbaccess import *
from django_apps_setup import django_apps_setup

# Встановлення змінної оточення та ініціалізація Django
django_apps_setup("koopsite.settings")

# Тепер можна імпортувати моделі з застосунку Django
from flats.models import Flat, Person

def sqlite3_from_mdb(mdbfilepath, tableName, model):
    # копіює всі дані з таблиці mdb в таблицю sqlite3
    pypyodbc.lowercase = False
    connection = pypyodbc.win_connect_mdb(mdbfilepath)
    cursor = connection.cursor()
    fields = "*"
    condition = ""
    sqlcommand = "SELECT %s FROM %s %s" % (fields, tableName, condition)
    cursor.execute(sqlcommand)

    print('-'*50)
    attr = False
    while True:
        row = cursor.fetchone()
        if not row: break
        print('row=', row)
        m = model()
        if not attr:
            attr = True
            coldict, collist = rowAttributes(row)
        # print(coldict)
        # print(collist)
        for field in m.mdbFields:
            # print(field, m.mdbFields[field])
            if row[coldict[m.mdbFields[field]]]:
                setattr(m, field, row[coldict[m.mdbFields[field]]])
        for field in m.mdbFields:
            print('%20s | %s' % (field, getattr(m, field)))
        m.save()
        print('m.id=', m.id)
        print('-'*50)
        # input()

    print('-'*50)

    cursor.close()
    connection.commit()
    connection.close()


mdbfiledir = 'c:/PyPrograms/PyRoman/mdbaccess/'
mdbfilename = 'Список Кооперативу Example.mdb'
mdbfilepath = mdbfiledir + mdbfilename
print(mdbfilepath)


# tableName='[Таблиця Квартири]'
# sqlite3_from_mdb(mdbfilepath, tableName, model=Flat)
#
# tableName='[Таблиця Особи]'
# sqlite3_from_mdb(mdbfilepath, tableName, model=Person)

