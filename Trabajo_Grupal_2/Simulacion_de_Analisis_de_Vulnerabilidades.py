import os
import time
import pyfiglet
from simple_term_menu import TerminalMenu


# base de datos de software con vulnerabilidades
software_db = {
    'ivsftpd': {
        'software_name' : 'vsftpd',
        'software_version': '2.3.4',
        'vulnerabilidades': ['CVE-2011-0762']['CVE-2015-1419'],
        'mitigacion': "Actualizar vsftpd:\n Asegúrate de estar utilizando la última versión estable de vsftpd, ya que las vulnerabilidades a menudo se corrigen en las actualizaciones."
    },  
    'iapache': {
        'software_name' : 'apache',
        'software_version': '2.4.29',
        'vulnerabilidades': ['CVE-2019-0211', 'CVE-2017-7679'],
        'mitigacion': "Actualizar Apache:\n Mantén Apache actualizado para beneficiarte de las correcciones de seguridad.\n Seguridad en Configuración:\n Configura Apache de manera segura, deshabilita módulos no utilizados y limita el acceso a recursos sensibles.\n Firewalls y WAFs:\n Utiliza firewalls y Web Application Firewalls (WAFs) para filtrar y monitorizar el tráfico entrante."
    },
    'issh': {
        'software_name' : 'ssh',
        'software_version': '7.6.1',
        'vulnerabilidades': ['CVE-2018-15473', 'CVE-2016-0777'],
        'mitigacion': "Actualizar OpenSSH:\n Mantén la versión de OpenSSH actualizada para corregir vulnerabilidades conocidas.\n Configuración Segura:\n Ajusta la configuración de SSH para limitar accesos, desactivar métodos de autenticación débiles y usar configuraciones criptográficas fuertes.\n Monitorización de Acceso:\n Implementa sistemas de monitoreo para detectar y responder a actividades sospechosas en conexiones SSH."
    }
}


def verificar_vulnerabilidad(name, version):
        for key, value in software_db.items():
         if value['software_name'] == name and value['software_version'] == version:
             return value['mitigacion'], value['vulnerabilidades']
        return "No se encontró información para ese software o versión en la base de datos."
  


    
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
        if main_menu_entry_index == 0:
            software_data = {}
            name = input("enter software name: ")
            version = input ("enter software version: ")
            software_data['nombre'] = name
            software_data['version'] = version
            print(software_data)
            time.sleep(2)
        elif main_menu_entry_index == 1:
            print("Finding information about", (name, version), "...")
            time.sleep(3)
            resultado = verificar_vulnerabilidad(name, version)
            print("\033[1mSe encontraron las siguientes vulnerabilidades:\033[0m", resultado[1], "\n\033[1mMitigar vulnerabilidades:\n\033[0m", resultado[0])
            input("Press enter to continue...")
        elif main_menu_entry_index == 2:
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