from django.conf.urls import url
from django.views.generic.base import TemplateView
from folders.views import folderDownload, ReportPreview, FolderReportList, some_view, DisplayPDFView, txt_view, \
    reportPreview, reportDecorView
from folders.views import  FolderCreate, \
                    FolderCreateInFolder, \
                    FolderUpdate, \
                    FolderDelete, \
                    FolderList, \
                    FolderDetail, \
                    ReportUpload, \
                    ReportUploadInFolder, \
                    ReportUpdate, \
                    ReportDelete, \
                    ReportList, \
                    ReportDetail, \
                    reportDownload, \
                    FolderParentList
from folders.viewsajaxfolder import \
                    FolderContents, \
                    ajaxFoldersTreeFromBase, \
                    AjaxFolderCreate, \
                    AjaxFolderRename, \
                    AjaxFolderDelete, \
                    XHRFolderDownload, \
                    XHRReportUpload, \
                    AjaxReportRename, \
                    AjaxReportDelete, \
                    XHRReportDownload, \
                    AjaxElementMove

"""
/folders/ - під'єднано у модулі koopsite.urls.py:
            url(r'^folders/',   include('folders.urls')),
"""

#--------- ПОЧАТОК коду, охопленого функціональними тестами ------------
urlpatterns = [
    url(r'^create/$',   FolderCreate.as_view(),     name='folder-create'),
    url(r'^list/$',     FolderList.as_view(),       name='folder-list'),
    url(r'^list-all/$', FolderReportList.as_view(), name='folder-list-all'),
    url(r'^parents/$',  FolderParentList.as_view(), name='folder-parents'),

    url(r'^(?P<pk>[0-9]+)/$',                   FolderDetail.as_view(), name='folder-detail'),
    url(r'^(?P<pk>[0-9]+)/update/$',            FolderUpdate.as_view(), name='folder-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$',            FolderDelete.as_view(), name='folder-delete'),
    url(r'^(?P<pk>[0-9]+)/download/$',          folderDownload,         name='folder-download'),

    url(r'^(?P<parent>\d+)/create/$',           FolderCreateInFolder.as_view(), name='folder-create-in'),
    url(r'^(?P<parent>\d+)/report/upload/$',    ReportUploadInFolder.as_view(), name='report-upload-in'),

    url(r'^report/upload/$',                    ReportUpload.as_view(), name='report-upload'),
    url(r'^report/list/$',                      ReportList.as_view(),   name='report-list'),

    url(r'^report/(?P<pk>[0-9]+)/$',            ReportDetail.as_view(), name='report-detail'),
    url(r'^report/(?P<pk>[0-9]+)/update/$',     ReportUpdate.as_view(), name='report-update'),
    url(r'^report/(?P<pk>[0-9]+)/delete/$',     ReportDelete.as_view(), name='report-delete'),
    url(r'^report/(?P<pk>[0-9]+)/download/$',   reportDownload,         name='report-download'),
    url(r'^report/(?P<pk>[0-9]+)/preview/$',    ReportPreview.as_view(), name='report-preview'),
#--------- Кінець коду, охопленого функціональними тестами ------------
    url(r'^report/(?P<pk>[0-9]+)/view/$',       reportPreview,          name='report-view'),
    url(r'^report/(?P<pk>[0-9]+)/deco/$',       reportDecorView,        name='report-deco'),

    url(r'^(?P<pk>[0-9]+)/contents/$',  FolderContents.as_view(),   name='folder-contents'),

    url(r'^ajax-folders-tree-from-base$',   ajaxFoldersTreeFromBase,    name='ajax-folders-tree-from-base'),
    url(r'^ajax-folder-create$',            AjaxFolderCreate.as_view(), name='ajax-folder-create'),
    url(r'^ajax-folder-rename$',            AjaxFolderRename.as_view(), name='ajax-folder-rename'),
    url(r'^ajax-folder-delete$',            AjaxFolderDelete.as_view(), name='ajax-folder-delete'),
    url(r'^ajax-report-rename$',            AjaxReportRename.as_view(), name='ajax-report-rename'),
    url(r'^ajax-report-delete/(?P<pk>[0-9]+)/$', AjaxReportDelete.as_view(), name='ajax-report-delete'),
    url(r'^ajax-element-move$',             AjaxElementMove.as_view(),  name='ajax-element-move'),
    url(r'^ajax-folder-download$',          XHRFolderDownload.as_view(),name='ajax-folder-download'),
    url(r'^ajax-report-download$',          XHRReportDownload.as_view(),name='ajax-report-download'),
    url(r'^ajax-report-upload$',            XHRReportUpload.as_view(),  name='ajax-report-upload$'),

    url(r'^folder-not-empty/$',
        TemplateView.as_view(template_name='folders/folder_not_empty.html'),
                                        name='folder-not-empty'),

    # TODO-зробити preview уніфіковану для jpg, pdf, txt на основі CBV + повідомлення про неможливість перегляду
    url(r'^txt/$',   txt_view,         name='txt_view'),
    url(r'^some_view/$',   some_view,         name='some_view'),
    url(r'^pdf/$',     DisplayPDFView.as_view(), name='pdf_view'),
]

# urlpatterns += staticfiles_urlpatterns()
'''
# from Tango with Django:
if settings.DEBUG:
        urlpatterns += patterns(
                'django.views.static',
                (r'media/(?P<path>.*)',
                'serve',
                {'document_root': settings.MEDIA_ROOT}), )
'''
