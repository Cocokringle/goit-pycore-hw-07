def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            if "Invalid" in str(e):
                return str(e)
            return "Not enough arguments. Please check command format."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Please provide a name."
        except TypeError:
            return "Invalid number of arguments for command."
    return inner