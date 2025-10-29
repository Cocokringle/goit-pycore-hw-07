from contact_bot_module import AddressBook, Record
from error_handlers import input_error

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if(record):
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        return f"Contact name {name} does not exist"

@input_error    
def show_phone(args,book: AddressBook):
    name = args[0]
    record = book.find(name)
    if(record):
        return str(record)
    else:
        return f"Contact name {name} does not exist"

@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "Address book is empty."
    return '\n'.join(str(record) for record in book.data.values())  

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if(record):
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        return f"Contact name {name} does not exist"


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if(record):
        if record.birthday:
            return f"{name}'s birthday: {str(record.birthday)}"
        else:
            return f"Birthday for contact name {name} is not set."
    else:
        return f"Contact name {name} does not exist"

@input_error
def birthdays(book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays in the next week"
    
    result = "Upcoming birthdays:\n"
    for bday_info in upcoming:
        result += f"{bday_info['name']}: {bday_info['congratulation_date']}\n"
    return result.strip()




# add [ім'я] [телефон]: Додати або новий контакт з іменем та телефонним номером, або телефонний номер к контакту який вже існує.
# change [ім'я] [старий телефон] [новий телефон]: Змінити телефонний номер для вказаного контакту.
# phone [ім'я]: Показати телефонні номери для вказаного контакту.
# all: Показати всі контакти в адресній книзі.
# add-birthday [ім'я] [дата народження]: Додати дату народження для вказаного контакту.
# show-birthday [ім'я]: Показати дату народження для вказаного контакту.
# birthdays: Показати дні народження, які відбудуться протягом наступного тижня.
# hello: Отримати вітання від бота.
# close або exit: Закрити програму.