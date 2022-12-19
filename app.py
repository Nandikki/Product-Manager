from tkinter import ttk
from tkinter import *
import sqlite3


class Product():
    def __init__(self, root):
        self.window = root
        self.window.title("Product Manager")
        self.window.resizable(0, 0)
        self.window.wm_iconbitmap('resources/icon.ico')

        root.geometry("400x627")

        style = ttk.Style()

        frame = LabelFrame(self.window, text="Add a new product", font=('Calibri', 12, "bold"))
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        self.nameTag = Label(frame, text="Product name: ", font=('Calibri', 10))
        self.nameTag.grid(row=1, column=0, pady=5)

        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        self.priceTag = Label(frame, text="Product price: ")
        self.priceTag.grid(row=2, column=0, pady=5)

        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        style.configure("my.TButton", font=('Calibri', 12, "bold"))

        self.addBtn = ttk.Button(frame, text="Save product", command=self.add_product, style="my.TButton")
        self.editBtn = ttk.Button(text="Edit product", command=self.edit_product, style="my.TButton")
        self.deleteBtn = ttk.Button(text="Delete product", command=self.delete_product, style="my.TButton")

        self.addBtn.grid(row=3, columnspan=2, sticky=W + E)
        self.editBtn.grid(row=6, column=0, sticky=W + E)
        self.deleteBtn.grid(row=6, column=1, sticky=W + E)

        style.configure("mystyle.Treeview", highlighthickness=0, bd=0, font=('Calibri', 10))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 12, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        self.status = Label(text="", fg="Red")
        self.status.grid(row=4, column=0, columnspan=2, sticky=W + E)

        self.table = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.table.grid(row=5, column=0, columnspan=2)
        self.table.heading('#0', text="Name", anchor=CENTER)
        self.table.heading('#1', text="Price", anchor=CENTER)

        self.get_products()

    db = "database/products.db"

    def db_query(self, query, parameters=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            result = cursor.execute(query, parameters)
            con.commit()
            return result

    def get_products(self):
        reg_table = self.table.get_children()
        for i in reg_table:
            self.table.delete(i)

        query = 'SELECT * FROM product ORDER BY name DESC'
        reg_db = self.db_query(query)

        for i in reg_db:
            print(i)
            self.table.insert('', 0, text=i[1], values=i[2])

    def name_validation(self):
        return len(self.name.get())

    # price_validation will verify if the price > 0 and if it's a number
    def price_validation(self):
        is_number = False
        try:
            float(self.price.get())
            is_number = True
        except ValueError:
            is_number = False

        return len(self.price.get()) and is_number

    def add_product(self):
        if self.price_validation() and self.name_validation():
            self.db_query('INSERT INTO product VALUES(NULL, ?, ?)', (self.name.get(), self.price.get()))
            self.status['fg'] = "Green"
            self.status['text'] = "New Product '{}' successfully saved".format(self.name.get())

        elif self.price_validation() and not (self.name_validation()):
            self.status['fg'] = "Red"
            self.status['text'] = "New product must have a name!"
        else:
            self.status['fg'] = "Red"
            self.status['text'] = "New product must have a price!"

        self.name.delete(0, END)
        self.price.delete(0, END)
        self.get_products()

    def edit_product(self):
        self.status['text'] = ""

        try:
            self.table.item(self.table.selection())['text'][0]
        except IndexError:
            self.status['fg'] = "Red"
            self.status['text'] = "Select a product to edit"
            return None

        self.edit_window = Toplevel()
        self.edit_window.title = "Edit Product"
        self.edit_window.resizable(0, 0)
        self.edit_window.wm_iconbitmap('resources/icon.ico')
        self.edit_window.geometry("200x190")

        title = Label(self.edit_window, text="Edit Product Details", font=("Calibri", 16, "bold"))
        title.grid(column=0, row=0)

        ep_frame = LabelFrame(self.edit_window, text="Edit the product below:", font=("Calibri", 12, "bold"))
        ep_frame.grid(row=1, column=0, columnspan=20, pady=20)

        name = self.table.item(self.table.selection())['text']
        price = self.table.item(self.table.selection())['values'][0]

        self.old_name = Label(ep_frame, text="Old name: ")
        self.old_name.grid(row=2, column=0)

        self.old_name_input = Entry(ep_frame,
                                    textvariable=StringVar(self.edit_window, value=name),
                                    state='readonly')
        self.old_name_input.grid(row=2, column=1)

        self.new_name = Label(ep_frame, text="New name: ")
        self.new_name.grid(row=3, column=0)

        self.new_name_input = Entry(ep_frame)
        self.new_name_input.grid(row=3, column=1)
        self.new_name_input.focus()

        self.old_price = Label(ep_frame, text="Old price: ")  #
        self.old_price.grid(row=4, column=0)

        self.old_price_input = Entry(ep_frame,
                                     textvariable=StringVar(self.edit_window, value=price),
                                     state='readonly')
        self.old_price_input.grid(row=4, column=1)

        self.new_price = Label(ep_frame, text="New price: ")
        self.new_price.grid(row=5, column=0)

        self.new_price_input = Entry(ep_frame)
        self.new_price_input.grid(row=5, column=1)

        self.save_edit_btn = ttk.Button(ep_frame, style="my.TButton", text="Update product", command=lambda:
        self.update_product(self.new_name_input.get(),
                            self.old_name_input.get(),
                            self.new_price_input.get(),
                            self.old_price_input.get())
                                        )
        self.save_edit_btn.grid(row=6, columnspan=2, sticky=W + E)

    def delete_product(self):
        self.status['text'] = ""

        try:
            self.table.item(self.table.selection())['text'][0]
        except IndexError:
            self.status['fg'] = "Red"
            self.status['text'] = "Select a product to delete"
            return None

        query = "DELETE FROM product WHERE name = ?"
        name = self.table.item(self.table.selection())['text']
        self.db_query(query, (name,))

        self.status['fg'] = "#0000ff"
        self.status['text'] = "The product '{}' was successfully deleted.".format(name)

        self.get_products()

    def update_product(self, name, old_name, price, old_price):
        modified = False
        query = "UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?"
        if name != "" and price != "":
            args = (name, price, old_name, old_price)
            modified = True
        elif name != "" and price == "":
            args = (name, old_price, old_name, old_price)
            modified = True
        elif name == "" and price != "":
            args = (old_name, price, old_name, old_price)
            modified = True

        if modified:
            self.db_query(query, (args))

            self.edit_window.destroy()

            self.status['fg'] = "Green"
            self.status['text'] = "The product '{}' was successfully updated!".format(old_name)

            self.get_products()
        else:
            self.edit_window.destroy()
            self.status['fg'] = "Red"
            self.status['text'] = "The product '{}' was not updated. Please, try again.".format(old_name)


if __name__ == '__main__':
    root = Tk()
    app = Product(root)
    root.mainloop()
