"""
Log Analytics
"""

import os
import re
import time
from datetime import datetime, timedelta
import pyfiglet
from simple_term_menu import TerminalMenu

def detect_apache_bruteforce(logfile):
    """
    Function to detect brute force attacks in Apache logs.
    Args:
    logfile (str): The path to the Apache log file.
    Returns:
    list: A list of IP addresses that have been detected as brute force attackers.
    """
    failed_attempts = {}
    alert_threshold = 10
    time_window = 5
    ip_alerted = set()
    brute_force_details = []
    with open(logfile, "r", encoding="UTF-8") as log:
        for line in log:
            if "GET /login.html" in line and " 401 " in line:
                parts = line.split()
                timestamp = parts[3] + " " + parts[4]
                log_time = datetime.strptime(timestamp, "[%d/%b/%Y:%H:%M:%S +%f]")
                ip = parts[0]
                if ip in failed_attempts:
                    if (log_time - failed_attempts[ip][-1]) <= timedelta(minutes=time_window):
                        failed_attempts[ip].append(log_time)
                        if len(failed_attempts[ip]) >= alert_threshold and ip not in ip_alerted:
                            ip_alerted.add(ip)
                            brute_force_details.append(ip)
                    else:
                        failed_attempts[ip] = [log_time]
                else:
                    failed_attempts[ip] = [log_time]
    return brute_force_details

def detect_bruteforce_ssh(logfile):
    """
    Function to detect brute force attacks in SSH logs.
    Args:
    logfile (str): The path to the SSH log file.
    Returns:
    list: A list of tuples containing the IP address and the user that have been detected as brute force attackers.
    """
    failed_attempts = {}
    alert_threshold = 10
    time_window = 5
    ip_alerted = set()
    brute_force_details = []
    with open(logfile, "r", encoding="UTF-8") as log:
        for line in log:
            if "sshd" in line and "Failed password" in line:
                parts = line.split()
                timestamp = parts[0] + " " + parts[1] + " " + parts[2]
                log_time = datetime.strptime(timestamp, "%b %d %H:%M:%S")
                ip = re.search(r'\d+\.\d+\.\d+\.\d+', line)
                if ip:
                    ip = ip.group()
                else:
                    continue
                user = None
                user_match = re.search(r'for (\w+) from', line)
                if user_match:
                    user = user_match.group(1)
                if ip in failed_attempts:
                    if (log_time - failed_attempts[ip][-1]) <= timedelta(minutes=time_window):
                        failed_attempts[ip].append(log_time)
                        if len(failed_attempts[ip]) >= alert_threshold and ip not in ip_alerted:
                            ip_alerted.add(ip)
                            brute_force_details.append((ip, user))
                    else:
                        failed_attempts[ip] = [log_time]
                else:
                    failed_attempts[ip] = [log_time]
    return brute_force_details 

def detect_brute_force_menu():
    """
    Function that displays the submenu to detect brute force attacks.
    Args:
    None
    Returns:
    None
    """
    while True:
        os.system("clear")
        print(pyfiglet.figlet_format("Detect Brute Force", font="big", justify="center"))
        options = ["[1] SSH", "[2] Apache", "[3] Back to Main Menu"]
        submenu = TerminalMenu(options)
        submenu_entry_index = submenu.show()
        if submenu_entry_index == 0:
            logfile = "/workspaces/Euneiz_Introduction-to-Programming/Analisis de logs/auth.log"  # Ruta al archivo de registro de SSH, ajusta según tu sistema
            print("Detecting Brute Force for SSH...")
            brute_force_details = detect_bruteforce_ssh(logfile)
            if brute_force_details:
                for ip, user in brute_force_details:
                    print(f"Alert: Brute Force Detected in SSH from IP: {ip}, User: {user}")
            else:
                print("No Brute Force Detected")
            input("Press Enter to continue...")
        elif submenu_entry_index == 1:
            logfile = "/workspaces/Euneiz_Introduction-to-Programming/Analisis de logs/access.log"  # Ruta al archivo de registro de Apache, ajusta según tu sistema
            print("Detecting Brute Force for Apache...")
            brute_force_details = detect_apache_bruteforce(logfile)
            if brute_force_details:
                for ip in brute_force_details:
                    print(f"Alert: Brute Force Detected in Apache from IP: {ip}")
            else:
                print("No Brute Force Detected")
            input("Press Enter to continue...")
        elif submenu_entry_index == 2:
            break

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
        options = ["[1] Detect Brute Force", "[2] Exit"]
        main_menu = TerminalMenu(options)
        main_menu_entry_index = main_menu.show()
        if main_menu_entry_index == 0:
            detect_brute_force_menu()
        elif main_menu_entry_index == 1:
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
