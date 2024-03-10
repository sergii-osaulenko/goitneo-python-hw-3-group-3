from datetime import datetime, timedelta
from collections import defaultdict
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Birthday must be in the format DD.MM.YYYY.")
        super().__init__(value)

class Record:
    def __init__(self, name, phone):
        self.name = Name(name)
        self.phones = [Phone(phone)]
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if str(phone) != phone_number]

    def edit_phone(self, old_phone_number, new_phone_number):
        for i, phone in enumerate(self.phones):
            if str(phone) == old_phone_number:
                self.phones[i] = Phone(new_phone_number)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = ', '.join(str(phone) for phone in self.phones)
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Name: {self.name}, Phones: {phones_str}{birthday_str}"

class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        today = datetime.today().date()
        next_week = today + timedelta(days=5)
        birthdays_per_week = defaultdict(list)

        for name, record in self.data.items():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
                if today <= birthday_date < next_week:
                    weekdays_diff = (birthday_date - today).days
                    weekday = (today + timedelta(days=weekdays_diff)).strftime('%A')
                    birthdays_per_week[weekday].append(name)

        return birthdays_per_week
    
    def save_to_file(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.data, f)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            print("No address book file found. Starting with empty address book.")

# Test the implementation
if __name__ == "__main__":
    book = AddressBook()
    address_book_file = "address_book.pkl"
    
    # Load existing address book from file, if available
    book.load_from_file(address_book_file)

    # Command handlers
    def handle_add_birthday(command):
        _, name, birthday = command.split()
        if name not in book.data:
            print("Contact does not exist.")
            return
        book.data[name].add_birthday(birthday)
        print(f"Birthday added for {name}.")

    def handle_show_birthday(command):
        _, name = command.split()
        if name not in book.data or not book.data[name].birthday:
            print("Birthday not found for this contact.")
            return
        print(f"{name}'s birthday: {book.data[name].birthday}")

    def handle_birthdays():
        birthdays = book.get_birthdays_per_week()
        if not birthdays:
            print("No birthdays in the next week.")
            return
        for day, names in birthdays.items():
            print(f"{day}: {', '.join(names)}")

    # Command processing loop
    while True:
        command = input("Enter command: ").strip().lower()
        if command.startswith("add "):
            _, name, phone = command.split()
            book.add_record(Record(name, phone))
            print("Contact added successfully.")
        elif command.startswith("change "):
            _, name, new_phone = command.split()
            if name not in book.data:
                print("Contact does not exist.")
            else:
                book.data[name].edit_phone(book.data[name].phones[0].value, new_phone)
                print("Phone number changed successfully.")
        elif command.startswith("phone "):
            _, name = command.split()
            if name not in book.data:
                print("Contact does not exist.")
            else:
                print(f"Phone number for {name}: {book.data[name].phones[0]}")
        elif command == "all":
            for record in book.data.values():
                print(record)
        elif command.startswith("add-birthday"):
            handle_add_birthday(command)
        elif command.startswith("show-birthday"):
            handle_show_birthday(command)
        elif command == "birthdays":
            handle_birthdays()
        elif command == "close" or command == "exit":
            break
        else:
            print("Invalid command. Please try again.")

    # Saving address book to file before exiting
    book.save_to_file(address_book_file)