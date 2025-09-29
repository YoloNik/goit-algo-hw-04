from Helpers.cmd_pryttyfy import msg_welcome, animated_line
from Helpers.normalize_phone import normalize_phone


import csv
import os
from colorama import init, Fore, Back, Style

init(autoreset=True)  # auto reset colors after each print

CSV_FILE = "DB_files/contacts.csv"

def print_title(text):
    print(f"{Style.BRIGHT}{Fore.WHITE}{Back.BLUE}{text}{Style.RESET_ALL}")

def print_info(text):
    print(f"{Fore.CYAN}{text}{Style.RESET_ALL}")

def print_ok(text):
    print(f"{Style.BRIGHT}{Fore.GREEN}{text}{Style.RESET_ALL}")

def print_warn(text):
    print(f"{Style.BRIGHT}{Fore.YELLOW}{text}{Style.RESET_ALL}")

def print_error(text):
    print(f"{Style.BRIGHT}{Fore.WHITE}{Back.RED}{text}{Style.RESET_ALL}")

def ensure_csv():
    # Create csv with header if not exists
    if not os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["name", "phone"])
        except Exception as e:
            print_error(f"Failed to create CSV: {e}")

def load_contacts():
    # Load contacts from CSV into dict; ignore duplicates after the first
    ensure_csv()
    contacts = {}
    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = (row.get("name") or "").strip()
                phone = (row.get("phone") or "").strip()
                if name and name not in contacts:
                    contacts[name] = phone
                elif name in contacts:
                    print_warn(f"Duplicate in CSV ignored: {name}")
    except Exception as e:
        print_error(f"Failed to read CSV: {e}")
    return contacts

def save_contacts(contacts):
    # Overwrite CSV with current contacts
    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "phone"])
            for name, phone in sorted(contacts.items()):
                writer.writerow([name, phone])
        return True
    except Exception as e:
        print_error(f"Failed to save CSV: {e}")
        return False

def show_help():
    print_title("Available commands:")
    print_info("  hello                    - Greet the assistant.")
    print_info("  add <name> <phone>       - Add a new contact.")
    print_info("  change <name> <phone>    - Update phone for existing contact.")
    print_info("  phone <name>             - Show phone by name.")
    print_info("  all                      - List all contacts.")
    print_info("  help                     - Show this help.")
    print_info("  exit | close             - Exit the assistant.")

def add_contact(args, contacts):
    # add <name> <phone>
    if len(args) != 2:
        print_warn("Invalid arguments. Usage: add <name> <phone>")
        return
    name = args[0].title()
    phone = normalize_phone(args[1])

    if name in contacts:
        # Ask user to overwrite or create new name
        print_warn(f"Contact '{name}' already exists with phone: {contacts[name]}")
        ans = input(f"{Style.BRIGHT}{Fore.MAGENTA}Replace it with {phone}? [y/N]: {Style.RESET_ALL}").strip().lower()
        if ans == "y" or ans == "yes":
            contacts[name] = phone
            if save_contacts(contacts):
                print_ok("Contact updated and saved.")
            return
        else:
            # Ask for a new unique name
            while True:
                new_name = input(f"{Style.BRIGHT}{Fore.MAGENTA}Enter a new unique name (or press Enter to cancel): {Style.RESET_ALL}").strip()
                if new_name == "":
                    print_warn("Add cancelled.")
                    return
                if new_name in contacts:
                    print_warn(f"'{new_name}' already exists. Try again.")
                else:
                    contacts[new_name] = phone
                    if save_contacts(contacts):
                        print_ok(f"Contact added as '{new_name}' and saved.")
                    return
    else:
        contacts[name] = phone
        if save_contacts(contacts):
            print_ok("Contact added and saved.")

def change_contact(args, contacts):
    # change <name> <phone>
    if len(args) != 2:
        print_warn("Invalid arguments. Usage: change <name> <phone>")
        return
    name, phone = args[0], normalize_phone(args[1])
    if name not in contacts:
        print_error("Contact not found.")
        return
    contacts[name] = phone
    if save_contacts(contacts):
        print_ok("Contact updated and saved.")

def show_phone(args, contacts):
    # phone <name>
    if len(args) != 1:
        print_warn("Invalid arguments. Usage: phone <name>")
        return
    name = args[0]
    if name not in contacts:
        print_error("Contact not found.")
        return
    print_ok(f"{name}: {contacts[name]}")

def show_all(contacts):
    # all
    if not contacts:
        print_warn("No contacts yet.")
        return
    print_title("Contacts:")
    for name, phone in sorted(contacts.items()):
        print_info(f"  {name}: {phone}")

def main():
    # Main loop with CSV persistence and simple command parsing
    animated_line(msg_welcome)
    contacts = load_contacts()
    show_help()
    print()

    while True:
        raw = input(f"{Style.BRIGHT}{Fore.MAGENTA}Enter a command:{Style.RESET_ALL} ").strip()
        if not raw:
            print_warn("Invalid command. Type 'help' to see available commands.")
            continue

        parts = raw.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "exit" or cmd == "close":
            print_title("Good bye!")
            break
        elif cmd == "hello":
            print_info("How can I help you?")
        elif cmd == "help":
            show_help()
        elif cmd == "add":
            add_contact(args, contacts)
        elif cmd == "change":
            change_contact(args, contacts)
        elif cmd == "phone":
            show_phone(args, contacts)
        elif cmd == "all":
            show_all(contacts)
        else:
            print_error("Invalid command. Type 'help' to see available commands.")

if __name__ == "__main__":
    main()
