import sys
import os
from Configs.postgres_connection import postgres_conn
import psycopg2
from tabulate import tabulate
import random
from faker import Faker
from datetime import datetime
import calendar

def dummy_populate_tables():
    conn, cursor = postgres_conn()

    fake = Faker('es_AR')
    for _ in range(1585):
        name = (f'{fake.first_name()} {fake.last_name()}')
        email = f"{name.split()[0]}{name.split()[-1]}@gmail.com".lower()
        temp_num = (fake.unique.phone_number())
        phone = f'11{temp_num.split()[-2]}{temp_num.split()[-1]}'
        address = fake.unique.street_address()

        cursor.execute ("""INSERT INTO customers (name, email, address, phone) 
                        VALUES (%s, %s, %s, %s)""", (name, email, address, phone))
        conn.commit()


    # Fetching customer IDs
    cursor.execute("SELECT customer_id FROM Customers")
    customer_ids = [row[0] for row in cursor.fetchall()]

    # Fetching products
    cursor.execute("SELECT product_id FROM products")
    products = [row[0] for row in cursor.fetchall()]


    current_year = datetime.now().year
    current_month = datetime.now().month
    current_day = datetime.now().day

    order_id_counter = 1  # Initialize the order ID counter

    for year in range(2023, current_year + 1):  # Loop for 2023 to current year
        num_months = 12 if year != current_year else current_month  # Generate sales for all months until the current month
        for month in range(1, num_months + 1):
            if year == current_year and month == current_month:
                num_days_in_month = current_day - 1  # Generate orders only up to today's date
            else:
                num_days_in_month = calendar.monthrange(year, month)[1]  # Get the number of days in the month
            for day in range(1, num_days_in_month + 1):
                num_orders_for_day = random.randint(1, 10)  # Number of orders for the current day
                for _ in range(num_orders_for_day):
                    random_product_id = random.choice(products)
                    
                    cursor.execute("SELECT cost_price FROM Products WHERE product_id = %s", (random_product_id,))
                    unit_price = round(float(cursor.fetchone()[0]) * 1.67, 2)
                    
                    random_customer_id = random.choice(customer_ids)
                    
                    order_quantity = random.randint(1, 10)
                    
                    # Create order date based on the year, month, and day
                    order_date = datetime(year, month, day)
                                
                    cursor.execute("""
                        INSERT INTO Orders (order_id, customer_id, product_id, quantity, unit_price, order_date) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """, (order_id_counter, random_customer_id, random_product_id, order_quantity, unit_price, order_date))
                    conn.commit()

                    order_id_counter += 1  # Increment the order ID counter

    print("Tablas cargadas con éxito hasta el día de hoy.")
    input("Presiona Enter para volver al menú: ")

    cursor.close()
    conn.close()


