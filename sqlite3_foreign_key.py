__author__ = 'Мирослава'

from django_apps_setup import django_apps_setup

# Встановлення змінної оточення та ініціалізація Django
django_apps_setup("koopsite.settings")

# Тепер можна імпортувати моделі з застосунку Django
from flats.models import Flat, Person

def modelprint(model=Flat):
    # друк всіх записів одної моделі
    print('model:', model.objects.all())
    for m in model.objects.all():
        try:
            print('%3s  %s' % (m.id, m))
        except: pass

def flatpersonprint():
    # друк всіх записів моделі Flat
    # і для кожного запису - всі записи моделі Person,
    # у яких значення flat_99 співпадають
    # (тобто без застосування ForeignKey)
    for flat99 in range(1,100):
        # print(flat99)
        f = Flat.objects.get(flat_99=flat99)
        print('%3s  %s' % (f.id, f))
        fpers = Person.objects.filter(flat_99=flat99)
        for p in fpers:
            print(' '*10+'%3s  %s' % (p.id, p))


def personforeignkeysave():
    # Для кожного запису моделі Flat
    # відбираються всі записи моделі Person,
    # у яких значення flat_99 співпадають
    # (тобто поки-що без застосування ForeignKey).
    # Встановлення для цієї вибірки значень в поле flat (ForeignKey)
    # і збереження в базі.
    for flat99 in range(1,100):
        # print(flat99)
        f = Flat.objects.get(flat_99=flat99)
        print('%3s  %s' % (f.id, f))
        fpers = Person.objects.filter(flat_99=flat99)
        for p in fpers:
            print(' '*10+'%3s  %s' % (p.id, p))
            p.flat = f
            p.save()


# flatpersonprint()

# УВАГА! Рядок виклику закоментовано:
# personforeignkeysave()
