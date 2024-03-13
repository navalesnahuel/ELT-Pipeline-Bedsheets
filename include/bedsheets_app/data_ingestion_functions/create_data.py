import psycopg2
import random
import sys
import os
from Configs.postgres_connection import postgres_conn
from Configs.usd_convertion import usd_to_ars

def delete_tables():
    conn, cursor = postgres_conn()
    try:
        cursor.execute(""" 
            DROP SCHEMA public CASCADE;
            CREATE SCHEMA public """)
            
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        pass

def create_tables():
    conn, cursor = postgres_conn()

    delete_tables()
    queries = [
        """
        CREATE TABLE IF NOT EXISTS Categories (
            category_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS Materials (
            material_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS Sizes (
            size_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Products (
            product_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            cost_price DECIMAL(10, 2) NOT NULL,
            category_id INT REFERENCES Categories(category_id),
            material_id INT REFERENCES Materials(material_id),
            size_id INT REFERENCES Sizes(size_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            address VARCHAR(255),
            phone VARCHAR(20)
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS Orders (
            order_id SERIAL PRIMARY KEY,
            customer_id INT REFERENCES Customers(customer_id),
            product_id INT REFERENCES Products(product_id),
            quantity INT NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL,
            order_date DATE DEFAULT CURRENT_DATE
        );
        """
    ]

    for query in queries:
        cursor.execute(query)

    try:
        cursor.execute("ALTER TABLE Sizes ADD CONSTRAINT unique_size_name UNIQUE (name);")
        cursor.execute("ALTER TABLE Materials ADD CONSTRAINT unique_material_name UNIQUE (name);")
        cursor.execute("ALTER TABLE Categories ADD CONSTRAINT unique_category_name UNIQUE (name);")
        cursor.execute("ALTER TABLE Products ADD CONSTRAINT unique_product_name UNIQUE (name);")
    except Exception as e:
        pass
        
    cursor.close()
    conn.commit()
    conn.close()

def populate_size():
    conn, cursor = postgres_conn()

    try:
        cursor.execute("""
            INSERT INTO Sizes (name) VALUES
                ('1 1/2 Plaza'),
                ('2 1/2 Plazas'),
                ('King'),
                ('Queen'),
                ('2 Plazas'),
                ('1 Plaza');
        """)
        conn.commit()
        print("Tamaños insertados correctamente.")


    except Exception as e:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def populate_materials():
    conn, cursor = postgres_conn()

    try:
        cursor.execute("""
        INSERT INTO Materials (name) VALUES
            ('Algodón'),
            ('Poliéster'),
            ('Microfibra'),
            ('Algodón y Poliéster'),
            ('Percal'),
            ('Ultra Soft');
        """)
        conn.commit()
        print("Materiales insertados correctamente.")

    except Exception as e:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def populate_category():
    conn, cursor = postgres_conn()

    try:
        cursor.execute("""
        INSERT INTO Categories (name, description) VALUES
            ('Sábanas', 'Sábanas de diferentes materiales y tamaños para camas.'),
            ('Juegos de Sábanas', 'Juegos de sábanas completos con funda de almohada.'),
            ('Funda de Colchón', 'Fundas ajustables para colchones.');
        """)
        conn.commit()
        print("Categorias insertadas correctamente.")

    except Exception as e:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def populate_products():
    conn, cursor = postgres_conn()
    price_matrix = usd_to_ars()

    try:
        cursor.execute("SELECT category_id, name FROM Categories;")
        categories = cursor.fetchall()

        cursor.execute("SELECT material_id, name FROM Materials;")
        materials = cursor.fetchall()

        cursor.execute("SELECT size_id, name FROM Sizes;")
        sizes = cursor.fetchall()

        insert_values = []
        for category_id, category_name in categories:
            for material_id, material_name in materials:
                for size_id, size_name in sizes:
                    product_name = f"{category_name} de {material_name} - {size_name}"
                    cost_price = price_matrix.get(category_id, {}).get(material_id, {}).get(size_id, 0)
                    insert_values.append((product_name, cost_price, category_id, material_id, size_id))
                    
        cursor.executemany("""
            INSERT INTO Products (name, cost_price, category_id, material_id, size_id) 
            VALUES (%s, %s, %s, %s, %s);
        """, insert_values)
        conn.commit()
        print("Productos insertados correctamente.")
        input ("Enter para volver al menu")

    except Exception as e:
        print(f"Error al insertar productos, puede que ya se encuentren insertados.")
        input ("Enter para volver al menu")
        conn.rollback() 
    finally:
        cursor.close()
        conn.close()

def formating():
    create_tables()
    populate_size()
    populate_materials()
    populate_category()
    populate_products()