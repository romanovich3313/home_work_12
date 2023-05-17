from classes import Name, Phone, AddressBook, Record

USERS = AddressBook()


def error_handler(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except KeyError:
            return "No user"
        except ValueError:
            return 'Give me name and phone please'
        except IndexError:
            return 'Enter user name'

    return inner


def hello_user():
    return "How can I help you?"


@error_handler
def add_contact(name, phone):
    name = Name(name)
    phone = Phone(phone)
    record = Record(name, phone)
    result = USERS.add_record(record)
    return f"User {result} added"


@error_handler
def change_phone(name, new_phone):
    if name in USERS:
        old_phone = USERS[name]
        USERS[name] = new_phone
        return f'User {name} has new phone number: {new_phone}, old phone number: {old_phone}'
    else:
        return f'This user: {name} is not in your phone book'


@error_handler
def show_phone(name):
    return f'Phone number for {name}: {USERS[name]}'


def show_all():
    result = ''
    for name, phone in USERS.items():
        result += f'Name: {name}, phone: {phone}\n'
    return result


def unknown_command(command):
    return f"Not command {command}"


def close_bot():
    exit("Good bye")


HANDLERS = {
    'add': add_contact,
    'phone': show_phone,
    'all': show_all,
    'change': change_phone,
    'exit': close_bot,
    'goodbye': close_bot,
    'close': close_bot,
}


def parse_command(command):
    parts = command.split()
    command_name = parts[0]
    if len(parts) > 1:
        command_args = parts[1:]
    else:
        command_args = []
    return command_name, command_args


def main():

    book = AddressBook()
    book.read_from_file('phone_book.dat')

    print(hello_user())
    while True:
        command_line = input('Please enter command and args: ').strip().lower()
        command_name, command_args = parse_command(command_line)
        if command_name in HANDLERS:
            try:
                result = HANDLERS[command_name](*command_args)
                print(result)
            except TypeError:
                print('Invalid input. Please try again.')
        else:
            print(unknown_command(command_name))


if __name__ == '__main__':
    main()
