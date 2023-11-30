import os
import time
import pyfiglet
from simple_term_menu import TerminalMenu



def main_menu():
    """
    Function that displays the program's main menu.
    Args:
    None
    Returns:
    None
    """
    while True:
        os.system("clear")
        print(pyfiglet.figlet_format("Menu", font="big", justify="center"))
        options = ["[1] Enter software data ", "[2] Exit"]
        main_menu = TerminalMenu(options)
        main_menu_entry_index = main_menu.show()
        if main_menu_entry_index == 0:
            software_data = {}
            name = input("enter software name: ")
            version = float(input ("enter software version: "))
            software_data['nombre'] = name
            software_data['version'] = version
            print(software_data)
            time.sleep(5)
        elif main_menu_entry_index == 1:
            print(software_data)
            time.sleep(5)
            return

def main():
    """
    Main function of the program.
    Args:
    None
    Returns:
    None
    """
    os.system("clear")
    print(pyfiglet.figlet_format("Euneiz", font="big", justify="center"))
    time.sleep(0.5)
    os.system("clear")
    print(pyfiglet.figlet_format("Project:\nLogs analytics", font="big", justify="center", width=100))
    time.sleep(0.5)
    main_menu()

if __name__ == "__main__":
    main()