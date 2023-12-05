import os  # Operating system interface for clearing the terminal
import time  # Time-related functions for introducing delays
import pyfiglet  # ASCII art text generator for creating stylized banners
from simple_term_menu import TerminalMenu  # Terminal-based menu library for user interaction

# We declare the variable outside the loops to use it throughout the program
software_data = {}
# Database of software with vulnerabilities
software_db = {
    'ivsftpd': {
        'software_name' : 'vsftpd',
        'software_version': '2.3.4',
        'vulnerabilidades': ['CVE-2011-0762', 'CVE-2015-1419'],
        'mitigacion': "Update vsftpd:\n Ensure you are using the latest stable version of vsftpd, as vulnerabilities are often addressed in updates."
    },  
    'iapache': {
        'software_name' : 'apache',
        'software_version': '2.4.29',
        'vulnerabilidades': ['CVE-2019-0211', 'CVE-2017-7679'],
        'mitigacion': "Update Apache:\n Keep Apache up to date to benefit from security fixes.\n Configuration Security:\n Configure Apache securely by disabling unused modules and limiting access to sensitive resources.\n Firewalls and WAFs:\n Use firewalls and Web Application Firewalls (WAFs) to filter and monitor incoming traffic."
    },
    'issh': {
        'software_name' : 'ssh',
        'software_version': '7.6.1',
        'vulnerabilidades': ['CVE-2018-15473', 'CVE-2016-0777'],
        'mitigacion': "Update OpenSSH:\n Keep the OpenSSH version up to date to address known vulnerabilities.\n Secure Configuration:\n Adjust SSH configuration to limit access, disable weak authentication methods, and use strong cryptographic settings.\n Access Monitoring:\n Implement monitoring systems to detect and respond to suspicious activities in SSH connections."
    }
}

# Function to check vulnerabilities based on software name and version
def verificar_vulnerabilidad(name, version):
        for key, value in software_db.items():
         if value['software_name'] == name and value['software_version'] == version:
             return value['mitigacion'], value['vulnerabilidades']
        return "No se encontró información para ese software o versión en la base de datos."
  


# Main menu function    
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
        options = ["[1] Enter software data ", "[2] Mitigate vulnerability", "[3] Exit"]
        main_menu = TerminalMenu(options)
        main_menu_entry_index = main_menu.show()
        # Option to enter software data
        if main_menu_entry_index == 0:
            name = input("enter software name: ")
            version = input ("enter software version: ")
            software_data['nombre'] = name
            software_data['version'] = version
            print(software_data)
            time.sleep(2)
        # Option to mitigate vulnerability
        elif main_menu_entry_index == 1:
            if software_data:
                print("Searching information for", (name, version), "...")
                time.sleep(3)
                resultado = verificar_vulnerabilidad(name, version)
                print("\033[1mThe following vulnerabilities were found:\033[0m", resultado[1], "\n\033[1mMitigate vulnerabilities:\n\033[0m", resultado[0])
                input("Press enter to continue...")
            else:
                print("Please enter software information")
                time.sleep(3)
        # Option to exit
        elif main_menu_entry_index == 2:
            return
# Main function
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