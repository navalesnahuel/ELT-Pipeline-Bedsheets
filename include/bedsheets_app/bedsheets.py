import os
import sys
configs_parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(configs_parent_dir)
from data_ingestion_functions.create_data import *
from data_ingestion_functions.ingestion_data import *
from dummy_data_functions.dummy_data_ingestion import *

def main():
    while True:
        clear_screen()
        print("¡Bienvenido al Sistema de Gestión!")
        print("1. Agregar un nuevo cliente")
        print("2. Realizar un nuevo pedido")
        print("3. Salir")
        print("[Dummies] Para popular ordenes/productos con dummy-data")
        print("[Formatear] Para crear/formatear tablas")

        choice = input("Por favor, seleccione una opción (1-3): ").capitalize()
        
        if choice == "Formatear":
            formating()
        elif choice == "Dummies":
            dummy_populate_tables()
        elif choice == "1":
            manually_populate_customers()
        elif choice == "2":
            manually_populate_orders()
        elif choice == "3":
            break
        else:
            continue

if __name__ == "__main__":
    main()
