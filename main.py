import requests
import json
import os
import sys
from pick import pick
from colorama import init, Fore, Back, Style
from pyfiglet import Figlet
import inquirer

init()

houses = ['bravery', 'brilliance', 'balance']
CONFIG_FILE = 'config.json'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    clear_screen()
    f = Figlet(font='slant')
    print(Fore.CYAN + f.renderText('vsfgang') + Style.RESET_ALL)
    print(Fore.MAGENTA + Style.BRIGHT + " " * 10 + "made by hax & and" + Style.RESET_ALL)
    print(Fore.MAGENTA + Style.BRIGHT + " " * 10 + "D I S C O R D   H O U S E   C H A N G E R" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 65 + Style.RESET_ALL + "\n")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(token):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({'token': token}, f)

def get_token():
    config = load_config()
    
    if 'token' in config:
        questions = [
            inquirer.Confirm('use_saved',
                            message="Found saved token. Use it?",
                            default=True),
        ]
        answers = inquirer.prompt(questions)
        if answers['use_saved']:
            return config['token']
    
    print(Fore.YELLOW + Style.BRIGHT + "\n[!] WARNING: Never share your token with anyone!" + Style.RESET_ALL)
    token = input(Fore.WHITE + "\nEnter your Discord token: " + Style.RESET_ALL).strip()
    
    if not token:
        print(Fore.RED + Style.BRIGHT + "\n[ERROR] Token cannot be empty!" + Style.RESET_ALL)
        sys.exit(1)
    
    questions = [
        inquirer.Confirm('save_token',
                        message="Save token for future use?",
                        default=False),
    ]
    answers = inquirer.prompt(questions)
    if answers['save_token']:
        save_config(token)
    
    return token

def select_house():
    questions = [
        inquirer.List('house',
                     message="Select your HypeSquad house",
                     choices=[
                         ('Bravery', 'bravery'),
                         ('Brilliance', 'brilliance'),
                         ('Balance', 'balance')
                     ],
                     carousel=True),
    ]
    answers = inquirer.prompt(questions)
    return answers['house']

def change_house(token: str, house: str) -> bool:
    try:
        response = requests.post(
            url="https://discord.com/api/v9/hypesquad/online",
            json={"house_id": houses.index(house) + 1},
            headers={
                "Authorization": token,
                "Content-Type": "application/json"
            },
            timeout=10
        )
        return response.status_code == 204
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"\n[ERROR] {str(e)}" + Style.RESET_ALL)
        return False

def display_result(success, house):
    clear_screen()
    display_banner()
    if success:
        print(Fore.GREEN + Style.BRIGHT + " " * 20 + "[✓] SUCCESS!" + Style.RESET_ALL)
        print(Fore.GREEN + f"\n  Your HypeSquad house has been changed to {house.capitalize()}!")
        print(Fore.GREEN + "  Thank you for using the HypeSquad Changer!")
    else:
        print(Fore.RED + Style.BRIGHT + " " * 20 + "[✗] FAILED!" + Style.RESET_ALL)
        print(Fore.RED + "\n  Failed to change HypeSquad house.")
        print(Fore.RED + "  Please check your token and try again.")
    
    print(Fore.YELLOW + "\n" + "=" * 65 + Style.RESET_ALL)
    input(Fore.WHITE + "\nPress Enter to exit..." + Style.RESET_ALL)

def main():
    display_banner()
    token = get_token()
    house = select_house()
    
    print(Fore.BLUE + Style.BRIGHT + f"\n[~] Switching to {house.capitalize()} house..." + Style.RESET_ALL)
    
    success = change_house(token, house)
    display_result(success, house)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + Style.BRIGHT + "\nOperation cancelled by user" + Style.RESET_ALL)
        sys.exit(0)