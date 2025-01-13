Dacles acccessories inventory System

Description

This Inventory System is a desktop application built using Python and the Tkinter library. It provides functionalities to manage a shop's product inventory, track sales, generate bills, and manage stock levels. The system supports two user roles:

Admin: Can add and delete products, view sales data, and perform other administrative tasks.
Employee: Can search for products, add items to their cart, and generate bills.

Features

Admin Panel:

Add, edit, and delete products.
View sales data, including detailed item sales history.
Export sales data to CSV.
View total sales summary.

Employee Panel:

Search for products by name.
Add products to the shopping cart.
Remove items from the cart.
Generate bills and view total amounts.
Clear the cart.
Calculator:

A built-in calculator for calculations during shopping or billing.

Data Persistence:

Sales and products data are saved in JSON files.
Products: products.json
Sales: sales.json

Usage

Admin Login

Click on Admin Login to open the login window.
Enter the username and password:

Username: admin
Password: password

After a successful login, the Admin Panel will open where you can manage the products and view sales data.
employee Operations
Employee can browse the available products in the All Products section.
Use the Search field to search for specific products by name.
Add items to the cart using the Add to Cart button and remove them using Remove from Cart.
Generate a bill by clicking Generate Bill. The total amount will be displayed in the Customer Billing Area.

Admin Panel Operations

Add Product: You can add a new product by entering the name, price, and quantity.
Delete Product: Select a product and click on Delete Selected Product to remove it.
View Sales Data: View past sales records and export them to a CSV file.
Show Sales Summary: View total sales and items sold.

File Structure

inventory-management-system/
├── products.json        # Stores product details
├── sales.json           # Stores sales records
├── project.py              # Main application script
└── README.md            # This readme file