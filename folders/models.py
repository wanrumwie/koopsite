import os
from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from koopsite.fileExtIconPath import get_viewable_extension_list


class Folder(models.Model):
    name        = models.CharField(max_length=256,
                                      verbose_name='Тека',
                                      error_messages={
                                         # інші помилки переозначені на поч. цього модуля
                                      'unique': "Така назва вже існує!"},
                                      )
    parent      = models.ForeignKey('self',
                                      verbose_name='Материнська тека',
                                      related_name='children',
                                      default=None,
                                      null=True,
                                      blank=True)
    created_on  = models.DateTimeField(verbose_name='Дата створення',
                                      # auto_now_add=True,
                                      null=True,
                                      blank=True)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('folders:folder-detail', kwargs={'pk': self.pk})
        # return reverse('folders:folder-contents', kwargs={'pk': self.pk})
        # return reverse('folders:folder-list-all')

    class Meta:
        verbose_name = ('тека')
        verbose_name_plural = ('теки')
        unique_together = (("parent", "name"),)
        permissions = (
                        ('view_folder', 'Can view folder'),
                        ('download_folder', 'Can download folder'),
        )


def get_report_path(report_id):
    # Повертає абс.шлях до файла (відносно MEDIA_ROOT)
    # Замість первісної назви файла використовується його id
    # Файли фізично записуються в теку з номером k = id // 512
    k = report_id // 512
    file_path = os.path.join('uploads',
                        'folders',      # підтека з назвою аплікації
                        str(k),         # тека для кожних 512 файлів
                        str(report_id)  # id файла
                        + ".data")       # фіктивне розширення файла
    # print('get_report_path:', report_id, k, file_path)
    return file_path


class Report(models.Model):
    def get_file_path(instance, filename):
        # Ця ф-ція призначена для динамічної зміни значення
        # параметра upload_to -  шляху збереження
        # файлів моделі (поля ImageField, FileFild)
        # Оскільки значення параметра upload_to є функцією (callable),
        # то вона автоматично приймає своїми параметрами instance і filename
        # з чого генерує стрічку - шлях збереження файлів:
        # upload_to=/uploads/folders/id/filename - СТАРИЙ ВАРІАНТ
        # upload_to=/uploads/folders/folder_id/file_id - НОВИЙ ВАРІАНТ
        # upload_to=/uploads/folders/k/file_id - НОВІШИЙ ВАРІАНТ,
        #   де k=id mod 512 - для кожних 512 файлів відкриватимемо нову теку
        # Але id визначається базою даних при збереженні, тому
        # для новоствореного запису id=None
        instance.filename = filename # в БД запишеться первинне ім'я файла
        file_path = get_report_path(instance.id)
        return file_path

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_file = self.file
            self.file = None
            super(Report, self).save(*args, **kwargs)
            self.file = saved_file
        super(Report, self).save(*args, **kwargs)

    parent   = models.ForeignKey(Folder,
                                      verbose_name='Тека',
                                      related_name='reports',
                                      default=None)
    file     = models.FileField(verbose_name='Файл',
                                      upload_to=get_file_path,
                                      # null=True,
                                      # blank=True)
                                      default=None)
    filename = models.CharField(verbose_name='Назва файлу',
                                      max_length=512,
                                      null=True)
                                      # blank=True)
    uploaded_on  = models.DateTimeField(verbose_name='Дата заладування',
                                      auto_now_add=True,
                                      null=True,
                                      blank=True)
    user     = models.ForeignKey(User,
                                      verbose_name='Автор',
                                      related_name='reports',
                                      null=True,
                                      blank=True)

    def __str__(self):
        s = self.filename or ''
        return s

    def get_absolute_url(self):
        try:
            fileExt = os.path.splitext(self.filename)[1]  # [0] returns path+filename
        except:
            fileExt = ""
        if fileExt in get_viewable_extension_list():
            url_name = 'folders:report-preview'
        else:
            url_name = 'folders:report-detail'
        return reverse(url_name, kwargs={'pk': self.pk})
        # return reverse('folders:folder-list-all')

    class Meta:
        verbose_name = ('файл')
        verbose_name_plural = ('файли')
        permissions = (
                        ('view_report', 'Can view report'),
                        ('download_report', 'Can download report'),
        )

#---------------- Кінець коду, охопленого тестуванням ------------------
