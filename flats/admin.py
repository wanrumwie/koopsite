from django.contrib import admin
from .models import Flat, Person

class FlatAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = (
                                    'flat_No'    ,
                                    'rooms'      ,
                                    'entrance_No',
                                    'floor_No'   ,
                    )
    list_filter =   (
                                    'rooms'      ,
                                    'entrance_No',
                                    'floor_No'   ,
                    )
    fieldsets = [
        (None,          {'fields': [
                                   (
                                    'flat_No'    ,
                                   ),
                                   (
                                    'rooms'      ,
                                    'entrance_No',
                                    'floor_No'   ,
                                   ),
                                   (
                                    'note'       ,
                                    'listing'    ,
                                   ),
                                    ]
                        }
        ),
        ('BTI info'  ,  {'fields': [
                                   (
                                    'room1_S'    ,
                                    'room2_S'    ,
                                    'room3_S'    ,
                                   ),
                                   (
                                    'kitchen_S'  ,
                                    'toilet_S'   ,
                                    'bathroom_S' ,
                                   ),
                                   (
                                    'larder1_S'  ,
                                    'larder2_S'  ,
                                    'corridor_S' ,
                                    'loggia_S'   ,
                                   ),
                                   (
                                    's_BTI'      ,
                                    's0_BTI'     ,
                                   ),
                                    ],
                         'classes': ['collapse']
                        }
        ),
        ('plan info' ,  {'fields': [
                                   (
                                    's_plan'     ,
                                    's0_plan'    ,
                                    'bti_plan'   ,
                                    'deviation'  ,
                                   ),
                                   (
                                    'flat_99'    ,
                                   ),
                                    ],
                         'classes': ['collapse']
                        }
        ),
    ]


class PersonAdmin(admin.ModelAdmin):
    actions = ['make_fullnamesplit']
    def make_fullnamesplit(self, request, queryset):
        i = 0
        for obj in queryset:
            full_name = obj.full_name
            try:
                obj.last_name, obj.first_name, obj.middle_name = full_name.split()
                print('full_name=', full_name)
                print(obj.last_name, obj.first_name, obj.middle_name)
                obj.save()
                i += 1
            except:
                pass
        if i == 1:  message_bit = "%s object was" % i
        else:       message_bit = "%s objects were" % i
        self.message_user(request, "%s successfully updated." % message_bit)
    make_fullnamesplit.short_description = "Split full Name for selected Persons"
    list_per_page = 15
    list_display = (
                                    'flat_99'               ,
                                    'person_ID'             ,
                                    'coop_member'           ,
                                    'first_name'            ,
                                    'middle_name'           ,
                                    'last_name'             ,
                                    'full_name'             ,
                    )
    list_filter =   (
                                    'flat_99'               ,
                                    'coop_member'           ,
                    )
    search_fields = (
                                    '^full_name'             ,
                    )
    fieldsets = [
        (None,          {'fields': [
                                   (
                                    'flat'                  ,
                                    'person_ID'             ,
                                    'coop_member'           ,
                                   ),
                                   (
                                    'first_name'            ,
                                    'middle_name'           ,
                                    'last_name'             ,
                                    'full_name'             ,
                                   ),
                                   (
                                    'will_living'           ,
                                    'family_rel'            ,
                                    'birthday'              ,
                                    'year_of_birth'         ,
                                   ),
                                    ]
                        }
        ),
        ('ZEK info'  ,  {'fields': [
                                   (
                                    'if_queue'              ,
                                    'if_retaired'           ,
                                    'if_ZEK'                ,
                                    'old_family_rel'        ,
                                    'on_queue_with'         ,
                                   ),
                                    ],
                         'classes': ['collapse']
                        }
        ),
        ('Queue info',  {'fields': [
                                   (
                                    'queue_in'              ,
                                    'town_sertif_date'      ,
                                   ),
                                   (
                                    'flat_reg_date'         ,
                                    'flat_reg_No'           ,
                                   ),
                                   (
                                    'flat_privil_reg_date'  ,
                                    'flat_privil_reg_No'    ,
                                    'flat_privil_reg_like'  ,
                                   ),
                                   (
                                    'coop_reg_date'         ,
                                    'coop_reg_No'           ,
                                   ),
                                   (
                                    'coop_privil_reg_date'  ,
                                    'coop_privil_reg_No'    ,
                                    'coop_privil_reg_like'  ,
                                   ),
                                    ],
                         'classes': ['collapse']
                        }
        ),
        ('Old info'  ,  {'fields': [
                                   (
                                    'member_pib'            ,
                                    'telephone_old'         ,
                                   ),
                                   (
                                    'experience_from'       ,
                                    'queue_from'            ,
                                    'privilege'             ,
                                    'professor'             ,
                                    'docent'                ,
                                    'if_second'             ,
                                   ),
                                   (
                                    'number_of_people'      ,
                                    'address_old'           ,
                                    'rooms_old'             ,
                                   ),
                                   (
                                    's_old'                 ,
                                    's0_old'                ,
                                    'flat_charact_old'      ,
                                   ),
                                   (
                                    'work'                  ,
                                    'faculty'               ,
                                    'work_from'             ,
                                    'work_from_date'        ,
                                   ),
                                   (
                                    'note'                  ,
                                    'improve_house'         ,
                                    'reg_removal'           ,
                                    'in_Lviv_from'          ,
                                   ),
                                   (
                                    'control_reg_date'      ,
                                    'control_reg_No'        ,
                                    'right_to_add_S'        ,
                                    'add_information'       ,
                                   ),
                                   (
                                    'sex'                   ,
                                    'if_privatized'         ,
                                   ),
                                   (
                                    'entry_protocol_date'   ,
                                    'exit_protocol_date'    ,
                                    'coop_control_reg_No'   ,
                                    'info_about_missed'     ,
                                    'flat_gived_like'       ,
                                    'flat_99'               ,
                                   ),
                                    ],
                         'classes': ['collapse']
                        }
        ),
    ]


class PersonInline(admin.StackedInline):
# class PersonInline(admin.TabularInline):
    model = Person
    extra = 0
    fieldsets = PersonAdmin.fieldsets


class FlatPersonAdmin(FlatAdmin):
    inlines = [PersonInline]


admin.site.register(Flat, FlatPersonAdmin)
# admin.site.register(Flat, FlatAdmin)
admin.site.register(Person, PersonAdmin)

# admin.site.register(UserProfile)

