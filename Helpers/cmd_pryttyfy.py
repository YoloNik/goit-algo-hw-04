# helpers_cmd_prettyfy_student.py
# simple student version

from colorama import init, Fore, Style
import sys
import time

# just a cool welcome message
msg_welcome = '''
 __      __   _                    _         _   _                     _    _            _     _         _   _ 
 ╲ ╲    ╱ ╱__│ │__ ___ _ __  ___  │ │_ ___  │ │_│ │_  ___   __ _ _____(_)__│ │_ __ _ _ _│ │_  │ │__  ___│ │_│ │
  ╲ ╲╱╲╱ ╱ ─_) ╱ _╱ _ ╲ '  ╲╱ ─_) │  _╱ _ ╲ │  _│ ' ╲╱ ─_) ╱ _` (_─<_─< (_─<  _╱ _` │ ' ╲  _│ │ '_ ╲╱ _ ╲  _│_│
   ╲_╱╲_╱╲___│_╲__╲___╱_│_│_╲___│  ╲__╲___╱  ╲__│_││_╲___│ ╲__,_╱__╱__╱_╱__╱╲__╲__,_│_││_╲__│ │_.__╱╲___╱╲__(_)
                                                                                                               '''

# init colorama to make colors work in Windows too
init(autoreset=True)

# color styles
STYLE = {
    "title":    f"{Style.BRIGHT}{Fore.CYAN}",
    "subtitle": f"{Style.BRIGHT}{Fore.BLUE}",
    "success":  f"{Style.NORMAL}{Fore.GREEN}",
    "warn":     f"{Style.BRIGHT}{Fore.YELLOW}",
    "error":    f"{Style.BRIGHT}{Fore.RED}",
    "info":     f"{Style.NORMAL}{Fore.CYAN}",
    "prompt":   f"{Style.BRIGHT}{Fore.MAGENTA}",
    "ok":       f"{Style.BRIGHT}{Fore.GREEN}",
}

# print text slowly, like typing animation
def animated_line(text, style_key="title", delay=0.005):
    color = STYLE.get(style_key, "")
    sys.stdout.write(color)
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(Style.RESET_ALL + "\n")

# return text with color (not print)
def colorize(text, style_key):
    color = STYLE.get(style_key, "")
    return f"{color}{text}{Style.RESET_ALL}"

# just print text with color
def print_styled(text, style_key="info", end="\n"):
    print(colorize(text, style_key), end=end)
