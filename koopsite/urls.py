"""koopsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView
from koopsite.views import index, user_logout, \
                    noaccess, success, \
                    OwnProfileUpdate, \
                    UserProfileCreate, \
                    adm_index, \
                    UserProfilePersonDataUpdate, \
                    UserPermsFullUpdate,\
                    UserPermsActivateUpdate, \
                    OwnProfileDetailShow, \
                    UserProfileDetailShow, LoginView, ChangePassword, \
                    page_not_ready
from koopsite.viewsajax import \
                    ajaxSelRowIndexToSession, \
                    ajaxStartRowIndexFromSession
from koopsite.viewsajaxuser import UsersTable, AjaxRecognizeAccount, \
                    AjaxDenyAccount, AjaxActivateAccount, \
                    AjaxDeactivateAccount, AjaxDeleteAccount, \
                    AjaxSetMemberAccount, AjaxDenyMemberAccount, \
                    AjaxActivateAllAccounts, AjaxSetMemberAllAccounts

from koopsite.settings import MEDIA_ROOT, MEDIA_URL

#--------- ПОЧАТОК коду, охопленого функціональними тестами ------------
urlpatterns = [
    # сайт: localhost або готовий сайт

    # /index/ та інші "кореневі" url - виклик з views.py проекту
    url(r'^$',          index,                          name='root'),
    url(r'^index/$',    index,                          name='index'),
    url(r'^login/$',    LoginView.as_view(),            name='login'),
    url(r'^logout/$',   user_logout,                    name='logout'),
#--------- Кінець коду, охопленого функціональними тестами ------------
    url(r'^noaccess/$', noaccess,                       name='noaccess'),
    url(r'^success/$',  success,                        name='success'),
#--------- ПОЧАТОК коду, охопленого функціональними тестами ------------
    url(r'^register/$', UserProfileCreate.as_view(),    name='register'),
#--------- Кінець коду, охопленого функціональними тестами ------------

    # /own/profile/ та інші - дані залогіненого користувач (is_authenticated == True)
    url(r'^own/profile/$',          OwnProfileDetailShow.as_view(), name='own-profile'),
    url(r'^own/profile/update/$',   OwnProfileUpdate.as_view(),     name='own-profile-update'),
    url(r'^own/change-password/$',  ChangePassword.as_view(),       name='change-password'),
    # url(r'^own/change-password/$',  change_password,                name='change-password'),

    # /adm/ та інші - адміністративні сторінки (is_staff == True)
    url(r'^adm/index/$',                              adm_index,                            name='adm-index'),
    url(r'^adm/users/table/$',                        UsersTable.as_view(),                 name='adm-users-table'),
    url(r'^adm/users/(?P<pk>[0-9]+)/profile/$',       UserProfileDetailShow.as_view(),      name='adm-users-profile'),
    url(r'^adm/users/(?P<pk>[0-9]+)/profile/update/$',UserProfilePersonDataUpdate.as_view(),name='adm-users-profile-update'),
    url(r'^adm/users/(?P<pk>[0-9]+)/perms/update/$',  UserPermsFullUpdate.as_view(),        name='all-users-perm-update'),
    url(r'^adm/users/(?P<pk>[0-9]+)/perms/activate/$',UserPermsActivateUpdate.as_view(),    name='all-users-perm-activate'),

    # Виклик AJAX для koop_users_table
    url(r'^adm/users/ajax-activate-all-accounts$',  AjaxActivateAllAccounts.as_view(),  name='adm-users-ajax-activate-all-accounts'),
    url(r'^adm/users/ajax-set-member-all-accounts$',AjaxSetMemberAllAccounts.as_view(), name='adm-users-ajax-set-member-all-accounts'),
    url(r'^adm/users/ajax-recognize-account$',      AjaxRecognizeAccount.as_view(),     name='adm-users-ajax-recognize-account'),
    url(r'^adm/users/ajax-deny-account$',           AjaxDenyAccount.as_view(),          name='adm-users-ajax-deny-account'),
    url(r'^adm/users/ajax-activate-account$',       AjaxActivateAccount.as_view(),      name='adm-users-ajax-activate-account'),
    url(r'^adm/users/ajax-deactivate-account$',     AjaxDeactivateAccount.as_view(),    name='adm-users-ajax-deactivate-account'),
    url(r'^adm/users/ajax-set-member-account$',     AjaxSetMemberAccount.as_view(),     name='adm-users-ajax-set-member-account'),
    url(r'^adm/users/ajax-deny-member-account$',    AjaxDenyMemberAccount.as_view(),    name='adm-users-ajax-deny-member-account'),
    url(r'^adm/users/ajax-delete-account$',         AjaxDeleteAccount.as_view(),        name='adm-users-ajax-delete-account'),

    # Виклик AJAX для обміну даними з сесією
    url(r'^ajax-selrowindex-to-session$',     ajaxSelRowIndexToSession,     name='ajax-selrowindex-to-session'),
    url(r'^ajax-startrowindex-from-session$', ajaxStartRowIndexFromSession, name='ajax-startrowindex-from-session'),

    # /flats/ та інші - під'єднуємо urls.py аплікацій
    url(r'^flats/',     include('flats.urls',   namespace='flats')),
    url(r'^folders/',   include('folders.urls', namespace='folders')),

    # /admin/ - під'єднання до вбудованого admin
    url(r'^admin/',     include(admin.site.urls)),

    # /messages/ - під'єднання до вбудованого django_messages app
    # url(r'^messages/',  include('django_messages.urls')),

    url(r'^page_not_ready/$', page_not_ready,   name='page_not_ready'),

    # /js_tests/ - під'єднуємо urls.py js-тестів
    url(r'^js_tests/',  include('js_tests.urls', namespace='js_tests')),

    # FT - порожня сторінка, щоб задати кукі перед аутентифікацією при тестах
    url(r'^selenium-cookie-setup/$',
        TemplateView.as_view(template_name='selenium_cookie_page.html'),
                                        name='selenium-cookie-setup'),

]
urlpatterns += static.static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

