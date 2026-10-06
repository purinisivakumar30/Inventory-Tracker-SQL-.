# 📦 Inventory Management System

A simple and efficient **Inventory Management System** built with **Python** and **SQLite3**. This is a menu-driven command-line application designed to manage products, quantities, prices, stock levels, and overall inventory value.

The project demonstrates practical use of **Python functions, loops, conditional statements, SQLite database operations, and CRUD functionality**.

---

## 🚀 Features

* ➕ **Add Product**

  * Add a new product with its quantity and price.
  * If the product already exists, its information can be replaced.

* ✏️ **Update Product**

  * Update the quantity and price of an existing product.

* 📋 **Show All Products**

  * Display all products stored in the inventory.

* 🔍 **Show Specific Product**

  * Search and display a particular product.

* 🗑️ **Remove Product**

  * Delete a product from the inventory.

* 💰 **Calculate Total Inventory Value**

  * Calculates the total value using:

  `Quantity × Price`

* ⚠️ **Low Stock Detection**

  * Displays products whose quantity is below **5 units**.

* 💾 **SQLite Database**

  * Product information is stored persistently in an SQLite database.

---

## 🛠️ Technologies Used

| Technology   | Purpose                 |
| ------------ | ----------------------- |
| Python       | Application development |
| SQLite3      | Database management     |
| SQL          | Database operations     |
| Command Line | User interface          |

---

## 📂 Project Structure

```text
Inventory-Management-System/
│
├── main.py
├── inventory.db
└── README.md
```

### Files

**`main.py`**
Contains the complete Python application, including the menu, functions, database operations, and inventory logic.

**`inventory.db`**
SQLite database used to store product information.

**`README.md`**
Project documentation and setup instructions.

---

## 🗄️ Database Structure

The application automatically creates a `products` table if it does not already exist.

```sql
CREATE TABLE products (
    name TEXT PRIMARY KEY,
    quantity INTEGER,
    price REAL
);
```

### Product Fields

| Field      | Type    | Description     |
| ---------- | ------- | --------------- |
| `name`     | TEXT    | Product name    |
| `quantity` | INTEGER | Available stock |
| `price`    | REAL    | Product price   |

---

## ⚙️ How It Works

When the application starts, it connects to the SQLite database:

```python
conn = sqlite3.connect('inventory.db')
```

The program then provides a menu with the following options:

```text
1. Add Product
2. Update Product
3. Show All Products
4. Show Specific Product
5. Remove Product
6. Display Total Inventory Value
7. Show Products with Quantity Below 5
8. Exit
```

The menu runs continuously using a Python `while` loop until the user selects **Exit**.

---

## ▶️ Installation & Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the Project

```bash
cd Inventory-Management-System
```

### 3. Run the Application

Make sure Python is installed on your system.

```bash
python main.py
```

On some systems, use:

```bash
python3 main.py
```

---

## 💻 Example

After starting the program:

```text
Inventory Management System
1. Add Product
2. Update Product
3. Show All Products
4. Show Specific Product
5. Remove Product
6. Display Total Inventory Value
7. Show Products with Quantity Below 5
8. Exit

Enter your choice:
```

### Adding a Product

```text
Enter your choice: 1
Enter product name: Laptop
Enter quantity: 10
Enter price: 55000

Product 'Laptop' added/updated successfully.
```

### Displaying Inventory

```text
Laptop: Quantity = 10, Price = Rs55000.00
```

### Low Stock

The system can identify products where:

```text
Quantity < 5
```

---

## 🧠 Concepts Demonstrated

This project is useful for practicing fundamental Python and database concepts:

* Python functions
* `while` loops
* `if/elif/else`
* User input
* Exception-prone type conversion
* SQLite database connection
* SQL `INSERT`
* SQL `UPDATE`
* SQL `SELECT`
* SQL `DELETE`
* SQL aggregate functions
* Parameterized SQL queries
* CRUD operations
* Database persistence

---

## 🔄 CRUD Operations

The application supports complete basic CRUD operations:

| Operation | Function                                |
| --------- | --------------------------------------- |
| Create    | `add_product()`                         |
| Read      | `show_all_products()`, `show_product()` |
| Update    | `update_product()`                      |
| Delete    | `remove_product()`                      |

---

## 📊 Inventory Value Calculation

The total inventory value is calculated using:

```text
Total Inventory Value =
Σ (Quantity × Price)
```

The application uses an SQL query equivalent to:

```sql
SELECT SUM(quantity * price) FROM products;
```

---

## 🎯 Project Objective

The main objective of this project is to create a beginner-friendly inventory system while demonstrating how **Python can interact with a relational database**.

It can be used as a foundation for developing a more advanced inventory management application with a graphical or web-based interface.

---

## 🔮 Future Improvements

Possible improvements for future versions include:

* 🔐 User authentication
* 🖥️ Graphical User Interface (GUI)
* 🌐 Web-based interface using Django or Flask
* 📊 Inventory dashboard
* 📈 Sales and inventory reports
* 🔔 Custom low-stock thresholds
* 🔎 Advanced product search
* 📤 Export inventory to CSV/Excel
* 📥 Import products from CSV
* 🧾 Invoice generation
* 📅 Product transaction history
* 📊 Charts and analytics
* 🧑‍💼 Admin and staff accounts

---

## 👨‍💻 Author

**Pargat Singh**

Computer Science & Engineering Student

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 📜 License

This project is created for **educational and learning purposes**. You are free to modify and improve it for your own projects.
