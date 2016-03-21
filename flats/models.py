from django.db import models
from datetime import date

# Create your models here.

def get_day():
    day=date(1900, 1, 1)
    return day

class Flat(models.Model):
    flat_No     = models.CharField(max_length=5, verbose_name="Квартира №")
    flat_99     = models.IntegerField(default=0, verbose_name="Кв № 99")
    rooms       = models.IntegerField(default=0, verbose_name="Кімнат")
    entrance_No = models.CharField(max_length=5, verbose_name="Під'їзд")
    floor_No    = models.CharField(max_length=5, verbose_name="Поверх")
    room1_S     = models.FloatField(default=0, verbose_name="кімната")
    room2_S     = models.FloatField(default=0, verbose_name="2-га кімната")
    room3_S     = models.FloatField(default=0, verbose_name="3-тя кімната")
    kitchen_S   = models.FloatField(default=0, verbose_name="кухня")
    toilet_S    = models.FloatField(default=0, verbose_name="вбиральня")
    bathroom_S  = models.FloatField(default=0, verbose_name="ванна")
    larder1_S   = models.FloatField(default=0, verbose_name="комора")
    larder2_S   = models.FloatField(default=0, verbose_name="2-га комора")
    corridor_S  = models.FloatField(default=0, verbose_name="коридор")
    loggia_S    = models.FloatField(default=0, verbose_name="лоджія")
    s_BTI       = models.FloatField(default=0, verbose_name="Загальна площа (БТІ)")
    s0_BTI      = models.FloatField(default=0, verbose_name="в тч житлова (БТІ)")
    s_plan      = models.FloatField(default=0, verbose_name="Типовий поверх Загальна")
    s0_plan     = models.FloatField(default=0, verbose_name="Типовий поверх Житлова")
    bti_plan    = models.FloatField(default=0, verbose_name="БТІ - Типовий")
    deviation   = models.FloatField(default=0, verbose_name="% відхилення")
    note        = models.CharField(max_length=10, default='', verbose_name="Примітка")
    listing     = models.IntegerField(default=0, verbose_name="Список")

    def __str__(self):
        return "%-3s" % self.flat_No

    class Meta:
        verbose_name = ('квартира')
        verbose_name_plural = ('квартири')

    mdbTable = "Таблиця Квартири"
    mdbFields = {
                'flat_No'    : "Квартира №",
                'flat_99'    : "Кв № 99",
                'rooms'      : "Кімнат",
                'entrance_No': "Під'їзд",
                'floor_No'   : "Поверх",
                'room1_S'    : "кімната",
                'room2_S'    : "2-га кімната",
                'room3_S'    : "3-тя кімната",
                'kitchen_S'  : "кухня",
                'toilet_S'   : "вбиральня",
                'bathroom_S' : "ванна",
                'larder1_S'  : "комора",
                'larder2_S'  : "2-га комора",
                'corridor_S' : "коридор",
                'loggia_S'   : "лоджія",
                's_BTI'      : "Загальна площа (БТІ)",
                's0_BTI'     : "в тч житлова (БТІ)",
                's_plan'     : "Типовий поверх Загальна",
                's0_plan'    : "Типовий поверх Житлова",
                'bti_plan'   : "БТІ - Типовий",
                'deviation'  : "% відхилення",
                'note'       : "Примітка",
                'listing'    : "Список",
                }
    # список полів, яким можна задати порядок виводу в FlatDetailView
    fieldsList = [
                'flat_No'    ,
                'flat_99'    ,
                'rooms'      ,
                'entrance_No',
                'floor_No'   ,
                'room1_S'    ,
                'room2_S'    ,
                'room3_S'    ,
                'kitchen_S'  ,
                'toilet_S'   ,
                'bathroom_S' ,
                'larder1_S'  ,
                'larder2_S'  ,
                'corridor_S' ,
                'loggia_S'   ,
                's_BTI'      ,
                's0_BTI'     ,
                's_plan'     ,
                's0_plan'    ,
                'bti_plan'   ,
                'deviation'  ,
                'note'       ,
                'listing'    ,
                ]


class Person(models.Model):
    flat                 = models.ForeignKey(Flat)
    first_name           = models.CharField(max_length=100,default='')
    middle_name          = models.CharField(max_length=100,default='')
    last_name            = models.CharField(max_length=100,default='')
    flat_99              = models.IntegerField(default=0)
    person_ID            = models.IntegerField(default=0)
    coop_member          = models.BooleanField(default=False)
    full_name            = models.CharField(max_length=100,default='')
    if_queue             = models.BooleanField(default=False)
    if_retaired          = models.BooleanField(default=False)
    if_ZEK               = models.BooleanField(default=False)
    old_family_rel       = models.CharField(max_length=100,default='')
    on_queue_with        = models.BooleanField(default=False)
    will_living          = models.BooleanField(default=False)
    family_rel           = models.CharField(max_length=20,default='')
    birthday             = models.DateField(default=get_day())
    year_of_birth        = models.IntegerField(default=0)
    queue_in             = models.CharField(max_length=100,default='')
    town_sertif_date     = models.DateField(default=get_day())
    flat_reg_date        = models.DateField(default=get_day())
    flat_reg_No          = models.IntegerField(default=0)
    flat_privil_reg_date = models.DateField(default=get_day())
    flat_privil_reg_No   = models.IntegerField(default=0)
    flat_privil_reg_like = models.CharField(max_length=100,default='')
    coop_reg_date        = models.DateField(default=get_day())
    coop_reg_No          = models.IntegerField(default=0)
    coop_privil_reg_date = models.DateField(default=get_day())
    coop_privil_reg_No   = models.IntegerField(default=0)
    coop_privil_reg_like = models.CharField(max_length=100,default='')
    member_pib           = models.CharField(max_length=100,default='')
    telephone_old        = models.CharField(max_length=20,default='')
    experience_from      = models.IntegerField(default=0)
    queue_from           = models.IntegerField(default=0)
    privilege            = models.CharField(max_length=100,default='')
    professor            = models.BooleanField(default=False)
    docent               = models.BooleanField(default=False)
    if_second            = models.BooleanField(default=False)
    number_of_people     = models.IntegerField(default=0)
    address_old          = models.CharField(max_length=100,default='')
    rooms_old            = models.IntegerField(default=0)
    s_old                = models.FloatField(default=0)
    s0_old               = models.FloatField(default=0)
    flat_charact_old     = models.CharField(max_length=100,default='')
    work                 = models.CharField(max_length=100,default='')
    faculty              = models.CharField(max_length=100,default='')
    work_from            = models.IntegerField(default=0)
    work_from_date       = models.DateField(default=get_day())
    note                 = models.CharField(max_length=100,default='')
    improve_house        = models.BooleanField(default=False)
    reg_removal          = models.BooleanField(default=False)
    in_Lviv_from         = models.CharField(max_length=20,default='')
    control_reg_date     = models.DateField(default=get_day())
    control_reg_No       = models.IntegerField(default=0)
    right_to_add_S       = models.CharField(max_length=100,default='')
    add_information      = models.CharField(max_length=100,default='')
    sex                  = models.CharField(max_length=100,default='')
    if_privatized        = models.BooleanField(default=False)
    entry_protocol_date  = models.DateField(default=get_day())
    exit_protocol_date   = models.DateField(default=get_day())
    coop_control_reg_No  = models.IntegerField(default=0)
    info_about_missed    = models.CharField(max_length=100,default='')
    flat_gived_like      = models.CharField(max_length=100,default='')

    def __str__(self):
        return "Кв.%3s %s" % (self.flat.flat_No, self.full_name)

    class Meta:
        verbose_name = ('особа')
        verbose_name_plural = ('особи')

    mdbTable = "Таблиця Особи"
    mdbFields = {
                'flat_99'               : "Кв № 99",
                'person_ID'             : "Особа ID",
                'coop_member'           : "Член ЖК",
                'full_name'             : "ПІБ",
                'if_queue'              : "Є на черзі",
                'if_retaired'           : "Вибулий член ЖК",
                'if_ZEK'                : "Є в довідці з ЖЕКу",
                'old_family_rel'        : "Старі Родинні відносини",
                'on_queue_with'         : "На черзі разом з",
                'will_living'           : "Буде проживати",
                'family_rel'            : "Родинні відносини",
                'birthday'              : "День народження",
                'year_of_birth'         : "Рік народження",
                'queue_in'              : "Виконком, у якому черга",
                'town_sertif_date'      : "Дата довідки з Ратуші",
                'flat_reg_date'         : "Кварт облік Дата",
                'flat_reg_No'           : "Кварт облік №",
                'flat_privil_reg_date'  : "Кварт Пільг список Дата",
                'flat_privil_reg_No'    : "Кварт Пільг список №",
                'flat_privil_reg_like'  : "Кварт Пільг список як",
                'coop_reg_date'         : "Кооп облік Дата",
                'coop_reg_No'           : "Кооп облік №",
                'coop_privil_reg_date'  : "Кооп Пільг список Дата",
                'coop_privil_reg_No'    : "Кооп Пільг список №",
                'coop_privil_reg_like'  : "Кооп Пільг список як",
                'member_pib'            : "Член кооперативу Прізвище, ініціали",
                'telephone_old'         : "Телефон старий",
                'experience_from'       : "Стаж",
                'queue_from'            : "Черга",
                'privilege'             : "Пільга",
                'professor'             : "Професор",
                'docent'                : "Доцент",
                'if_second'             : "Другий чл сім'ї",
                'number_of_people'      : "К-ть людей",
                'address_old'           : "Адреса стара",
                'rooms_old'             : "К-ть кімнат Стара",
                's_old'                 : "Площа Стара",
                's0_old'                : "Житл пл Стара",
                'flat_charact_old'      : "Х-ка квартири Стара",
                'work'                  : "Посада",
                'faculty'               : "Факультет",
                'work_from'             : "Працює з",
                'work_from_date'        : "Працює з Дата",
                'note'                  : "Примітка",
                'improve_house'         : "Покращення житла",
                'reg_removal'           : "Зняття з обліку",
                'in_Lviv_from'          : "Проживає у Львові з",
                'control_reg_date'      : "Дата внесення в контр список",
                'control_reg_No'        : "№ в контр списку",
                'right_to_add_S'        : "Право на дод площу як",
                'add_information'       : "Додаткова інформація",
                'sex'                   : "Стать",
                'if_privatized'         : "Квартира приватизована",
                'entry_protocol_date'   : "Дата протоколу про вступ",
                'exit_protocol_date'    : "Дата протоклу про вихід",
                'coop_control_reg_No'   : "№ в контр списку Кооп",
                'info_about_missed'     : "Інформація про пропущених",
                'flat_gived_like'       : "Квартира надається з врахуванням",
                }


#---------------- Кінець коду, охопленого тестуванням ------------------
