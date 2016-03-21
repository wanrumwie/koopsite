__author__ = 'Мирослава'

from evalprint import evprint, elprint
from django_apps_setup import django_apps_setup

# Встановлення змінної оточення та ініціалізація Django
django_apps_setup("koopsite.settings")

# Тепер можна імпортувати моделі з застосунку Django
from flats.models import Flat, Person

def modeldel(model):
    print('Warning!'
          'Deleting database record(s)!')
    id = input('For record you would like to delete input id:')
    try:
        m = model.objects.filter(id=id)
        print('%3s  %s' % (id, m))
        m.delete()
        print('record %s deleted:' % id)
        print('%3s  %s' % (id, m))
    except:
        print('deleting unsuccessful')

def modelprint(model):
    print('model:', model.objects.all())
    for m in model.objects.all():
        try:
            print('%3s  %s' % (m.id, m))
        except: pass

def oneprint(model, id):
    print('model:', model.objects.all())
    m = model.objects.get(id=id)
    print(m.entrance_No)
    print('m.__dict__:', m.__dict__)
    for i in m.__dict__:
        print('%30s  %s' % (i, m.__dict__[i]))
    print(model.mdbFields)
    print(m.mdbFields)
    for i in m.mdbFields:
        print('%30s  %s' % (i, getattr(m, i)))


print('Робота з sqlite3')
while True:
    s = input('Введіть модель: F - Flat, P - Person, X - вихід :')
    if s.upper() == 'X': break
    if s.upper() == 'F': model = Flat
    if s.upper() == 'P': model = Person
    while True:
        s = input('Print model, Delete row(s), 1 row, eXit: input char:')
        if s.upper() == 'X': break
        if s.upper() == 'P': modelprint(model)
        if s == '1':
            id = input('Input id:')
            oneprint(model, id)

        if s.upper() == 'D':
            modelprint(model)
            modeldel(model)
