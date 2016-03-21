from django.contrib import admin
import os
from folders.functions import get_recursive_path
from folders.models import get_report_path, Folder, Report
from koopsite.settings import MEDIA_ROOT


class FolderAdmin(admin.ModelAdmin):
    actions = ['clear_date']
    def clear_date(self, request, queryset):
        i = 0
        print('%6s %6s %12s %s' % ('id', 'parent', 'date', 'name'))
        for obj in queryset:
            try:
                print('%6s %6s %12s %s' % (obj.id, obj.parent.id, obj.created_on, obj.name))
                obj.created_on = None
                obj.save()
                i += 1
            except:
                pass
        if i == 1:  message_bit = "%s object was" % i
        else:       message_bit = "%s objects were" % i
        self.message_user(request, "%s successfully updated." % message_bit)
    clear_date.short_description = "Clear date for selected Folders"

    list_per_page = 15
    preserve_filters = True
    readonly_fields = ('id', 'created_on')
    # date_hierarchy = 'created_on'
    list_display = (
                    'id'      ,
                    'name'      ,
                    'created_on',
                    'parent'    ,
                    )
    list_display_links = (
                    'id'      ,
                    'name'      ,
                    )
    list_filter =   (
                    'created_on',
                    'parent'    ,
                    )
    fieldsets = [
        (None,          {'fields': [
                                   (
                                    'id'      ,
                                    'name'      ,
                                    'created_on',
                                    'parent'    ,
                                   ),
                                    ]
                        }
        ),
    ]


class ReportAdmin(admin.ModelAdmin):
    actions = ['re_save_files', 'code_file_names', 'clear_files']
    # def re_save_files(self, request, queryset):
    #     i = 0
    #     print('%6s %6s %10s %s' % ('id', 'parent', 'path', 'file'))
    #     for obj in queryset:
    #         print('%6s %6s %10s %s' % (obj.id, obj.parent.id, get_recursive_path(obj), obj.file))
    #         obj.save()
    #         i += 1
    #     if i == 1:  message_bit = "%s object was" % i
    #     else:       message_bit = "%s objects were" % i
    #     self.message_user(request, "%s successfully updated." % message_bit)
    # re_save_files.short_description = "Re-save files for selected Reports (folders will be created)"

    def code_file_names(self, request, queryset):
        i = 0
        print('%-6s %-6s %-30s %s' %
              ('id', 'parent', 'file', 'newFilePath'))
        for obj in queryset:
            try:
                # Старий шлях до файла - дотеперішнє фактичне розташування
                oldAbsPath = os.path.join(MEDIA_ROOT, obj.file.name)
                oldAbsPath = os.path.normpath(oldAbsPath)
                # Файл буде збережено під новою кодовою назвою
                newFilePath = get_report_path(obj.id)
                newAbsPath = os.path.join(MEDIA_ROOT, newFilePath)
                newAbsPath = os.path.normpath(newAbsPath)
                print('%-6s %-6s %-30s %s' % (obj.id,
                                                obj.parent.id,
                                                obj.file,
                                                newAbsPath))
                obj.file.name = newFilePath # атрибут file повинен мати актуальну назву файла
                os.renames(oldAbsPath, newAbsPath)
                obj.save()
                i += 1
            except:
                print('%-6s %-6s %-30s %s' % (obj.id,
                                                obj.parent.id,
                                                obj.file,
                                                'NOT RENAMED'))
        if i == 1:  message_bit = "%s object was" % i
        else:       message_bit = "%s objects were" % i
        self.message_user(request, "%s successfully renamed." % message_bit)
    code_file_names.short_description = "Re-save files for selected Reports with coded names"

    def clear_files(self, request, queryset):
        i = 0
        print('%6s %6s %10s %s' % ('id', 'parent', 'path', 'file'))
        for obj in queryset:
            try:
                print('%6s %6s %10s %s' % (obj.id, obj.parent.id, get_recursive_path(obj), obj.file))
                obj.file.delete()
                obj.save()
                i += 1
            except:
                pass
        if i == 1:  message_bit = "%s object was" % i
        else:       message_bit = "%s objects were" % i
        self.message_user(request, "%s successfully updated." % message_bit)
    clear_files.short_description = "Clear files url for selected Reports"

    list_per_page = 15
    preserve_filters = True
    readonly_fields = ('id', 'uploaded_on',)
    list_display = (
                    'id'      ,
                    'filename',
                    'file'    ,
                    'uploaded_on',
                    'parent'  ,
                    )
    list_display_links = (
                    'id'      ,
                    'filename',
                    )
    list_filter =   (
                    'parent'  ,
                    'uploaded_on',
                    'filename',
                    )
    search_fields = (
                    'filename',
                    'parent'  ,
                    )
    fieldsets = [
        (None,          {'fields': [
                                   (
                                    'id'      ,
                                    'filename',
                                    'file'       ,
                                    'uploaded_on',
                                    'parent'     ,
                                   ),
                                    ]
                        }
        ),
    ]

class ReportInline(admin.TabularInline):
# class ReportInline(admin.StackedInline):
    model = Report
    extra = 0
    readonly_fields = ReportAdmin.readonly_fields
    fieldsets       = ReportAdmin.fieldsets
    list_display    = ReportAdmin.list_display


class FolderInline(admin.TabularInline):
# class FolderInline(admin.StackedInline):
    model = Folder
    extra = 0
    readonly_fields = FolderAdmin.readonly_fields
    fieldsets       = FolderAdmin.fieldsets
    list_display    = FolderAdmin.list_display


class FolderReportAdmin(FolderAdmin):
    inlines = [FolderInline,
               ReportInline,
               ]


admin.site.register(Folder, FolderReportAdmin)
admin.site.register(Report, ReportAdmin)

