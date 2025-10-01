from Helpers.cmd_pryttyfy import msg_welcome, animated_line, msg_good_bye
from Helpers.normalize_phone import normalize_phone
import csv
import os
from colorama import init, Fore, Back, Style

CSV_FILE = "DB_files/contacts.csv"


def ensure_storage():
    # create folder and csv file if not exists
    folder = os.path.dirname(CSV_FILE)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "phone"])


def load_contacts():
    # return contacts as {name_lower: {"name": display, "phone": phone}}
    ensure_storage()
    contacts = {}
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("name") or "").strip()
            phone = (row.get("phone") or "").strip()
            if name:
                key = name.casefold()
                # first occurrence wins (simple rule)
                if key not in contacts:
                    contacts[key] = {"name": name.title(), "phone": phone}
    return contacts


def save_contacts(contacts):
    # save all contacts to csv
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "phone"])
        for c in sorted(contacts.values(), key=lambda x: x["name"].casefold()):
            writer.writerow([c["name"], c["phone"]])


def add_contact(contacts, name, phone):
    # add or replace a contact; returns "added" or "updated"
    key = name.casefold()
    if key in contacts:
        contacts[key]["phone"] = phone
        save_contacts(contacts)
        return "updated"
    else:
        contacts[key] = {"name": name, "phone": phone}
        save_contacts(contacts)
        return "added"


def change_contact(contacts, name, phone):
    # change existing contact; returns True/False
    key = name.casefold()
    if key not in contacts:
        return False
    contacts[key]["phone"] = phone
    save_contacts(contacts)
    return True


def get_phone(contacts, name):
    # return phone or None
    key = name.casefold()
    return contacts.get(key, {}).get("phone")


def list_contacts(contacts):
    # return sorted list of tuples (name, phone)
    return sorted([(c["name"], c["phone"]) for c in contacts.values()],
                  key=lambda x: x[0].casefold())


def parse_name_phone(args):
    # last token is phone, the rest is name
    if len(args) < 2:
        return None, None
    phone_raw = args[-1].strip()
    name = " ".join(args[:-1]).strip()
    if not name or not phone_raw:
        return None, None
    return name, phone_raw


def normalize_phone_safe(raw_phone):
    # try to normalize, fallback to trimmed raw
    try:
        p = normalize_phone(raw_phone)
        return (p or "").strip()
    except Exception:
        return raw_phone.strip()


def get_help_lines():
    # return help text lines
    return [
        "Available commands:",
        "  hello                    - Greet the assistant.",
        "  add <name> <phone>       - Add a new contact (name can have spaces).",
        "  change <name> <phone>    - Update contact phone.",
        "  phone <name>             - Show phone by name.",
        "  all                      - Show all contacts.",
        "  help                     - Show this help.",
        "  exit | close             - Exit the assistant.",
    ]



def main():

    init(autoreset=True)
    animated_line(msg_welcome)
    print()
    contacts = load_contacts()


    for line in get_help_lines():
        if not line.startswith("  "):
            print(f"{Style.BRIGHT}{Fore.WHITE}{Back.BLUE}{line}{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}{line}{Style.RESET_ALL}")

    while True:
        try:
            cmd_line = input(f"{Style.BRIGHT}{Fore.MAGENTA}Enter a command:{Style.RESET_ALL} ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            animated_line(msg_good_bye)
            break

        if not cmd_line:
            print(f"{Fore.YELLOW}Invalid command. Type 'help' to see available commands.{Style.RESET_ALL}")
            continue

        parts = cmd_line.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd in ("exit", "close"):
            animated_line(msg_good_bye)
            break

        elif cmd == "help":
            print(f"{Style.BRIGHT}{Fore.WHITE}{Back.BLUE}Commands:{Style.RESET_ALL}")
            for line in get_help_lines():
                if line.startswith("  "):
                    print(f"{Fore.CYAN}{line}{Style.RESET_ALL}")
                else:
                    print(f"{Style.BRIGHT}{Fore.WHITE}{Back.BLUE}{line}{Style.RESET_ALL}")

        elif cmd == "hello":
            print(f"{Fore.CYAN}Hi! How can I help you?{Style.RESET_ALL}")

        elif cmd == "add":
            if len(args) < 2:
                print(f"{Fore.YELLOW}Usage: add <name> <phone>{Style.RESET_ALL}")
                continue
            name, phone_raw = parse_name_phone(args)
            if name:
                name = name.title()
            if not name:
                print(f"{Fore.YELLOW}Usage: add <name> <phone>{Style.RESET_ALL}")
                continue
            phone = normalize_phone_safe(phone_raw)
            if not phone:
                print(f"{Fore.YELLOW}Invalid phone number.{Style.RESET_ALL}")
                continue
            result = add_contact(contacts, name, phone)
            if result == "added":
                print(f"{Fore.GREEN}Contact '{name}' added successfully.{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Contact '{name}' updated successfully.{Style.RESET_ALL}")

        elif cmd == "change":
            if len(args) < 2:
                print(f"{Fore.YELLOW}Usage: change <name> <phone>{Style.RESET_ALL}")
                continue
            name, phone_raw = parse_name_phone(args)
            if name:
                name = name.title()
            if not name:
                print(f"{Fore.YELLOW}Usage: change <name> <phone>{Style.RESET_ALL}")
                continue
            phone = normalize_phone_safe(phone_raw)
            if not phone:
                print(f"{Fore.YELLOW}Invalid phone number.{Style.RESET_ALL}")
                continue
            ok = change_contact(contacts, name, phone)
            if ok:
                print(f"{Fore.GREEN}Phone updated for '{name}'.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Contact '{name}' not found.{Style.RESET_ALL}")

        elif cmd == "phone":
            if not args:
                print(f"{Fore.YELLOW}Usage: phone <name>{Style.RESET_ALL}")
                continue
            name = " ".join(args).strip()
            phone = get_phone(contacts, name)
            if phone:
                print(f"{Fore.GREEN}{name}: {phone}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Contact '{name}' not found.{Style.RESET_ALL}")

        elif cmd == "all":
            data = list_contacts(contacts)
            if not data:
                print(f"{Fore.YELLOW}No contacts yet.{Style.RESET_ALL}")
            else:
                print(f"{Style.BRIGHT}{Fore.WHITE}{Back.BLUE}Contacts:{Style.RESET_ALL}")
                for n, p in data:
                    print(f"{Fore.CYAN}  {n}: {p}{Style.RESET_ALL}")

        else:
            print(f"{Fore.RED}Invalid command. Type 'help' to see available commands.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
