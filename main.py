import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json

# Load products from JSON file
def load_products():
    try:
        with open("products.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save products to JSON file
def save_products():
    with open("products.json", "w") as file:
        json.dump(products, file, indent=4)

# Load sales from JSON file
def load_sales():
    try:
        with open("sales.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save sales to JSON file
def save_sales():
    with open("sales.json", "w") as file:
        json.dump(sales, file, indent=4)

# Sample product data (if JSON is empty)
products = load_products()
if not products:
    products = [
        {"ID": 1023, "Name": "Phone tempered", "Price": 100, "Quantity": 1000},
        {"ID": 3056, "Name": "Phone Case", "Price": 150, "Quantity": 5},
    ]
    save_products()

sales = load_sales()

cart = []

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

def search_product():
    search_query = entry_search.get().lower()
    for i in tree_products.get_children():
        tree_products.delete(i)
    for product in products:
        if search_query in product["Name"].lower():
            tree_products.insert("", "end", values=(product["ID"], product["Name"], product["Price"], product["Quantity"]))

def add_to_cart():
    selected_item = tree_products.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "No product selected!")
        return

    product_values = tree_products.item(selected_item, "values")
    product_id = int(product_values[0])
    product_name = product_values[1]
    product_price = float(product_values[2])
    product_quantity = int(product_values[3])

    if product_quantity <= 0:
        messagebox.showwarning("Warning", "Product out of stock!")
        return

    try:
        quantity = int(quantity_var.get())
        if quantity <= 0 or quantity > product_quantity:
            messagebox.showwarning("Warning", "Invalid quantity!")
            return

        cart.append({
            "ID": product_id,
            "Name": product_name,
            "Price": product_price,
            "Quantity": quantity,
            "Total": product_price * quantity
        })

        for product in products:
            if product["ID"] == product_id:
                product["Quantity"] -= quantity

        save_products()
        update_cart()
        populate_products()
    except ValueError:
        messagebox.showwarning("Warning", "Please enter a valid quantity!")

def remove_from_cart():
    selected_item = tree_cart.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "No item selected in the cart!")
        return

    cart_item_values = tree_cart.item(selected_item, "values")
    product_id = int(cart_item_values[0])
    quantity_to_remove = int(cart_item_values[3])

    global cart
    cart = [item for item in cart if item["ID"] != product_id]

    for product in products:
        if product["ID"] == product_id:
            product["Quantity"] += quantity_to_remove

    save_products()
    update_cart()
    populate_products()

    messagebox.showinfo("Success", "Item removed from the cart!")

def update_cart():
    for i in tree_cart.get_children():
        tree_cart.delete(i)
    for item in cart:
        tree_cart.insert("", "end", values=(item["ID"], item["Name"], item["Price"], item["Quantity"], item["Total"]))

def generate_bill():
    if not cart:
        messagebox.showwarning("Warning", "Cart is empty!")
        return

    total_amount = sum(item["Total"] for item in cart)
    bill_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save the sale
    sale_record = {
    "Date": bill_date,
    "TotalAmount": total_amount,
    "Items": cart.copy()
    }
    sales.append(sale_record)
    save_sales()

    label_bill_amount.config(text=f"Bill Amount (Rs.): {total_amount}\nDate: {bill_date}")

    clear_cart()
    populate_products()
    populate_sales()
    messagebox.showinfo("Success", "Bill generated and stock updated successfully!")


def clear_cart():
    global cart
    cart = []
    update_cart()

def populate_products():
    for i in tree_products.get_children():
        tree_products.delete(i)
    for product in products:
        tree_products.insert("", "end", values=(product["ID"], product["Name"], product["Price"], product["Quantity"]))
        
def open_login_window():
    login_window = tk.Toplevel(root)
    login_window.title("Admin Login")
    login_window.geometry("300x150")

    tk.Label(login_window, text="Username").pack(pady=5)
    entry_username = tk.Entry(login_window)
    entry_username.pack(pady=5)

    tk.Label(login_window, text="Password").pack(pady=5)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.pack(pady=5)

    def login():
        username = entry_username.get()
        password = entry_password.get()
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            login_window.destroy()
            open_admin_panel()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    tk.Button(login_window, text="Login", command=login).pack(pady=10)

def open_admin_panel():
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Panel")
    admin_window.geometry("600x500")

    tk.Label(admin_window, text="Admin Panel", font=("Arial", 16, "bold")).pack(pady=10)

    # Add product section
    frame_add_product = tk.LabelFrame(admin_window, text="Add Product")
    frame_add_product.pack(fill="x", padx=10, pady=10)

    tk.Label(frame_add_product, text="Name").grid(row=0, column=0, padx=5, pady=5)
    entry_add_name = tk.Entry(frame_add_product)
    entry_add_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_add_product, text="Price").grid(row=1, column=0, padx=5, pady=5)
    entry_add_price = tk.Entry(frame_add_product)
    entry_add_price.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_add_product, text="Quantity").grid(row=2, column=0, padx=5, pady=5)
    entry_add_quantity = tk.Entry(frame_add_product)
    entry_add_quantity.grid(row=2, column=1, padx=5, pady=5)

    def add_product():
        try:
            name = entry_add_name.get()
            price = float(entry_add_price.get())
            quantity = int(entry_add_quantity.get())
            new_id = max(p["ID"] for p in products) + 1
            products.append({"ID": new_id, "Name": name, "Price": price, "Quantity": quantity})
            save_products()
            populate_products()
            messagebox.showinfo("Success", "Product added successfully!")
            entry_add_name.delete(0, tk.END)
            entry_add_price.delete(0, tk.END)
            entry_add_quantity.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please try again.")

    tk.Button(frame_add_product, text="Add Product", command=add_product).grid(row=3, column=0, columnspan=2, pady=10)

    # Delete product section
    def delete_product():
        selected_item = tree_admin_products.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "No product selected!")
            return

        product_values = tree_admin_products.item(selected_item, "values")
        product_id = int(product_values[0])
        global products
        products = [p for p in products if p["ID"] != product_id]
        save_products()
        populate_admin_products()
        populate_products()
        messagebox.showinfo("Success", "Product deleted successfully!")

    tk.Button(admin_window, text="Delete Selected Product", command=delete_product).pack(pady=10)

    # Search product section
    frame_search = tk.LabelFrame(admin_window, text="Search Product")
    frame_search.pack(fill="x", padx=10, pady=10)

    tk.Label(frame_search, text="Search").grid(row=0, column=0, padx=5, pady=5)
    entry_search_admin = tk.Entry(frame_search)
    entry_search_admin.grid(row=0, column=1, padx=5, pady=5)

    def search_admin_product():
        search_query = entry_search_admin.get().lower()
        for i in tree_admin_products.get_children():
            tree_admin_products.delete(i)
        for product in products:
            if search_query in product["Name"].lower():
                tree_admin_products.insert("", "end", values=(product["ID"], product["Name"], product["Price"], product["Quantity"]))

    tk.Button(frame_search, text="Search", command=search_admin_product).grid(row=0, column=2, padx=5, pady=5)

    # Logout button
    def logout():
        admin_window.destroy()

    tk.Button(admin_window, text="Logout", command=logout, bg="red", fg="white").pack(pady=10)

    # Products table in admin panel
    tree_admin_products = ttk.Treeview(admin_window, columns=("ID", "Name", "Price", "Quantity"), show="headings")
    tree_admin_products.heading("ID", text="ID")
    tree_admin_products.heading("Name", text="Name")
    tree_admin_products.heading("Price", text="Price")
    tree_admin_products.heading("Quantity", text="Quantity")
    tree_admin_products.pack(fill="both", expand=True)

    def populate_admin_products():
        for i in tree_admin_products.get_children():
            tree_admin_products.delete(i)
        for product in products:
            tree_admin_products.insert("", "end", values=(product["ID"], product["Name"], product["Price"], product["Quantity"]))

    populate_admin_products()
 # Sales section
    try:
        with open("sales.json", "r") as file:
            sales = json.load(file)
            print("Sales data loaded:", sales)  # Debugging output
    except FileNotFoundError:
        print("sales_data.json not found. Please ensure the file exists.")
        sales = []
    except json.JSONDecodeError:
        print("Error decoding sales_data.json. Ensure the JSON is valid.")

    # Sales Section (with scrollbar)
    frame_sales = tk.LabelFrame(admin_window, text="Sales Data", padx=10, pady=10)
    frame_sales.place(x=440, y=60, width=900, height=158)  # Adjusted placement and size

# Sales Treeview
    tree_sales = ttk.Treeview(frame_sales, columns=("Date", "TotalAmount", "Details"), show="headings")
    tree_sales.heading("Date", text="Date")
    tree_sales.heading("TotalAmount", text="Total Amount (Rs.)")
    tree_sales.heading("Details", text="View Details")

# Adjust column widths
    tree_sales.column("Date", width=150, anchor="center")
    tree_sales.column("TotalAmount", width=120, anchor="center")
    tree_sales.column("Details", width=100, anchor="center")

# Create a Scrollbar for treeview
    sales_scroll = ttk.Scrollbar(frame_sales, orient="vertical", command=tree_sales.yview)
    tree_sales.configure(yscrollcommand=sales_scroll.set)

# Pack tree_sales and scrollbar in the frame
    tree_sales.pack(fill="both", expand=True, side="left")
    sales_scroll.pack(side="right", fill="y")


# Populate Sales Data
    def populate_sales():
        for i in tree_sales.get_children():
            tree_sales.delete(i)
        for sale in sales:
            tree_sales.insert("", "end", values=(sale["Date"], sale["TotalAmount"], "View"))

    def view_sale_details(event):
        selected_item = tree_sales.focus()
        if not selected_item:
            return

        sale_values = tree_sales.item(selected_item, "values")
        sale_date = sale_values[0]

        for sale in sales:
            if sale["Date"] == sale_date:
                sale_details = sale["Items"]
                show_sale_details_window(sale_date, sale_details)
                break

    def show_sale_details_window(sale_date, sale_details):
        details_window = tk.Toplevel(admin_window)
        details_window.title(f"Sale Details - {sale_date}")
        details_window.geometry("400x300")

        details_tree = ttk.Treeview(details_window, columns=("Name", "Quantity", "Total"), show="headings")
        details_tree.heading("Name", text="Product Name")
        details_tree.heading("Quantity", text="Quantity Sold")
        details_tree.heading("Total", text="Total (Rs.)")

        details_tree.column("Name", width=150, anchor="center")
        details_tree.column("Quantity", width=100, anchor="center")
        details_tree.column("Total", width=100, anchor="center")

        details_tree.pack(fill="both", expand=True)

        for item in sale_details:
            details_tree.insert("", "end", values=(item["Name"], item["Quantity"], item["Total"]))

# Bind double-click event to view details
    tree_sales.bind("<Double-1>", view_sale_details)

# Export Sales Data to CSV
    def export_sales_to_csv():
        import csv
        filename = "sales_report.csv"
        with open(filename, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Total Amount (Rs.)", "Product Name", "Quantity Sold"])
            for sale in sales:
                for item in sale["Items"]:
                    writer.writerow([sale["Date"], sale["TotalAmount"], item["Name"], item["Quantity"]])
        messagebox.showinfo("Export Successful", f"Sales data exported to {filename} successfully!")

    tk.Button(admin_window, text="Export Sales to CSV", command=export_sales_to_csv).pack(pady=5)

# Sales Summary
    def show_sales_summary():
        total_sales = sum(sale["TotalAmount"] for sale in sales)
        total_items_sold = sum(item["Quantity"] for sale in sales for item in sale["Items"])
        messagebox.showinfo("Sales Summary", f"Total Sales: Rs. {total_sales}\nTotal Items Sold: {total_items_sold}")


    tk.Button(admin_window, text="Show Sales Summary", command=show_sales_summary).pack(pady=5)

# Initial population of sales data
    populate_sales()


    

# Main Window
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("1200x700")

# Title Section
tk.Label(root, text="Dacles Accessories Shop Inventory System", font=("Arial", 16, "bold"), bg="blue", fg="white").pack(fill="x")

# All Products Section
frame_products = tk.LabelFrame(root, text="All Products", padx=10, pady=10)
frame_products.place(x=10, y=50, width=500, height=500)

entry_search = tk.Entry(frame_products)
entry_search.pack(fill="x", pady=5)
tk.Button(frame_products, text="Search", command=search_product).pack(fill="x")

tree_products = ttk.Treeview(frame_products, columns=("ID", "Name", "Price", "Quantity"), show="headings")

# Set column headings
tree_products.heading("ID", text="ID")
tree_products.heading("Name", text="Name")
tree_products.heading("Price", text="Price")
tree_products.heading("Quantity", text="Quantity")

# Adjust column widths
tree_products.column("ID", width=50, anchor="center")
tree_products.column("Name", width=70, anchor="center")
tree_products.column("Price", width=70, anchor="center")
tree_products.column("Quantity", width=70, anchor="center")

tree_products.pack(fill="both", expand=True)
# Cart Section
frame_cart = tk.LabelFrame(root, text="My Cart", padx=10, pady=10)
frame_cart.place(x=520, y=100, width=350, height=400)

tree_cart = ttk.Treeview(frame_cart, columns=("ID", "Name", "Price", "Quantity", "Total"), show="headings")
tree_cart.heading("ID", text="ID")
tree_cart.heading("Name", text="Name")
tree_cart.heading("Price", text="Price")
tree_cart.heading("Quantity", text="Quantity")
tree_cart.heading("Total", text="Total")

tree_cart.column("ID", width=50, anchor="center")
tree_cart.column("Name", width=70, anchor="center")
tree_cart.column("Price", width=70, anchor="center")
tree_cart.column("Quantity", width=70, anchor="center")
tree_cart.column("Total", width=70, anchor="center")

tree_cart.pack(fill="both", expand=True)

# Quantity and Cart Management Buttons
quantity_var = tk.StringVar()

tk.Label(frame_cart, text="Quantity").pack(anchor="w")
entry_quantity = tk.Entry(frame_cart, textvariable=quantity_var)
entry_quantity.pack(fill="x")

# Frame for Add/Remove Buttons
frame_cart_buttons = tk.Frame(frame_cart)
frame_cart_buttons.pack(fill="x", pady=5)

# Add to Cart Button
btn_add_to_cart = tk.Button(frame_cart_buttons, text="Add to Cart", width=15, command=add_to_cart)
btn_add_to_cart.pack(side="left", padx=5)

# Remove from Cart Button
btn_remove_from_cart = tk.Button(frame_cart_buttons, text="Remove from Cart", width=15, command=lambda: remove_from_cart())
btn_remove_from_cart.pack(side="left", padx=5)

# Calculator Section
frame_calculator = tk.LabelFrame(root, text="Calculator", padx=10, pady=10)
frame_calculator.place(x=880, y=50, width=500, height=500)

calc_display = tk.StringVar()
calc_display_entry = tk.Entry(frame_calculator, textvariable=calc_display, justify="right", font=("Arial", 16))
calc_display_entry.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

buttons = [
    '7', '8', '9', '+',
    '4', '5', '6', '-',
    '1', '2', '3', '*',
    'C', '0', '=', '/'
]

row_val, col_val = 1, 0
for button in buttons:
    if button == "C":
        action = lambda: calc_display.set("")
    elif button == "=":
        action = lambda: evaluate_expression()
    else:
        action = lambda char=button: calc_display.set(calc_display.get() + char)

    tk.Button(frame_calculator, text=button, command=action, height=2, width=5).grid(row=row_val, column=col_val, padx=5, pady=5)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

def evaluate_expression():
    try:
        result = eval(calc_display.get())
        calc_display.set(result)
    except:
        messagebox.showerror("Error", "Invalid Expression!")

# Billing Section
# Billing Section (placed below the calculator)
frame_billing = tk.LabelFrame(root, text="Customer Billing Area", padx=10, pady=10)
frame_billing.place(x=880, y=350, width=300, height=150)  # Positioned directly below the calculator

label_bill_amount = tk.Label(frame_billing, text="Total Amount: 0", font=("Arial", 10))
label_bill_amount.pack(anchor="w")
# Adjust button widths
buttons_frame = tk.Frame(frame_billing)
buttons_frame.pack(fill="x", pady=5)

btn_generate_bill = tk.Button(buttons_frame, text="Generate Bill", command=generate_bill, width=15)
btn_generate_bill.pack(side="left", padx=5)

btn_clear_cart = tk.Button(buttons_frame, text="Clear Cart", command=clear_cart, width=15)
btn_clear_cart.pack(side="left", padx=5)

btn_admin_login = tk.Button(root, text="Admin Login", command=open_login_window, width=20)
btn_admin_login.place(x=850, y=590)  
# Populate product table initially
for product in products:
    tree_products.insert("", "end", values=(product["ID"], product["Name"], product["Price"], product["Quantity"]))

root.mainloop() 