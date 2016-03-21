'''
##################################################################
# Багаторазово використовуваний клас форми для вводу даних
##################################################################
'''

from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.ttk import Combobox


class ComboForm(): # немодальне вікно форми для вводу даних
    def __init__(self,
                 parent=None,
                 topText='',
                 labels=[],
                 listboxElements=[],
                 entrysize=40):
        # передати список міток полів і значення по-замовч.

        if not parent: parent = Tk()
        labelsize = max(len(label['text']) for label in labels)

        self.setCnf()

        frmForm   = Frame(parent)     # головне вікно форми
        frmForm.grid(row=0, column=0, sticky=NSEW)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        frmTop    = Frame(frmForm)  # місце для заголовків
        frmInput  = Frame(frmForm)  # місце для вводу даних
        frmButton = Frame(frmForm)  # місце для кнопок
        frmOutput = Frame(frmForm)  # місце для виводу
        frmOutTop = Frame(frmForm)  # місце для заголовка виводу
        frmOutBot = Frame(frmForm)  # місце для підсумків виводу

        frmTop   .grid(row=0, column=0, sticky=NSEW)
        frmInput .grid(row=1, column=0, sticky=NSEW)
        frmButton.grid(row=2, column=0, sticky=NSEW)
        frmOutTop.grid(row=3, column=0, sticky=NSEW)
        frmOutput.grid(row=4, column=0, sticky=NSEW)
        frmOutBot.grid(row=5, column=0, sticky=NSEW)

        frmInput .config(cnf=self.frmInputCnf)
        frmButton.config(cnf=self.frmButtonCnf)
        frmOutTop.config(cnf=self.frmOutTopCnf)
        frmOutBot.config(cnf=self.frmOutBotCnf)

        frmForm.columnconfigure(0, weight=1)
        frmForm.rowconfigure(0, weight=0)
        frmForm.rowconfigure(1, weight=0)
        frmForm.rowconfigure(2, weight=0)
        frmForm.rowconfigure(3, weight=0)
        frmForm.rowconfigure(4, weight=1)
        frmForm.rowconfigure(5, weight=0)

        topLabel=Label(frmTop, text=topText)
        topLabel.grid(row=0, column=0, sticky=NSEW)
        topLabel.config(cnf=self.topLabelCnf)
        frmTop.columnconfigure(0, weight=1)
        frmTop.rowconfigure(0, weight=0)

        self.content = {}
        i = 0
        for label in labels:
            lab = Label(frmInput, text=label['text'],
                                  width=labelsize, anchor=E)
            lab.config(cnf=self.labCnf)
            if label.get('listbox'):
                ent = Listbox(frmInput, width=entrysize, height=2)
                for item in label.get('listbox'):
                    ent.insert(END, item)
                ent.config(cnf=self.entCnf)
            elif label.get('combobox'):
                ent = Combobox(frmInput, values=label.get('combobox'),
                               width=entrysize, height=10)
                if label.get('default'):
                    ent.set(label.get('default'))
            else:
                ent = Entry(frmInput, width=entrysize)
                if label.get('default'):
                    # спроба вставити значення по-замовч., якщо є
                    ent.insert(0, label.get('default'))
                ent.config(cnf=self.entCnf)
            lab.grid(row=i, column=0, sticky=NSEW)
            ent.grid(row=i, column=1, sticky=NSEW)
            self.content[label['text']] = ent
            col = 3         # колонка, в яку попаде наступний віджет
            if 'button' in label:   # має бути кнопка праворуч
                but = Button(frmInput, text=label['button'].get('text'),
                             command=lambda label=label: self.onLabelButton(label),
                             cnf=self.buttonCnf)
                but.grid(row=i, column=col, sticky=NW)
                col -= 1    # колонка, в яку попаде наступний віджет
            if 'checkbutton' in label:   # має бути прапорець праворуч
                chb = Checkbutton(frmInput, text=label['checkbutton'].get('text'),
                             command=lambda label=label: self.onLabelCheckButton(label),
                             variable=label['checkbutton'].get('variable'),
                             cnf=self.labCnf)
                chb.grid(row=i, column=col, sticky=NSEW)
                col -= 1    # колонка, в яку попаде наступний віджет
            if col > 1:   # Entry має займати більше, ніж 1 колонку
                ent.grid(columnspan=col)
            frmInput.rowconfigure(i, weight=1)
            i += 1

        frmInput.columnconfigure(0, weight=0)
        frmInput.columnconfigure(1, weight=1)
        frmInput.columnconfigure(2, weight=0)
        frmInput.columnconfigure(3, weight=0)

        # робимо ці об'єкти доступними ззовні
        self.parent = parent
        self.frmButton = frmButton
        self.frmOutput = frmOutput
        self.frmOutTop = frmOutTop
        self.frmOutBot = frmOutBot
        self.listboxElements = listboxElements

        self.setButtons()
        self.setButtonsCnf()

        # створювати scrolledList будемо окремо, тоді коли в головній
        # програмі натиснуть кнопку onSubmit
        # self.makeScrolledList(self.frmOutput, self.listboxElements)

    def setCnf(self):   # задаємо параметри cnf для віджетів
        self.topLabelCnf = {'bd': 2, 'fg': 'black', 'bg': 'lightgrey', 'font': ('times', 10, 'bold')}
        self.labCnf      = {'bd': 2, 'fg': 'black', 'bg': '#e6e6e6'  , 'font': ('times', 10, 'normal')}
        self.entCnf      = {'bd': 2, 'fg': 'black', 'bg': 'white'    , 'font': ('times', 10, 'normal')}
        self.buttonCnf   = {'bd': 2, 'fg': 'black', 'bg': 'lightgrey', 'font': ('times', 10, 'bold')}
        self.frmInputCnf = {'bd': 2,                'bg': '#e6e6e6'  }
        self.frmButtonCnf= {'bd': 2,                'bg': 'lightgrey'}
        self.frmOutTopCnf= {'bd': 2,                'bg': '#e6e6e6'  }
        self.frmOutBotCnf= {'bd': 2,                'bg': '#e6e6e6'  }

    def setButtons(self):
        cancelButton = Button(self.frmButton, text='Quit',       command=self.onCancel)
        adminButton  = Button(self.frmButton, text='Admin',      command=self.onAdmin)
        submitButton = Button(self.frmButton, text='Submit',     command=self.onSubmit)
        newsubButton = Button(self.frmButton, text='Submit New', command=self.onNewSubmit)
        cancelButton.grid(row=0, column=4, sticky=NSEW)
        adminButton .grid(row=0, column=3, sticky=NSEW)
        submitButton.grid(row=0, column=1, sticky=NSEW)
        newsubButton.grid(row=0, column=2, sticky=NSEW)
        self.frmButton.master.bind('<Return>', (lambda event: self.onSubmit()))
        self.cancelButton = cancelButton
        self.adminButton  = adminButton
        self.submitButton = submitButton
        self.newsubButton = newsubButton

    def setButtonsCnf(self):
        self.cancelButton.config(cnf=self.buttonCnf)
        self.adminButton .config(cnf=self.buttonCnf)
        self.submitButton.config(cnf=self.buttonCnf)
        self.newsubButton.config(cnf=self.buttonCnf)

    def onLabelButton(self, label):
        func = label['button'].get('command')
        args = self.content[label['text']].get()
        res = func(*args)
        if res:
            self.content[label['text']].delete(0, END)
            self.content[label['text']].insert(0, res)

    def onLabelCheckButton(self, label):
        var  = label['checkbutton'].get('variable')
        func = label['checkbutton'].get('command')
        args = self.content[label['text']].get()
        if func:
            res = func(var, var.get(), args)

    def onSubmit(self):                             # перевизначити цей метод
        for key in self.content:                    # ввід користувача
            print(key, '\t=>\t', self.content[key].get()) # в self.content[k]

    def onCancel(self):                     # перевизначити при необхідності
        Tk().quit()                         # по замовченню здійснюється вихід

    def onAdmin(self):                     # перевизначити при необхідності
        pass

    def onNewSubmit(self):                     # перевизначити при необхідності
        pass

class DynamicForm(ComboForm):
    def __init__(self, labels=None):
        labels = input('Enter field names: ').split()
        Combobox.__init__(self, labels)
    def onSubmit(self):
        print('Field values...')
        ComboForm.onSubmit(self)
        self.onCancel()


if __name__ == '__main__':

    root = Tk()

    caseSensitive = IntVar()    # примірник класу tkinter - булівська змінна

    def printCheckButtonVar(*args):   # функція друку змінної в Checkbutton
        print(*args)

    # Заголовок
    topText='Введіть аргументи до виконання для функції execute_from_command_line'
    # execute_from_command_line(['manage.py','test', 'koopsite'])

    # Назви полів вводу Label
    arg1Label = 'Перший аргумент'
    arg2Label = 'Другий аргумент'
    arg3Label = 'Третій аргумент'
    arg3dotLabel = 'Розділовий знак'
    arg3addLabel = 'Додатковий аргумент'

    # Початкові дані в Entry
    arg1 = 'manage.py'
    arg2 = 'test'
    arg3 = 'functional_tests.koopsite'
    arg3dot = '.'
    arg3add = ['alfa', 'beta', 'gama']
    arg3add0 = 'beta'

    # Формування labels - області вводу даних
    # Кожен з labels має віджети Label і Entry
    # і може мати віджети Button і Checkbutton
    labels = []
    labels.append({'text'   : arg1Label,
                   'default': arg1,
                   'button' : {'text'   : '...',
                               'command': printCheckButtonVar,
                               },
                   })
    labels.append({'text'   : arg2Label,
                   'default': arg2,
                   # 'button' : {'text'   : '###',
                   #             'command': printCheckButtonVar,
                   #             },
                   'checkbutton': {'text': 'Case sensitive',
                                   'command': printCheckButtonVar,
                                   'variable': caseSensitive,
                                   },
                   })
    labels.append({'text': arg3Label,
                   'default': arg3,
                   })
    labels.append({'text': arg3dotLabel,
                   'default': arg3dot,
                   })
    labels.append({'text': arg3addLabel,
                   'default': arg3add0,
                   'combobox': arg3add,
                   })

    ComboForm(parent=root, topText=topText, labels=labels)
    mainloop()
