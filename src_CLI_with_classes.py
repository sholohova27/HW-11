import json
# эта ошибка возникала при пустом файле contacts.json, ментор посоветовал импортировать ее явно
from json.decoder import JSONDecodeError
from src_classes import Name, Phone, Record, AddressBook

# Загружаем словарь из файла или создаем пустой словарь (для сохранения данных)
def read_contacts(file_name):
    try:
        with open(file_name, 'r') as f:
            contacts = json.load(f)
    except (FileNotFoundError, AttributeError, JSONDecodeError):
        contacts = {}
    return contacts


# Записываем контакты в файл
def save_contacts(file_name, contacts):
    with open(file_name, 'w') as f:
        if contacts:
            json.dump(contacts, f)


def Index_Key_error_func(func):
    def inner(*args, **kwargs):
        name = Name(args[0].strip().lower())
        contacts = AddressBook(kwargs['contacts'])

        try:
            return func(*args, **kwargs)
        except IndexError:
            return f'Print name and phone/s number via space', contacts
        except KeyError:
            return f'Contact {name} is absent', contacts
    return inner

# contacts возвращаем для того, чтобы сигнатура ф-й была одинаковая,
# kwargs['contacts']: 'contacts' это также ключ, по к-му можно найти в kwargs словарь contacts
def hello_func(*args, **kwargs):
    contacts = kwargs['contacts']
    return "How can I help you?", contacts

def help_func(*args, **kwargs):
    contacts = kwargs['contacts']
    return ''' 
               For adding Contacts type "add"
               To change Contacts type "change"
               To get Contact`s phone number type "phone" and Contact`s name after
               To get all Contacts "show all"
               To delete Contact type "delete"
               To exit type "bye"/"close"/"exit"/"." 
            ''', contacts


# передаем словарь Contacts из ф-и main в качестве аргумента
@Index_Key_error_func
def add_func(*args, **kwargs):
# делаем наши переменные объектами соответствующих классов
# и переносим их с блока try в начало ф-и
# contacts делается экземпляром класса в мейне
    contacts = kwargs['contacts']
    name = Name(args[0].strip().lower())
    phones = [Phone(phone.strip().lower()) for phone in args[1:]]
# создаем новую переменную rec, чтобы работать с классом Record
    rec = Record(name, phones)
    try:
# Забираем первый и второй элемент, т.к. ф-я handler, которую вызываем в мейне,
# возвращает ф-ю и очищенный от команды список, к-й распаковывается через * в
# позиционные параметры add_funс (в мейне): result, contacts = func(*text, Contacts=Contacts)
# без маг. метода hash в классе тут будет ошибка
        if not contacts.get(name):
# вместо contacts[name] = phone присваиваем метод класса AddressBook
            contacts.add_record(rec)
            # contacts[name] = phone
        else:
            return f'{name} already exists. Use "change" command to change number', contacts
    except AttributeError:
        pass
    return f"Contact {name} with phone {phones} successfully added", contacts

@Index_Key_error_func
def change_func(*args, **kwargs):
    contacts = kwargs['contacts']
# Забираем первый и второй элемент, т.к. ф-я handler, которую вызываем в мейне,
# возвращает ф-ю и очищенный от команды список, к-й распаковывается через * в
# позиционные параметры add_funс (в мейне): result = func(*text, Contacts=Contacts)
    name = Name(args[0].strip().lower())
    #old_phone = contacts.get(name) Це буде не old_phone, а екземпляр Record
    # contacts[name] = ""
    old_phone = Phone(args[1].strip().lower()) # буде на першій позиції в аргсах
    new_phone = Phone(args[2].strip().lower()) # буде на другій позиції в аргсах
    # rec = Record(name,new_phone) екземпляр Record потрібно дістати з книги контактів
    # если имени нет в словаре, оно добавится, если нет - поменяется номер
    # contacts[name] = new_phone
    # метод edit_phone у нас для списка, мы извлекаем список по ключу словаря
    # if name in [str(Name(key)) for key in contacts.keys()]: # невже це зручно читати?)))
    if contacts.get(str(name)):
        contacts.get(str(name)).edit_phone(old_phone, new_phone)
    # rec = contacts.get(str(name))
    # без str не работает, либо rec = contacts.get(name.value)
    # if rec:
    #     rec.edit_phone(old_phone, new_phone)
        return f"Phone for contact {name} changed successfully.\nOld phone {old_phone}, new phone {new_phone}", contacts
    # return f"Phone {new_phone} for contact {name} added successfully.", contacts # Якщо change буде додавати нові номери, то це не зовсім логічно(
    return f"Contact {name} doesn't exist", contacts




@Index_Key_error_func
def del_func(*args, **kwargs):
    contacts = kwargs['contacts']
# Забираем первый и второй элемент, т.к. ф-я handler, которую вызываем в мейне,
# возвращает ф-ю и очищенный от команды список, к-й распаковывается через * в
# позиционные параметры add_funс (в мейне): result = func(*text, Contacts=Contacts)
    name = Name(args[0].strip().lower())
    # без str не находит ключ! (либо добавлять value)
    contacts.pop(str(name))
    return f"Contact {name} successfully deleted", contacts

@Index_Key_error_func
def phone_func(*args, **kwargs):
    contacts = kwargs['contacts']
    name = Name(args[0].strip().lower())
    return str(contacts.get(str(name))), contacts



def show_all_func(*args, **kwargs):
    contacts = kwargs['contacts']
    return '\n'.join([f'{name} : {phone}' for name, phone in contacts.items()]), \
           contacts


def unknown_command(*args, **kwargs):
    contacts = kwargs['contacts']
    return "Sorry, unknown command. Try again", contacts


def exit_func(*args, **kwargs):
    contacts = kwargs['contacts']
    return "Bye", contacts

# Ф-я handler проверяет, является ли введенный текст командой, сверяясь со словарем MODES,
# и возвращает нужную ф-ю, а также текст после команды
# никаких изменений в связи с перестройкой на классы
def handler(text):
    for command, func in MODES.items():
        if text.lower().startswith(command):
            return func, text.replace(command,'').strip().split()
    # else тут нельзя, он вернет только 1-ю ф-ю словаря MODES, если ей соответствует введенная
    # команда, но следующей ф-ции она уже соответствовать не будет, поэтому вернет unknown_command для всех остальных
    return unknown_command, []
# у ретернов должна быть одинаковая структура, поэтому после 2-го возвращаем [] (None приводит к ошибке, потому что его нельзя распаковать *),
# и обязательно добавляем 2-ю переменную в ф-и Main (func, text = handler(input('>>>'))), т.к. handler возвращает 2
# и теперь нужно добавить в каждую ф-цию параметр *args, потому что в ф-ции теперь нужно передавать этот параметр тоже


# Создаем словарь MODES из всех промежуточных ф-ций (каррирование)
MODES = {"hello": hello_func,
         "add": add_func,
         "change": change_func,
         "help": help_func,
         "delete": del_func,
         "phone": phone_func,
         "show all": show_all_func,
         "close": exit_func,
         "exit": exit_func,
         "bye": exit_func,
         ".": exit_func}


# Передаем имя файла и путь к файлу с контактами в качестве аргументов
def main(file_name):
    # делаем словарь экземпляром объекта AddressBook, и все, contacts только тут, не нужно делать то же самое и  перезаписывать в ф-циях
    contacts = AddressBook(read_contacts(file_name))
    while True:
        # Ф-я handler проверяет, является ли введенный текст командой, сверяясь со словарем MODES,
        # и возвращает нужную ф-ю, а также список из текста после команды
        func, text = handler(input('>>>'))
        # можно просто result, но так легче масштабировать, перезаписывая в contacts
        # вместо исходного словаря результат выполнения ф-ций
        result, contacts = func(*text, contacts = contacts)
        print(result)
        if func == exit_func:
            save_contacts(file_name, contacts)
            break




# Проверяем, что скрипт запущен как основной
if __name__ == '__main__':
    file_name = 'contacts.json'
    main(file_name)