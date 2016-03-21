__author__ = 'Мирослава'
'''
Функції для доступу до даних з таблиць в базі даних Access
'''

import pypyodbc
import os.path

pypyodbc.lowercase = False

def mdbTableList(cursor):
    # повертає список таблиць і запитів у базі даних
    tab = cursor.tables()
    tableList = []
    queryList = []
    for t in tab:
        if t[3] == "TABLE": tableList.append(t[2])
        if t[3] == "VIEW" : queryList.append(t[2])
    return tableList, queryList

def mdbColumnList(cursor, table):
    # повертає список найменувань полів у таблиці у базі даних
    col = cursor.columns(table=table)
    columnList = []
    for c in col:
        columnList.append(c[3])
    return columnList

def mdbColumnParameters(cursor, table, column):
    # повертає кортеж параметрів обраної колонки
    col = cursor.columns(table=table, column=column)
    l = list(col)
    t = l[0]
    return t

def rowAttributes(row):
    # повертає словник: {columnName: n},
    # де n - номер елемента в кортежі row,
    # який відповідає колонці з назвою columnName
    coldict = {}
    # також повертає список тих же columnname
    # (сортований на відміну від словника)
    collist = []
    for i in range(len(row.cursor_description)):
        columnName = row.cursor_description[i][0]
        collist.append(columnName)
        coldict[columnName] = i
    return coldict, collist

def allfieldnamesprint(cursor):
    print('-'*50)
    print('ДРУК НАЗВ КОЛОНОК ВСІХ ТАБЛИЦЬ У БАЗІ ДАНИХ access:')
    tableList, queryList = mdbTableList(cursor)
    for table in tableList:
        print('-'*50)
        print('table=', table)
        print('-'*50)
        columnList = mdbColumnList(cursor, table)
        for column in columnList:
            columnParameters = mdbColumnParameters(cursor, table, column)
            s = '"%s"' % columnParameters[3]
            print(': %-40s' % s)

def get_mdb_connection(mdbfilepath):
    pypyodbc.lowercase = False
    connection = pypyodbc.win_connect_mdb(mdbfilepath)
    return connection

def close_mdb_connection(connection):
    # connection.cursor.close()
    connection.commit()
    connection.close()

def mdb_investigation(mdbfilepath):
    # Досліджує невідому mdb
    connection = get_mdb_connection(mdbfilepath)
    cursor = connection.cursor()
    allfieldnamesprint(cursor)
    print('-'*50)
    close_mdb_connection(connection)

def all_data_print_from_mdb(mdbfilepath, tableName):
    # друкує всі дані з таблиці mdb
    connection = get_mdb_connection(mdbfilepath)
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
        if not attr:
            attr = True
            coldict, collist = rowAttributes(row)
        # print(coldict)
        # print(collist)
        print('-'*50)
        # input()

    print('-'*50)

    close_mdb_connection(connection)



if __name__ == '__main__':

    # mdbfiledir = 'c:/PyPrograms/PyRoman/mdbaccess/'
    # mdbfilename = 'Список Кооперативу Example.mdb'
    # mdbfilepath = mdbfiledir + mdbfilename
    mdbfiledir = r'D:\Файли з Lenovo\Роман\Кооп Пасічний\1с Кооп 2013 11 30\Db-Koop'
    mdbfilename = r'1c Кооп 2013 11 30 Access.accdb'
    mdbfilepath = os.path.join(mdbfiledir, mdbfilename)
    print(mdbfilepath)

    mdb_investigation(mdbfilepath)
