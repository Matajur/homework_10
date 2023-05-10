from collections import UserDict


class Field:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self):
        return f'{self.value}'


class Name(Field):
    def __init__(self, name: str) -> None:
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone: str) -> None:
        super().__init__(phone)

    def __repr__(self) -> str:
        return str(self)


class Record:
    def __init__(self, name: Name):
        self.name = name
        self.phones = []

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def remove_phones(self):
        self.phones.clear()

    def change_phones(self, phone: Phone):
        self.phones = [phone]

    def __str__(self) -> str:
        return f'Contact Name: {self.name} with Phones: {self.phones if self.phones else "None"}'

    def __repr__(self) -> str:
        return str(self)


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def __str__(self) -> str:
        return '\n'.join(str(record) for record in self.data.values())


address_book = AddressBook()


def input_error(func):
    def inner(*args):
        try:
            if args:
                if args[1]:
                    int(args[1])
            result = func(*args)
        except TypeError:
            result = 'Wrong name or phone'
        except UnboundLocalError:
            result = 'Unknown command'
        except ValueError:
            result = 'Wrong phone format'
        except KeyError:
            result = f'Name: {args[0]} not in address book'
        return result
    return inner


def unknown_command(command: str) -> str:
    return f'Unknown command "{command}"'


def hello_user(*args) -> str:
    return 'How can I help you?'


def exit_func(*args) -> str:
    return 'Goodbye!'


@input_error
def add_contact(name: str, phone=None) -> str:
    if name in address_book.data.keys():
        return f'Contact Name: {name} already exists'

    record_name = Name(name)
    record = Record(record_name)

    if phone:
        record_phone = Phone(phone)
        record.add_phone(record_phone)

    address_book.add_record(record)

    return f'Added contact Name: {record.name} with Phone: {record.phones if record.phones else "None"}'


@input_error
def append_phone(name: str, phone: str) -> str:
    record = address_book.data[name]

    for ph in record.phones:
        if ph.value == phone:
            return f'Phone: {phone} for contact Name: {record.name} already exists'

    record_phone = Phone(phone)
    record.add_phone(record_phone)

    return f'Contact Name: {record.name} new Phones: {record.phones}'


@input_error
def phones_remove(name: str) -> str:
    record = address_book.data[name]

    record.remove_phones()
    return f'{record}'


@input_error
def phone_change(name: str, phone: str) -> str:
    record = address_book.data[name]

    record_phone = Phone(phone)
    record.change_phones(record_phone)
    return f'Contact Name: {record.name} has new Phone: {record.phones}'


@input_error
def show_contact(name: str) -> str:
    record = address_book.data[name]

    return f'{record}'


@input_error
def show_all() -> str:
    if address_book.data:
        result = 'Showing all contacts'
        for key, contact in address_book.data.items():
            result += f'\n{contact}'
    else:
        result = 'No contacts, please add'
    return result


commands = {
    'hello': hello_user,
    'add contact': add_contact,
    'add phone': append_phone,
    'change': phone_change,
    'remove phones': phones_remove,
    'show all': show_all,
    'phone': show_contact,
    'exit': exit_func,
    'goodbye': exit_func,
    'good bye': exit_func,
    'close': exit_func,
}


def main():
    while True:
        phrase = input('Please enter request: ').strip()
        command = None
        for key in commands:
            if phrase.lower().startswith(key):
                command = key
                break

        if not command:
            result = unknown_command(phrase.split(' ', 1)[0])
        else:
            data = phrase[len(command):].strip()
            if data:
                if ', ' in data:
                    data = data.split(', ', 1)
                else:
                    data = data.rsplit(' ', 1)

            handler = commands.get(command)
            result = handler(*data)
            if result == 'Goodbye!':
                print(result)
                break
        print(result)


if __name__ == '__main__':
    main()
