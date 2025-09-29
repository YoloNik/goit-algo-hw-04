import sys
from pathlib import Path
from colorama import init, Fore, Style

def print_dir_tree(path: Path, indent: str = ""):
    for item in path.iterdir():
        if item.is_dir():
            print(f"{indent}{Fore.BLUE}{item.name}{Style.RESET_ALL}")
            print_dir_tree(item, indent + "    ")
        else:
            print(f"{indent}{Fore.GREEN}{item.name}{Style.RESET_ALL}")

def main():
    init(autoreset=True)
    if len(sys.argv) < 2:
        
        print("Usage: python hw03.py <directory_path>")
        sys.exit(1)
    dir_path = Path(sys.argv[1])
    if not dir_path.exists():
        print(f"Error: Path '{dir_path}' does not exist.")
        sys.exit(1)
    if not dir_path.is_dir():
        print(f"Error: Path '{dir_path}' is not a directory.")
        sys.exit(1)
    print_dir_tree(dir_path)

if __name__ == "__main__":
    main()