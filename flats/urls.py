from django.conf.urls import url
from flats.views import FlatList, FlatScheme, \
                    FlatDetail, FlatDetailHorizontal, \
                    FlatTable, \
                    FlatSchemeUsers, FlatUsersList
from koopsite.views import page_not_ready


"""
/flats/ - під'єднано у модулі koopsite.urls.py:
            url(r'^flats/',   include('flats.urls')),
"""
urlpatterns = [
    url(r'^list/$',             FlatList.as_view(),             name='flat-list'),
    url(r'^scheme/$',           FlatScheme.as_view(),           name='flat-scheme'),
    url(r'^(?P<pk>[0-9]+)/$',   FlatDetail.as_view(),           name='flat-detail'),
    url(r'^(?P<pk>[0-9]+)/h/$', FlatDetailHorizontal.as_view(), name='flat-detail-h'),
    url(r'^table/$',            FlatTable.as_view(),            name='flat-table'),

    url(r'^scheme-users/$',     FlatSchemeUsers.as_view(),      name='flat-scheme-users'),
    url(r'^(?P<pk>[0-9]+)/users-list/$',   FlatUsersList.as_view(), name='flat-users-list'),

#--------- Кінець коду, охопленого функціональними тестами ------------

    # url(r'^person/table/$',   PersonTableView.as_view(), name='person-table'),
    url(r'^person/table/$',     page_not_ready,                 name='person-table'),
]
# urlpatterns += staticfiles_urlpatterns()

