from typing import List, Tuple, Dict, Optional


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    cmd, *args = user_input.split()
    return cmd.strip().lower(), args


def input_error(func):
    def inner(args: List[str], contacts: Dict[str, str]):
        try:
            return func(args, contacts)
        except (ValueError, IndexError):
            return "Enter the argument for the command"

    return inner


def contact_exists(expected: bool):
    def decorator(func):
        def inner(args: List[str], contacts: Dict[str, str]):
            name = args[0]
            exists = name in contacts
            if expected and not exists:
                return "Contact not found."
            if not expected and exists:
                return "Contact already exists."
            return func(args, contacts)

        return inner

    return decorator


@input_error
@contact_exists(False)
def add_contact(args: List[str], contacts: Dict[str, str]) -> str:
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
@contact_exists(True)
def change_contact(args: List[str], contacts: Dict[str, str]) -> str:
    name, phone = args
    contacts[name] = phone
    return "Contact changed."


@input_error
@contact_exists(True)
def show_phone(args: List[str], contacts: Dict[str, str]) -> str:
    name = args[0]
    return contacts[name]


@input_error
@contact_exists(True)
def delete_contact(args: List[str], contacts: Dict[str, str]) -> str:
    name = args[0]
    del contacts[name]
    return "Contact removed."


def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Goodbye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command in ["phone", "show"]:
            print(show_phone(args, contacts))
        elif command in ["delete", "remove"]:
            print(delete_contact(args, contacts))
        elif command == "all":
            print(contacts)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
