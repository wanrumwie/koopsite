from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from flats.models import Flat
from koopsite.functions import get_flat_users
from koopsite.views import AllFieldsView, AllRecordsAllFieldsView


class FlatList(ListView):
    model = Flat
    # paginate_by = 17
    context_object_name = 'flat_list'
    template_name = 'flats/flat_list.html'


def block_scheme():
    """
    Допоміжна функція для get_context_data()
    Групує квартири по-блочно у дворівневий словник:
    {floor0: {entrance1: [flat1, ], entrance2: [flat4, ]}, }
    :return:
    d - власне дворівневий словник списків квартир;
    floors - сортований список поверхів;
    entrances - сортований список під'їздів
    """
    # Готуємо порожні словники і списки до заповнення:
    entrances = set()
    floors = set()
    d = {}
    # Кожну квартиру з бази додаємо до списку d[f][e]
    for flat in Flat.objects.all().order_by('flat_99'):
        f = flat.floor_No
        e = flat.entrance_No
        if f not in d:
            d[f] = {}       # створюємо порожній словник для поверху
        if e not in d[f]:
            d[f][e] = []    # створюємо порожній список для блоку на поверсі
        d[f][e].append(flat)  # кожну квартиру вміщуємо у свій блок
        floors.add(f)
        entrances.add(e)
    floors = sorted(floors, reverse=True)
    entrances = sorted(entrances)
    # print(d)
    # print(floors)
    # print(entrances)
    return d, floors, entrances


def block_length(d):
    # Визначаємо для кожного під'їзду макс.к-ть квартир на поверсі
    # для того, щоб кожен під'їзд в шаблоні був представлений вертик. колонкою:
    block_len = {}
    for f in d:
        for e in d[f]:
            n = block_len.get(e, 0)
            n = max(n, len(d[f][e]))
            block_len[e] = n
    return block_len


class FlatScheme(ListView):
    model = Flat
    # context_object_name = 'flat_scheme'
    template_name = 'flats/flat_scheme.html'

    def get_context_data(self, **kwargs):
        # self.object_list = Flat.objects.all()
        self.object_list = None
        # Створюємо атрибут класу self.object_list
        # інакше TestCase дає AttributeError:
        #   'FlatScheme' object has no attribute 'object_list'
        # Крім того при None в контекст не передається (двічі!)
        # непотрібний тут список всіх об'єктів.
        # Всі потрібні значення описані нижче:
        kwargs = super(FlatScheme, self).get_context_data(**kwargs)
        d, floors, entrances = block_scheme()
        l = block_length(d)
        kwargs['block_scheme'] = d
        kwargs['block_length'] = l
        kwargs['floors']       = floors
        kwargs['entrances']    = entrances
        kwargs['flatclass']    = 'flat-has-users'
        # dict_print(kwargs, 'kwargs')
        return kwargs


class FlatDetail(AllFieldsView):
    model = Flat
    template_name = 'flats/flat_detail.html'
    paginate_by = 14
    exclude = ('id', 'flat_99', 'note', 'listing')   # Поля, які виключаються із списку виводу.


class FlatDetailHorizontal(AllFieldsView):
    model = Flat
    template_name = 'flats/flat_detail_h.html'
    paginate_by = 0
    exclude = ('id', 'flat_99', 'note', 'listing')   # Поля, які виключаються із списку виводу.


class FlatTable(AllRecordsAllFieldsView):
    model = Flat
    paginate_by = 15
    exclude = ('id', 'flat_99', 'note', 'listing')   # Поля, які виключаються із списку виводу.
    template_name = 'flats/flat_table.html'
    context_object_name = "field_vals"
    context_verbose_list_name = "field_names"


class FlatSchemeUsers(FlatScheme):
    template_name = 'flats/flat_scheme_users.html'

    @method_decorator(permission_required('koopsite.view_userprofile'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class FlatUsersList(SingleObjectMixin, ListView):
    template_name = 'flats/flat_users_list.html'

    @method_decorator(permission_required('koopsite.view_userprofile'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Flat.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # Повертає список всіх користувачів, у профілі яких вказано flat
        flat = self.object
        qs = get_flat_users(flat)
        return qs

#---------------- Кінець коду, охопленого тестуванням ------------------

