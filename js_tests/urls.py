from django.conf.urls import url
from django.views.generic.base import TemplateView

"""
/js_tests/ - під'єднано у модулі koopsite.urls.py:
    url(r'^js_tests/',  include('js_tests.urls')),
"""

urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name='js_tests.html'),
                                      name='js_tests'),

    url(r'^error_hide/$',
        TemplateView.as_view(template_name='js_tests_errorlist_hide_listeners.html'),
                                      name='error_hide'),
    url(r'^browtab/$',
        TemplateView.as_view(template_name='js_tests_browtab.html'),
                                      name='browtab'),
    url(r'^browtab_ajax/$',
        TemplateView.as_view(template_name='js_tests_browtab_ajax.html'),
                                      name='browtab_ajax'),
    url(r'^browtab_ui/$',
        TemplateView.as_view(template_name='js_tests_browtab_ui.html'),
                                      name='browtab_ui'),
    url(r'^browtab_sort/$',
        TemplateView.as_view(template_name='js_tests_browtab_sort.html'),
                                      name='browtab_sort'),

    url(r'^koopsite/users_browtab/$',
        TemplateView.as_view(template_name='koopsite/js_tests_users_browtab.html'),
                                      name='koopsite_users_browtab'),
    url(r'^koopsite/users_browtab_ajax/$',
        TemplateView.as_view(template_name='koopsite/js_tests_users_browtab_ajax.html'),
                                      name='koopsite_users_browtab_ajax'),
    url(r'^koopsite/users_browtab_ui/$',
        TemplateView.as_view(template_name='koopsite/js_tests_users_browtab_ui.html'),
                                      name='koopsite_users_browtab_ui'),
    url(r'^koopsite/users_browtab_sort/$',
        TemplateView.as_view(template_name='koopsite/js_tests_users_browtab_sort.html'),
                                      name='koopsite_users_browtab_sort'),
    url(r'^koopsite/users_browtab_filter/$',
        TemplateView.as_view(template_name='koopsite/js_tests_users_browtab_filter.html'),
                                      name='koopsite_users_browtab_filter'),

    url(r'^folders/folder_browtab/$',
        TemplateView.as_view(template_name='folders/js_tests_folder_browtab.html'),
                                      name='folders_folder_browtab'),
    url(r'^folders/folder_browtab_ajax/$',
        TemplateView.as_view(template_name='folders/js_tests_folder_browtab_ajax.html'),
                                      name='folders_folder_browtab_ajax'),
    url(r'^folders/folder_browtab_ui/$',
        TemplateView.as_view(template_name='folders/js_tests_folder_browtab_ui.html'),
                                      name='folders_folder_browtab_ui'),
    url(r'^folders/folder_browtab_sort/$',
        TemplateView.as_view(template_name='folders/js_tests_folder_browtab_sort.html'),
                                      name='folders_folder_browtab_sort'),


    url(r'^folders/$',
        TemplateView.as_view(template_name='folders/js_tests_folders.html'),
                                      name='folders'),
    url(r'^example/$',
        TemplateView.as_view(template_name='js_tests_example.html'),
                                      name='example'),
]

