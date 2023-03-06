import pickle
from collections import UserDict
from datetime import datetime, timedelta

class AddressBook(UserDict):
    file_name = 'AddressBook.bin'

    def show_all_records(self):
        return self.data

    def iterate(self, n=1):
        for key, value in self.data.items():
            d_list = list(self.data.values())
            for i in range(0, len(d_list), n):
                yield key, d_list[i:i + n]

    def add_record(self, record):
        self.data[record.name.value] = record

    def save_contacts(self):
        with open(self.file_name, 'wb') as f:
            pickle.dump(self.data, f)
        print(f'Your contact saved!')

    def load_contacts(self):
        try:
            with open(self.file_name, 'rb') as f:
                self.data = pickle.load(f)
            print(self.data)
        except:
            return


class Record:
    def __init__(self, name, phone=None, email=None, birthday=None):
        self.name = name
        self.email = email
        self.birthday = birthday

        self.phones = []
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone):
        self.phones.append(phone)
        print(self.phones)

    def days_to_birthday(self):
        if self.birthday:
            now = datetime.now().date()
            bday2 = self.birthday.value.split('.')
            b = datetime(year=now.year, month=int(bday2[1]),day=int(bday2[0])).date()
            next = b - now
            if next.days < 0:
                b = datetime(year=now.year + 1, month=int(bday2[1]),
                             day=int(bday2[0])).date()
                print(b - now)
            else:
                next = b - now
                print(next)


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value


class Name(Field):
    pass


class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not value.startswith('+'):
            raise ValueError
        if len(value) != 13:
            raise ValueError


class Email(Field):
    pass


class Birthday(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def set_value(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except:
            raise ValueError


def main():
    address_book = AddressBook()
    address_book.load_contacts()
    while True:
        user_inp = input('Enter command: ').lower().strip()
        user_exit_list = ['good bye', 'close', 'exit', '.']
        if user_inp in user_exit_list:
            print('Good bye!\n'
                  'Your entries have been successfully saved!')
            break
        elif user_inp == 'hello':
            print('How can I help you?')
            continue
        elif 'add' in user_inp:
            add_handler(address_book)
        elif 'find' in user_inp:
            find_handler(address_book)
        elif 'show all' in user_inp:
            show_all_handler(address_book)
        else:
            print('You can use following commands:\n'
                  'add - Add new contact\n'
                  'find - Find contact in Address Book\n'
                  'show all - Shows the entire Address Book\n'
                  'close, exit, good bye or . - Closing the program\n')
            continue


def add_handler(address_book):
    user_name = input("Enter contact name: ")
    if not user_name:
        print("Contact name is required")
        return
    else:
        name = Name(user_name)

    record = Record(name)

    user_phone = input("Enter contact phone: ")
    if user_phone:
        phone = Phone(user_phone)
        record.phone = phone

    user_email = input("Enter contact email: ")
    if user_email:
        email = Email(user_email)
        record.email = email

    user_birthday = input("Enter contact Birthday: ")
    if user_birthday:
        birthday = Birthday(user_birthday)
        record.birthday = birthday
    address_book.add_record(record)
    address_book.save_contacts()


def show_all_handler(address_book):
    data = address_book.show_all_records()
    for record, v in data.items():
        print(record, v)


def find_handler(address_book):
    find_user = input('Enter contact name or phone: ')
    data = address_book.show_all_records()
    for name, record in data.items():
        if name.startswith(find_user):
            print(name)
        phone = getattr(record, 'phone', '')
        if phone:
            if phone.value.startswith(find_user):
                print(phone.value)


if __name__ == "__main__":
    main()

