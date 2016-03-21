from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from .models import UserProfile

admin.site.site_header  = 'koop administration'
admin.site.site_title   = 'koop site admin'
admin.site.index_title  = 'Адміністрація сайту'
# admin.site.site_url = r'localhost:8080/index/'

class UserAdmin(admin.ModelAdmin):
    list_per_page = 15
    preserve_filters = True
    readonly_fields = ('id', 'username',)
    list_display = (
                    'id',
                    'username',
                    'first_name',
                    'last_name',
                    'password',
                    'email',   
                    )
    list_display_links = (
                    'id',
                    'username',
                    )
    list_filter =   (
                    'first_name',
                    'last_name',
                    'email',   
                    )
    search_fields = (
                    'username',
                    'first_name',
                    'last_name',
                    'email',   
                    )
    fieldsets = [
        (None,          
         {'fields': [
                   (
                    'id',
                    'username',
                    'first_name',
                    'last_name',
                    'password',
                    'email',   
                   ),
                    ]
        }
        ),
    ]

class ProfileAdmin(admin.ModelAdmin):
    list_per_page = 15
    preserve_filters = True
    readonly_fields = ('id', 'user',)
    list_display = (
                    'user',
                    'id',
                    'flat',
                    'picture',
                    )
    list_display_links = (
                    'id',
                    )
    list_filter =   (
                    'flat',
                    )
    search_fields = (
                    'user',
                    'flat',
                    )
    fieldsets = [
        (None,
         {'fields': [
                   (
                    'user',
                    'id',
                    'flat',
                    'picture',
                   ),
                    ]
        }
        ),
    ]

class UserInline(admin.TabularInline):
    model = User
    extra = 0
    readonly_fields = UserAdmin.readonly_fields
    fieldsets       = UserAdmin.fieldsets
    list_display    = UserAdmin.list_display

class ProfileInline(admin.TabularInline):
    model = UserProfile
    extra = 0
    readonly_fields = ProfileAdmin.readonly_fields
    fieldsets       = ProfileAdmin.fieldsets
    list_display    = ProfileAdmin.list_display


class UserProfileAdmin(UserAdmin):
    inlines = [UserInline,
               ProfileInline,
               ]


# admin.site.register(User, UserProfileAdmin)
admin.site.register(UserProfile, ProfileAdmin)
#

