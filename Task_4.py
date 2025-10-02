import csv
import os
from colorama import init, Fore, Back, Style
from Helpers.cmd_pryttyfy import msg_welcome, animated_line, msg_good_bye
from Helpers.normalize_phone import normalize_phone

CSV_FILE = "./goit-algo-hw-04/DB_files/contacts.csv"

def ensure_storage():
    folder = os.path.dirname(CSV_FILE)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "phone"])

def load_contacts():
    ensure_storage()
    contacts = {}
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("name") or "").strip()
            phone = (row.get("phone") or "").strip()
            if name and phone:
                contacts[name.casefold()] = phone
    return contacts

def save_contacts(contacts):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "phone"])
        for name_lower, phone in sorted(contacts.items()):
            writer.writerow([name_lower.title(), phone])

def normalize_phone_raw(raw_phone):
    try:
        p = normalize_phone(raw_phone)
        return (p or "").strip()
    except Exception:
        return raw_phone.strip()

def parse_name_phone(args):
    if len(args) < 2:
        return None, None
    phone_raw = args[-1].strip()
    name = " ".join(args[:-1]).strip()
    if not name or not phone_raw:
        return None, None
    return name, phone_raw

def handle_add(contacts, args):
    name, phone_raw = parse_name_phone(args)
    if not name:
        return f"{Fore.YELLOW}Usage: add <name> <phone>{Style.RESET_ALL}"
    phone = normalize_phone_raw(phone_raw)
    if not phone:
        return f"{Fore.YELLOW}Invalid phone number.{Style.RESET_ALL}"
    key = name.casefold()
    contacts[key] = phone
    save_contacts(contacts)
    return f"{Fore.GREEN}Contact '{name.title()}' added/updated successfully.{Style.RESET_ALL}"

def handle_change(contacts, args):
    name, phone_raw = parse_name_phone(args)
    if not name:
        return f"{Fore.YELLOW}Usage: change <name> <phone>{Style.RESET_ALL}"
    phone = normalize_phone_raw(phone_raw)
    if not phone:
        return f"{Fore.YELLOW}Invalid phone number.{Style.RESET_ALL}"
    key = name.casefold()
    if key in contacts:
        contacts[key] = phone
        save_contacts(contacts)
        return f"{Fore.GREEN}Phone updated for '{name.title()}'.{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}Contact '{name.title()}' not found.{Style.RESET_ALL}"

def handle_phone(contacts, args):
    if not args:
        return f"{Fore.YELLOW}Usage: phone <name>{Style.RESET_ALL}"
    name = " ".join(args).strip()
    key = name.casefold()
    phone = contacts.get(key)
    if phone:
        return f"{Fore.GREEN}{name.title()}: {phone}{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}Contact '{name.title()}' not found.{Style.RESET_ALL}"

def handle_all(contacts):
    if not contacts:
        return f"{Fore.YELLOW}No contacts yet.{Style.RESET_ALL}"
    lines = [f"{Style.BRIGHT}{Fore.WHITE}{Back.BLUE}Contacts:{Style.RESET_ALL}"]
    for name_lower, phone in sorted(contacts.items()):
        lines.append(f"{Fore.CYAN}  {name_lower.title()}: {phone}{Style.RESET_ALL}")
    return "\n".join(lines)

def handle_help():
    help_lines = [
        "Available commands:",
        "  hello                  - Greet the assistant.",
        "  add <name> <phone>     - Add a new contact.",
        "  change <name> <phone>  - Update contact phone.",
        "  phone <name>           - Show phone by name.",
        "  all                    - Show all contacts.",
        "  help                   - Show this help.",
        "  exit | close           - Exit the assistant.",
    ]
    lines = []
    for line in help_lines:
        if not line.startswith("  "):
            lines.append(f"{Style.BRIGHT}{Fore.WHITE}{Back.BLUE}{line}{Style.RESET_ALL}")
        else:
            lines.append(f"{Fore.CYAN}{line}{Style.RESET_ALL}")
    return "\n".join(lines)

def handle_hello():
    return f"{Fore.CYAN}Hi! How can I help you?{Style.RESET_ALL}"

def main():
    init(autoreset=True)
    animated_line(msg_welcome)
    print()
    contacts = load_contacts()
    print(handle_help())

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
            print(handle_help())
        elif cmd == "hello":
            print(handle_hello())
        elif cmd == "add":
            print(handle_add(contacts, args))
        elif cmd == "change":
            print(handle_change(contacts, args))
        elif cmd == "phone":
            print(handle_phone(contacts, args))
        elif cmd == "all":
            contacts = load_contacts()
            print(handle_all(contacts))
            #print(f"{Fore.YELLOW}{contacts}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Invalid command. Type 'help' to see available commands.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
