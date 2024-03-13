import psycopg2
import sys
import os
from Configs.postgres_connection import postgres_conn

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def search_customer_id_by_name(cursor, customer_name):
    cursor.execute("SELECT customer_id FROM Customers WHERE name = %s", (customer_name,))
    result = cursor.fetchone()
    if result:
        return result[0]  
    else:
        return None  

def product_id_search():
    clear_screen()
    conn, cursor = postgres_conn()
    materials = {1: 'Algodón', 2: 'Poliéster', 3: 'Microfibra', 4: 'Algodón y Poliéster', 5: 'Percal', 6: 'Ultra Soft'}
    product_types = {1: 'Sábanas', 2: 'Juegos de Sábanas', 3: 'Funda de Colchón'}
    sizes = {1: '1 1/2 Plaza', 2: '2 1/2 Plazas', 3: 'King', 4: 'Queen', 5: '2 Plazas', 6: '1 Plaza'}

    print("------ Especificaciones del Producto ------")

    # Selección de Categoría
    print("\nSeleccione la categoría del producto:")
    for num, product_type in product_types.items():
        print(f"{num}. {product_type}")
    while True:
        try:
            product_type_num = int(input('\u25CF Elija el número correspondiente al tipo de producto: '))
            if product_type_num in product_types:
                break
            else:
                print('\u25CF Número inválido. Por favor, elija entre las opciones proporcionadas.')
        except ValueError:
            print("\u25CF Por favor, ingrese un número válido.")
    
    category = product_types.get(product_type_num)
    clear_screen()

    # Selección de Material
    print("------ Especificaciones del Producto ------")
    print("\nSeleccione el material del producto:")
    for num, material in materials.items():
        print(f"{num}. {material}")
    while True:
        try:
            material_num = int(input('\u25CF Elija el número correspondiente al material del producto: '))
            if material_num in materials:
                break
            else:
                print('\u25CF Número inválido. Por favor, elija entre las opciones proporcionadas.')
        except ValueError:
            print("\u25CF Por favor, ingrese un número válido.")

    material = materials.get(material_num)
    clear_screen()

    # Selección de Tamaño
    print("------ Especificaciones del Producto ------")
    print("\nSeleccione el tamaño del producto:")
    for num, size in sizes.items():
        print(f"{num}. {size}")
    while True:
        try:
            size_num = int(input('\u25CF Elija el número correspondiente al tamaño del producto: '))
            if size_num in sizes:
                break
            else:
                print('\u25CF Número inválido. Por favor, elija entre las opciones proporcionadas.')
        except ValueError:
            print("\u25CFPor favor, ingrese un número válido.")

    size = sizes.get(size_num)
    clear_screen()

    # Imprimir Producto Seleccionado
    print(f"\nProducto Seleccionado: {category} - {material} - {size}")

    cursor.execute("""
        SELECT * FROM (
            SELECT product_id, s.name AS size, c.name AS category, m.name AS material
            FROM products p
            JOIN sizes s ON s.size_id = p.size_id
            JOIN categories c ON c.category_id = p.category_id 
            JOIN materials m ON m.material_id = p.material_id
        ) a
        WHERE category = %s AND size = %s AND material = %s
    """, (category, size, material))

    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

def manually_populate_customers():
    conn, cursor = postgres_conn()
    insert_values = []

    clear_screen()

    customer_name = input("\u25CF Ingrese el nombre del cliente: ").lower().title() 
    email = input("\u25CF Ingrese el correo electrónico: ").lower()
    address = input("\u25CF Ingrese la dirección: ").lower().capitalize()
    phone = input("\u25CF Ingrese el número de teléfono: ").replace(" ", "")  

    clear_screen()

    cursor.execute("SELECT COUNT(*) FROM Customers WHERE name = %s", (customer_name,))
    count = cursor.fetchone()[0]

    if count > 0:
        print(f"El cliente con el nombre '{customer_name}' ya existe. Abortando la inserción.")
        input("Enter para seguir operando")
        return

    insert_values.append((customer_name, email, address, phone))

    for value in insert_values:
        print(f'\nNombre del Cliente: {value[0]}\nCorreo Electrónico: {value[1]}\nDirección: {value[2]}\nTeléfono: {value[3]}')
     
    while True:
        confirmation1 = input("\n\u25CF Por favor, verifique si los datos son correctos - [S/N]: ").lower() 
        if confirmation1 not in ['s', 'n']:
            print("Entrada inválida")
            continue

        if confirmation1 == 'n':
            return 'no_data'

        if confirmation1 == 's':
            while True:
                confirmation2 = input("\u25CF Por favor, confirme para agregar los datos - [S/N]: ").lower() 
                if confirmation2 not in ['s', 'n']:
                    print("Entrada inválida")
                    continue
                elif confirmation2 == 'n':
                    break
                elif confirmation2 == 's':
                    for values in insert_values:
                        cursor.execute("""
                            INSERT INTO Customers (name, email, address, phone) 
                            VALUES (%s, %s, %s, %s)
                        """, values)
                    conn.commit() 
                    print("\u2605 Datos agregados exitosamente a la tabla.")
                    input("Enter para seguir operando")               
                    return values[0]
            break

def manually_populate_orders():
    conn, cursor = postgres_conn()

    # Get the current maximum order_id in the Orders table
    cursor.execute("SELECT MAX(order_id) FROM Orders")
    max_order_id = cursor.fetchone()[0]

    # Initialize the order_id_counter to one greater than the current maximum order_id
    order_id_counter = max_order_id + 1 if max_order_id is not None else 1

    # Obtener el nombre del cliente
    customer_name = input('Ingrese el nombre del cliente: ').lower().title()
    customer_id = search_customer_id_by_name(cursor, customer_name)

    # Verificar si el cliente existe
    if customer_id is None:
        print('El cliente no existe, vuelva al menu para crear cliente.')
        input ("Enter para volver al menu")
        return

    # Buscar el ID del producto
    product_id = product_id_search()
    cursor.execute("SELECT cost_price FROM Products WHERE product_id = %s", (product_id,))
    result = cursor.fetchone()
    unit_price = round(float(result[0]) * 1.67, 2)

    # Solicitar la cantidad de productos
    while True:
        quantity_input = input('\n\u25CF Cantidad de productos: ')
        if not quantity_input.isdigit():
            print("\u25CF Entrada inválida. Por favor, ingrese un número entero positivo.")
            continue
        quantity = int(quantity_input)
        if quantity <= 0:
            print("\u25CF La cantidad debe ser un número entero positivo.")
        else:
            break

    cursor.execute("""
        INSERT INTO Orders (order_id, customer_id, product_id, quantity, unit_price) 
        VALUES (%s, %s, %s, %s, %s)
        """, (order_id_counter, customer_id, product_id, quantity, unit_price))
    conn.commit() 

    print(f"\n\u2713 Pedido agregado exitosamente a Ordenes.")
    input ("Enter para volver al menu")