"""
Log Analytics
"""

import os
import re
import time
from datetime import datetime, timedelta
import pyfiglet
from simple_term_menu import TerminalMenu

# Function to detect brute force attacks in Apache logs
def detect_apache_bruteforce(logfile):
    # Initialization of variables
    failed_attempts = {}
    alert_threshold = 10
    time_window = 5
    ip_alerted = set()
    brute_force_details = []
    
    # Open the Apache log file and iterate through each line
    with open(logfile, "r", encoding="UTF-8") as log:
        for line in log:
            # Check for login attempts and failed status in Apache logs
            if "GET /login.html" in line and " 401 " in line:
                # Split the log line and extract necessary information
                parts = line.split()
                timestamp = parts[3] + " " + parts[4]
                log_time = datetime.strptime(timestamp, "[%d/%b/%Y:%H:%M:%S +%f]")
                ip = parts[0]
                # Check for previous failed attempts from the same IP
                if ip in failed_attempts:
                    # Check the time window for consecutive attempts
                    if (log_time - failed_attempts[ip][-1]) <= timedelta(minutes=time_window):
                        # Update the failed attempts and trigger alerts if threshold reached
                        failed_attempts[ip].append(log_time)
                        if len(failed_attempts[ip]) >= alert_threshold and ip not in ip_alerted:
                            ip_alerted.add(ip)
                            brute_force_details.append(ip)
                    else:
                        failed_attempts[ip] = [log_time]
                else:
                    failed_attempts[ip] = [log_time]
    return brute_force_details

# Function to detect brute force attacks in SSH logs
def detect_bruteforce_ssh(logfile):
    # Similar structure as the previous function with adjustments for SSH logs
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

# Function to interact with the user and display the menu for detection
def detect_brute_force_menu():
    while True:
        # Display the submenu options for different logs
        os.system("clear")
        print(pyfiglet.figlet_format("Detect Brute Force", font="big", justify="center"))
        options = ["[1] SSH", "[2] Apache", "[3] Create Report", "[4] Back to Main Menu"]
        submenu = TerminalMenu(options)
        submenu_entry_index = submenu.show()
        if submenu_entry_index == 0:
            # Detection for SSH brute force attacks
            # Adjust the path to your SSH log file according to your system
            logfile = "/workspaces/EjercicioGrupal2/Trabajo_Grupal_2/Procesamiento de Logs Básico/auth.log"
            print("Detecting Brute Force for SSH...")
            brute_force_details = detect_bruteforce_ssh(logfile)
            # Display detected brute force attempts
            if brute_force_details:
                for ip, user in brute_force_details:
                    print(f"Alert: Brute Force Detected in SSH from IP: {ip}, User: {user}")
            else:
                print("No Brute Force Detected")
            input("Press Enter to continue...")
        # Similar logic for Apache detection
        elif submenu_entry_index == 1:
            logfile = "/workspaces/EjercicioGrupal2/Trabajo_Grupal_2/Procesamiento de Logs Básico/access.log"
            print("Detecting Brute Force for Apache...")
            brute_force_details = detect_apache_bruteforce(logfile)
            if brute_force_details:
                for ip in brute_force_details:
                    print(f"Alert: Brute Force Detected in Apache from IP: {ip}")
            else:
                print("No Brute Force Detected")
            input("Press Enter to continue...")
        # Option to create a report
        elif submenu_entry_index == 2:
            with open("informe.txt", "w") as file:
                file.write("Informe de Detección de Ataques de Fuerza Bruta\n\n")
                
                # Detección de ataques de fuerza bruta en SSH
                logfile_ssh = "/workspaces/EjercicioGrupal2/Trabajo_Grupal_2/Procesamiento de Logs Básico/auth.log"
                brute_force_details_ssh = detect_bruteforce_ssh(logfile_ssh)
                file.write("Ataques de Fuerza Bruta en SSH:\n")
                if brute_force_details_ssh:
                    for ip, user in brute_force_details_ssh:
                        file.write(f"Alerta: Ataque de Fuerza Bruta Detectado en SSH desde la IP: {ip}, Usuario: {user}\n")
                else:
                    file.write("No se detectaron ataques de fuerza bruta en SSH.\n")
                
                file.write("\n")
                
                # Detección de ataques de fuerza bruta en Apache
                logfile_apache = "/workspaces/EjercicioGrupal2/Trabajo_Grupal_2/Procesamiento de Logs Básico/access.log"
                brute_force_details_apache = detect_apache_bruteforce(logfile_apache)
                file.write("Ataques de Fuerza Bruta en Apache:\n")
                if brute_force_details_apache:
                    for ip in brute_force_details_apache:
                        file.write(f"Alerta: Ataque de Fuerza Bruta Detectado en Apache desde la IP: {ip}\n")
                else:
                    file.write("No se detectaron ataques de fuerza bruta en Apache.\n")
                
                print("Archivo 'informe.txt' creado con éxito")
            input("Presiona Enter para continuar...")

        # Return to the main menu
        elif submenu_entry_index == 3:
            break

# Function to display the main menu of the program
def main_menu():
    while True:
        os.system("clear")
        print(pyfiglet.figlet_format("Menu", font="big", justify="center"))
        options = ["[1] Detect Brute Force", "[2] Exit"]
        main_menu = TerminalMenu(options)
        main_menu_entry_index = main_menu.show()
        # Option to detect brute force attacks
        if main_menu_entry_index == 0:
            detect_brute_force_menu()
        # Option to exit the program
        elif main_menu_entry_index == 1:
            return

# Main function to start the program
def main():
    os.system("clear")
    print(pyfiglet.figlet_format("Euneiz", font="big", justify="center"))
    time.sleep(0.5)
    os.system("clear")
    print(pyfiglet.figlet_format("Project:\nLogs analytics", font="big", justify="center", width=100))
    time.sleep(0.5)
    main_menu()

# Execute the main function when the script is run directly
if __name__ == "__main__":
    main()
