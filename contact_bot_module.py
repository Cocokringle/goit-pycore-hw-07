from collections import UserDict
from datetime import datetime, date, timedelta

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
              raise ValueError('Invalid phone number: must be 10 digits')
         super().__init__(value)
         
         
class Birthday(Field):
    def __init__(self, value):
         try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(parsed_date)
         except ValueError:
             raise ValueError("Invalid date format. Use DD.MM.YYYY")
         
    def __str__(self):
         return self.value.strftime("%d.%m.%Y")  


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def find_phone(self, phone_number):
         for phone in self.phones:
              if phone.value == phone_number:
                   return phone
         return None
              
    def remove_phone(self, phone_number):
         phone_to_remove = self.find_phone(phone_number)
         if phone_to_remove:
              self.phones.remove(phone_to_remove)
         else:
              raise ValueError('Phone number dose not exist')

    def edit_phone(self, old_phone_number, new_phone_number):
         phone_to_edit = self.find_phone(old_phone_number)
         if phone_to_edit:
              new_phone_number = Phone(new_phone_number)
              index = self.phones.index(phone_to_edit)
              self.phones[index] = new_phone_number
         else:
              raise ValueError('Phone number dose not exist')
         
    def add_birthday(self, birthday_str):   
         self.birthday = Birthday(birthday_str)

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"
        
    

class AddressBook(UserDict):
    def add_record(self, record: Record):
         self.data[record.name.value] = record
    
    def find(self, name):
         return self.data.get(name)
    
    def delete(self,name):
         if name in self.data:
            self.data.pop(name)
         else:
              raise ValueError('This contact dose not exist')
         
    def get_upcoming_birthdays(self):
         today = date.today()
         upcoming_birthdays = []
         for record in self.data.values():
             if record.birthday:
                 birthday_date = record.birthday.value
                 try:
                     birthday_this_year = birthday_date.replace(year=today.year)
                 except ValueError:
                     birthday_this_year = birthday_date.replace(year=today.year, day=birthday_date.day - 1)

                 if birthday_this_year < today:
                     birthday_this_year = birthday_date.replace(today.year + 1)

                 delta_days = (birthday_this_year - today).days

                 if 0 <= delta_days <= 7:
                     congratulation_date = birthday_this_year
                     birthday_on_saturday = congratulation_date.weekday() == 5 
                     birthday_on_monday =  congratulation_date.weekday() == 6
     
                     if birthday_on_saturday:
                         congratulation_date += timedelta(2)
                     elif birthday_on_monday:
                         congratulation_date += timedelta(1)

                     upcoming_birthdays.append({
                         "name": record.name.value,
                         "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                     })
                         
         return upcoming_birthdays
         