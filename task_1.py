from datetime import datetime, timedelta
from collections import defaultdict

def get_next_birthday(birthday):
    today = datetime.today().date()
    birthday_this_year = birthday.replace(year=today.year)
    
    if birthday_this_year < today:
        birthday_this_year = birthday_this_year.replace(year=today.year + 1)
    
    return birthday_this_year

def get_weekday(date):
    return date.strftime('%A')

def get_birthdays_per_week(users):
    birthdays_per_week = defaultdict(list)
    days_in_week = 7
    
    for user in users:
        name, birthday = user["name"], user["birthday"].date()
        birthday_this_year = get_next_birthday(birthday)
        delta_days = (birthday_this_year - datetime.today().date()).days
        birthday_weekday = get_weekday(birthday_this_year)
        
        if delta_days < days_in_week:
            if birthday_weekday in ['Saturday', 'Sunday']:
                birthday_weekday = 'Monday'
            
            birthdays_per_week[birthday_weekday].append(name)
    
    for day, names in birthdays_per_week.items():
        print(f"{day}: {', '.join(names)}")

# Example usage:
users = [
    {"name": "Bill Gates", "birthday": datetime(1955, 3, 11)},
    {"name": "Jan Koum", "birthday": datetime(1976, 3, 13)},
    {"name": "Kim Kardashian", "birthday": datetime(1980, 3, 15)},
    {"name": "Jill Valentine", "birthday": datetime(1974, 3, 17)},
]

get_birthdays_per_week(users)