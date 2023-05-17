from collections import UserDict
from datetime import datetime, date
import re
import pickle


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, it):
        records = list(self.data.values())
        for i in range(0, len(records), it):
            yield records[i : i + it]

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def read_from_file(self, filename):
        with open(filename, "rb") as file:
            data = pickle.load(file)
        return data

    def search(self, keyword):
        results = []
        keyword = keyword.lower()
        for record in self.data.values():
            if keyword in record.name.value.lower():
                results.append(record)
            for phone in record.phones:
                if keyword in phone.value.lower():
                    results.append(record)
                    break
        return results

class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday) if birthday else None
        self.phones = []
        if phone is not None:
            self.phones.append(phone)

    @property
    def phones(self):
        return self.__phones

    @phones.setter
    def phones(self, phones):
        self.__phones = phones

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday):
        self.__birthday = birthday

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def change_phone(self, old_phone, new_phone):
        old_index = self.phones.index(old_phone)
        self.phones[old_index] = new_phone

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = date.today()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        days_to_birthday = (next_birthday - today).days
        return days_to_birthday


class Field:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    def __init__(self, name: str):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        self.value = phone

    @Field.value.setter
    def value(self, phone):
        if not isinstance(phone, str) or len(phone) != 10:
            raise ValueError("Invalid phone number")
        self._value = phone[:3] + "-" + phone[3:6] + "-" + phone[6:]


class Birthday(Field):
    def __init__(self, birthday):
        # self._value = None
        self.value = birthday

    @Field.value.setter
    def value(self, birthday):
        try:
            dt = datetime.strptime(birthday, "%d.%m.%Y")
        except (ValueError, TypeError):
            raise Exception("Invalid birthday. Only string format dd.mm.yyyy")
        Field.value.fset(self, dt.date())


book = AddressBook()


record1 = Record('John Doe', Phone('1234567890'), '01.01.1990')
record2 = Record('Jane Smith', Phone('9876543210'), '15.05.1985')
record3 = Record('Mike Johnson', Phone('4567890123'), '10.10.1995')

book.add_record(record1)
book.add_record(record2)
book.add_record(record3)

book.save_to_file('address_book')


# record = Record("roma", "10.12.1995")
# record2 = Record("roma", "20.12.1995")
# print(record.birthday)  # none!!!!!!!!!!!!!!!!!!!!!!!!!!

# record.add_phone("23343434")
# book.add_record(record)
# print(record)

# name = Name("Ivan")
# phone = Phone("0958887481")
# birthday = Birthday("20.05.95")

# rec = Record(name, phone, birthday)
# book.add_record(rec)
# print(rec.days_to_birthday())

# record = Record("roma", "10-12-1995")
# record.add_phone("23343434")
# record.add_phone("23343434")
# record.add_phone("49586548")

# book.add_record(record)
# print(record)

# name = Name("Ivan")
# phone = Phone("095-888-7481")
# birthday = Birthday("20-05-95")

# rec = Record(name, phone, birthday)
# book.add_record(rec)
# print(rec.days_to_birthday())
