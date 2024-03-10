import pickle

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
        next_week = today + timedelta(days=7)
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

    # Command handlers...
    # (Code for command handlers remains the same)

    # Command processing loop...
    # (Code for command processing loop remains the same)

    # Saving address book to file before exiting
    book.save_to_file(address_book_file)