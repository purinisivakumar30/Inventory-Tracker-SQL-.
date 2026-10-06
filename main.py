'''Inventory Management System (Dictionary + Functions + Loops)
        Create a menu-driven program to:
       Add/update a product with quantity and price.
      Remove a product.
      Display total inventory value.
      Show products with quantity below 5.'''


import sqlite3

conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# create the products table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    name TEXT PRIMARY KEY,
    quantity INTEGER,
    price REAL
)
''')
conn.commit()   

# add product to the inventory
def add_product(cursor, product_name, quantity, price):
    cursor.execute('INSERT OR REPLACE INTO products (name, quantity, price) VALUES (?, ?, ?)', (product_name, quantity, price))
    conn.commit()


# update product in the inventory
def update_product(cursor, product_name, quantity, price):
    cursor.execute('UPDATE products SET quantity = ?, price = ? WHERE name = ?', (quantity, price, product_name))
    conn.commit()

#show all products in the inventory
def show_all_products(cursor):
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    if products:
        for product in products:
            print(f"{product[0]}: Quantity = {product[1]}, Price = rs{product[2]:.2f}")         
    else:
        print(f"Product not found in inventory.")

# show a specific product in the inventory
def show_product(cursor, product_name):
    cursor.execute('SELECT * FROM products WHERE name = ?', (product_name,))
    product = cursor.fetchone()
    if product:
        print(f"{product[0]}: Quantity = {product[1]}, Price = rs{product[2]:.2f}")
    else:
        print(f"Product '{product_name}' not found in inventory.")


# remove a product from the inventory
def remove_product(cursor, product_name):
    cursor.execute('DELETE FROM products WHERE name = ?', (product_name,))
    conn.commit()
    print(f"Product '{product_name}' removed successfully.")

# display total inventory value
def display_inventory_value(cursor):
    cursor.execute('SELECT SUM(quantity * price) FROM products')
    total_value = cursor.fetchone()[0]
    print(f"Total inventory value: rs{total_value:.2f}")

#def show products with quantity below 5
def show_low_stock_products(cursor):
    cursor.execute('SELECT * FROM products WHERE quantity < 5')
    low_stock_products = cursor.fetchall()
    if low_stock_products:
        print("Products with quantity below 5:")
        for product in low_stock_products:
            print(f"{product[0]}: Quantity = {product[1]}, Price = rs{product[2]:.2f}")
    else:
        print("No products with quantity below 5.")


# main function to run the inventory management system
def main():
    while True:
        print("\nInventory Management System")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Show All Products")
        print("4. Show Specific Product")
        print("5. Remove Product")
        print("6. Display Total Inventory Value")
        print("7. Show Products with Quantity Below 5")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter product name: ")
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price: "))
            add_product(cursor, name, quantity, price)
            print(f"Product '{name}' added/updated successfully.")


        elif choice == '2':
            name = input("Enter product name to update: ")
            quantity = int(input("Enter new quantity: "))
            price = float(input("Enter new price: "))
            update_product(cursor, name, quantity, price)
            print(f"Product '{name}' updated successfully.")


        elif choice == '3':
            show_all_products(cursor)

        elif choice == '4':
            name = input("Enter product name to show: ")
            show_product(cursor, name)

        elif choice == '5':
            name = input("Enter product name to remove: ")
            remove_product(cursor, name)
            print(f"Product '{name}' removed successfully.")


        elif choice == '6':
            display_inventory_value(cursor)

        
        elif choice == '7':
            show_low_stock_products(cursor)

        
        elif choice == '8':
            print("Exiting the program.")
            break


        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()  

