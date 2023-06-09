from collections import UserDict
from datetime import datetime


# родительский
class Field:
    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("Value must be string")
        else:
            self.value = value

    # теперь при вызове экземпляра объекта будет выводиться его имя, а не ячейка памяти
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)

    # obj.value -> AttributeError, хотя так писать правильнее
    def __eq__(self, obj):
        return self.value == obj.value

    def __hash__(self):
        return hash(self.value)


# поле с именем
class Name(Field):
    pass


# поле с телефоном (отказалась от наследования, т.к. были ошибки
class Phone(Field):
    def __init__(self, phone = None):
        super().__init__(phone)
        self.__phone = None
        self.phone = phone

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        if len(value) <= 5:
            raise ValueError('Phone number must have more then 5 digits')
        self.__phone = value


class Birthday(Field):
    def __init__(self, bday=None):
        super().__init__(bday)
# скрытое поле нужно для геттеров/сеттеров, чтобы не уйти в рекурсию
        self.__bday = None
        self.bday = bday

# геттер для поля bday, в этоу ветку он пойдет, если будут соблюдены условия в сеттере
    @property
    def bday(self):
        return f'{self.__bday}'

# сеттер для поля bday !!! Вводится новое для класса поле value
    @bday.setter
    def bday(self, value):
        try:
            datetime.strptime(value, '%d %B %Y')
            self.__bday = value
        except ValueError:
            raise ValueError(f'Write birthday in format like "27 August 1987"') from None

    # добавление/удаление/редактирование
class Record:
    def __init__(self, name: Name, phones: list[Phone] = None, bday = None):
        self.name = name
        self.phones = phones
        self.bday = bday

    def add_phone(self, phone: Phone):
        self.phones.append(phone)
        return f"Contact {self.name} with {phone} phone number has been added"

    def del_phone(self, phone: Phone):
        for phone in self.phones:
            self.phones.remove(phone)
            return f"Phone number {phone} has been deleted from contact {self.name}"
        return f'{phone} not in list'

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        if old_phone in self.phones:
            self.del_phone(old_phone)
            self.add_phone(new_phone)
            return f"Phone number {old_phone} has been substituted with {new_phone} for contact {self.name}"
        return f'{old_phone} not in list'

    def days_to_birthday(self, bday:Birthday):
        bday = datetime.strptime(bday, '%d %B %Y')
        now = datetime.now()
        bday_day = bday.day
        bday_month = bday.month
        bday_year = bday.year
        bday_cur_Y = datetime(year = now.year, month = bday_month, day = bday.day)
        diff = bday_cur_Y - now
        if (bday_cur_Y - now).days >= 0:
            diff = bday_cur_Y - now
        if (bday_cur_Y - now).days < 0:
            bday_next_Y = datetime(year = now.year + 1, month = bday_month, day = bday.day)
            diff = bday_next_Y - now
        return f'{diff.days} days left to your birthday'


    def __str__(self):
        return f'{self.phones}'

    def __repr__(self):
        return str(self)

# Nata_bd = Birthday('27 August 1987')
# name1 = Record("Nataly", ["+34"])
# print(name1.days_to_birthday("27 August 1987"))
# print(name1.add_phone("44"))
# print(name1.phones)
# name2 = Name('Andrew')
# print(name2)
# phone2 = Phone('0956985211')
# print(phone2)
# record2 = Record(name2, phone2)
# print(record2.phones)
# print(name1.del_phone('4487654'))
# print(name1.edit_phone("44006600", "38"))


# поиск по записям
class AddressBook(UserDict):
    # ожидает поля объекта Record (name, phone)
    def add_record(self, record: Record):
        # эта запись приводила к проблемам с сериализацией: if record.name == self.get('name')
        if self.get(record.name.value):
            return f'{record.name.value} is already in contacts'
        # data - поле UserDict
        # т.к. в классе Name есть маг. метод __str__, можно просто record.name
        # добавили value и-за проблем с сериализацией
        self.data[record.name.value] = [record.phones, record.bday]
        return f'{record.name.value} with {record.phones} phone and birthday {record.bday}  is successfully added in contacts'

    def show_all(self):
        return self.data

    def phone(self, name):
        try:
            return self.data[name]
        except KeyError:
            return f'Contact {name} is absent'

    def paginator(self, records_num):
        start = 0
        while True:
            # превращаем в список ключи словаря и слайсим
            result_keys = list(self.data)[start: start + records_num]
            # превращаем список ключей словаря в список строк с форматом "ключ : [значение]"
            result_list = [f"{key} : {self.data.get(key)}" for key in result_keys]
            if not result_keys:
                break
            yield '\n'.join(result_list)
            start += records_num

    def to_dict(self):
        contacts_dict = {}
        for key, value in self.contacts.items():
            contacts_dict[key] = {"phones": [str(phone) for phone in value.phones], "birthday": value.bday}
        return contacts_dict

    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return '\n'.join([str(r) for r in self.values()])



