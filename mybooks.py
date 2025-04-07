#!/usr/bin/env python3

from tkinter import Tk, Button, Label, Scrollbar, Listbox, StringVar, Entry, W, E, END
from tkinter import ttk, messagebox
from mysql_config import dbConfig
import mysql.connector as pyo  # type: ignore

con = pyo.connect(**dbConfig)
cursor = con.cursor()
selected_tuple = None

class Bookdb:
    def __init__(self):
        self.con = pyo.connect(**dbConfig)
        self.cursor = self.con.cursor()
        print("You have connected to the database")

    def _del_(self):
        self.con.close()

    def view(self):
        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()

    def insert(self, title, author, isbn):
        sql = "INSERT INTO books(title,author,isbn) VALUES (%s,%s,%s)"
        values = [title, author, isbn]
        self.cursor.execute(sql, values)
        self.con.commit()
        messagebox.showinfo(title="📚 Book Database", message="✅ New book added successfully!")

    def update(self, id, title, author, isbn):
        tsql = 'UPDATE books SET title = %s, author = %s, isbn = %s WHERE id = %s'
        self.cursor.execute(tsql, (title, author, isbn, id))
        self.con.commit()
        messagebox.showinfo(title="📚 Book Database", message="🔁 Book updated successfully!")

    def delete(self, id):
        delquery = 'DELETE FROM books WHERE id = %s'
        self.cursor.execute(delquery, [id])
        self.con.commit()
        messagebox.showinfo(title="📚 Book Database", message="🗑️ Book deleted successfully!")

db = Bookdb()

def get_selected_row(event):
    try:
        global selected_tuple
        index = list_bx.curselection()[0]
        selected_tuple = list_bx.get(index)
        title_entry.delete(0, END)
        title_entry.insert(END, selected_tuple[1])
        author_entry.delete(0, END)
        author_entry.insert(END, selected_tuple[2])
        isbn_entry.delete(0, END)
        isbn_entry.insert(END, selected_tuple[3])
    except IndexError:
        selected_tuple = None

def view_records():
    list_bx.delete(0, END)
    for row in db.view():
        list_bx.insert(END, row)

def add_book():
    db.insert(title_text.get(), author_text.get(), isbn_text.get())
    list_bx.delete(0, END)
    list_bx.insert(END, (title_text.get(), author_text.get(), isbn_text.get()))
    title_entry.delete(0, END)
    author_entry.delete(0, END)
    isbn_entry.delete(0, END)

def delete_records():
    global selected_tuple
    if selected_tuple is None:
        messagebox.showwarning("Selection Error", "❗ Please select a book to delete.")
        return
    db.delete(selected_tuple[0])

def clear_screen():
    list_bx.delete(0, END)
    title_entry.delete(0, END)
    author_entry.delete(0, END)
    isbn_entry.delete(0, END)

def update_records():
    global selected_tuple
    if selected_tuple is None:
        messagebox.showwarning("Selection Error", "❗ Please select a book to update.")
        return
    db.update(selected_tuple[0], title_text.get(), author_text.get(), isbn_text.get())
    title_entry.delete(0, END)
    author_entry.delete(0, END)
    isbn_entry.delete(0, END)

# GUI setup
root = Tk()
root.title("📖 My Books Database Application")
root.configure(background="light green")
root.geometry("1180x550")  # Widened window
root.resizable(False, False)

# Labels and entries
title_label = ttk.Label(root, text="📘 Title", background="gold", font=("TkDefaultFont", 15))
title_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
title_text = StringVar()
title_entry = ttk.Entry(root, width=28, textvariable=title_text)
title_entry.grid(row=0, column=1, padx=5, pady=5)

author_label = ttk.Label(root, text="✍️ Author", background="light green", font=("TkDefaultFont", 15))
author_label.grid(row=0, column=2, padx=5, pady=5, sticky=W)
author_text = StringVar()
author_entry = ttk.Entry(root, width=28, textvariable=author_text)
author_entry.grid(row=0, column=3, padx=5, pady=5)

isbn_label = ttk.Label(root, text="🔖 ISBN", background="light green", font=("TkDefaultFont", 15))
isbn_label.grid(row=0, column=4, padx=5, pady=5, sticky=W)
isbn_text = StringVar()
isbn_entry = ttk.Entry(root, width=20, textvariable=isbn_text)
isbn_entry.grid(row=0, column=5, padx=5, pady=5)

# Adjusting the Add button spacing to be closer to the input fields
add_btn = Button(root, text="➕ Add Book", bg="blue", fg="white", font="helvetica 10 bold", width=20, command=add_book)
add_btn.grid(row=1, column=0, columnspan=6, pady=5)  # Reduced pady to bring closer

# Listbox and scrollbar
list_bx = Listbox(root, height=16, width=130, font="helvetica 13", bg="white")
list_bx.grid(row=3, column=0, columnspan=7, padx=15, pady=30, sticky=W+E)
list_bx.bind('<<ListboxSelect>>', get_selected_row)

scroll_bar = Scrollbar(root)
scroll_bar.grid(row=3, column=7, sticky="nsw", pady=30)
list_bx.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=list_bx.yview)

# Action buttons
clear_btn = Button(root, text="🧹 Clear", bg="maroon", fg="white", font="helvetica 10 bold", width=15, command=clear_screen)
clear_btn.grid(row=4, column=0, padx=10, pady=10)

view_btn = Button(root, text="📄 View", bg="black", fg="white", font="helvetica 10 bold", width=15, command=view_records)
view_btn.grid(row=4, column=1, padx=10, pady=10)

exit_btn = Button(root, text="❌ Exit", bg="blue", fg="white", font="helvetica 10 bold", width=15, command=root.destroy)
exit_btn.grid(row=4, column=2, padx=10, pady=10)

modify_btn = Button(root, text="✏️ Modify", bg="purple", fg="white", font="helvetica 10 bold", width=15, command=update_records)
modify_btn.grid(row=4, column=3, padx=10, pady=10)

delete_btn = Button(root, text="🗑️ Delete", bg="red", fg="white", font="helvetica 10 bold", width=15, command=delete_records)
delete_btn.grid(row=4, column=4, padx=10, pady=10)

root.mainloop()
