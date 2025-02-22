
from tkinter import Tk, Button, Label, Scrollbar, Listbox,StringVar,Entry,W,E,N,S,END
from tkinter import ttk 
from tkinter import messagebox
from mysql_config import dbConfig
import mysql.connector as pyo # type: ignore

con = pyo.connect(**dbConfig)
cursor = con.cursor()
selected_tuple = None

class Bookdb:
    def __init__(self):
        self.con = pyo.connect(**dbConfig)
        self.cursor = self.con.cursor()
        print("You have connected to the database")
        print(con)
        
    def _del_(self):
        self.con.close()
       
    def view(self):
        self.cursor.execute("SELECT * FROM books")
        rows = self.cursor.fetchall()
        return rows
    
    def insert(self,title,author, isbn):
        sql=("INSERT INTO books(title,author,isbn)VALUES (%s,%s,%s)")
        values =[title,author,isbn]
        self.cursor.execute(sql,values)
        self.con.commit()
        messagebox.showinfo(title="Book Database", message="New book added to database")
        
    def update(self, id, title, author, isbn):
        tsql =' UPDATE books SET title = %s, author = %s, isbn = %s WHERE id = %s'
        self.cursor.execute(tsql, (title, author,isbn,id))
        self.con.commit()
        messagebox.showinfo(title="Book Database", message="Book updated in database")
        
    def delete(self, id):
        delquery = 'DELETE FROM books WHERE id = %s'
        self.cursor.execute(delquery, [id])
        self.con.commit()
        messagebox.showinfo(title="Book Database", message="Book deleted from database")
        
        
db = Bookdb()    
def get_selected_row(event):
    try:
       global selected_tuple
       index = list_bx.curselection()[0]
       selected_tuple = list_bx.get(index)
       title_entry.delete(0, 'end')
       title_entry.insert('end', selected_tuple[1])
       author_entry.delete(0, 'end')
       author_entry.insert('end', selected_tuple[2])
       isbn_entry.delete(0,'end')
       isbn_entry.insert('end', selected_tuple[3])
    except IndexError:
        selected_tuple = None   
    
def view_records():
    list_bx.delete(0, 'end')
    for row in db.view():
        list_bx.insert('end', row)
        
def add_book():
    print(title_text.get(), author_text.get(), isbn_text.get())
    db.insert(title_text.get(), author_text.get(), isbn_text.get())
    list_bx.delete(0, 'end')
    list_bx.insert('end', (title_text.get(), author_text.get(), isbn_text.get()))
    title_entry.delete(0,"end")
    author_entry.delete(0,"end")
    isbn_entry.delete(0,"end")
    db.con.commit()
    
def delete_records():
    global selected_tuple
    if selected_tuple is None:
        messagebox.showwaring("Selection Error", "Please select a book to delete")
        return
        
        
    db.delete(selected_tuple[0])
    con.commit()
    
    
def clear_screen():
    list_bx.delete(0, 'end')
    title_entry.delete(0,'end')
    author_entry.delete(0,'end')
    isbn_entry.delete(0,'end')
    
def update_records():
    global selected_tuple
    if selected_tuple is None:
       messagebox.showwarning("Selection Error", "Please select a book to update.")
       return


    
    db.update(selected_tuple[0], title_text.get(), author_text.get(), isbn_text.get())
    title_entry.delete(0, "end")
    author_entry.delete(0,"end")
    isbn_entry.delete(0, "end")
    con.commit()
    
def on_closing():
    dd = db
    if messagebox.askokcancle("Quit", "Do you want to quit?"):
        root.destroy()
        del  add 
    
    


root = Tk()
root.title("My Books Database Application")
root.configure(background="light green")
root.geometry("850x500")
root.resizable(width=False, height=False)

title_label =ttk.Label(root,text="Title",background="gold", font=("TkDefaultFont",15))
title_label.grid(row=0,column=0,sticky=W)
title_text = StringVar()
title_entry = ttk.Entry(root, width=22,textvariable=title_text)
title_entry.grid(row=0, column=1, sticky=W)

author_label =ttk.Label(root,text="Author",background="light green", font=("TkDefaultFont",15))
author_label.grid(row=0,column=2,sticky=W)
author_text = StringVar()
author_entry = ttk.Entry(root, width=22,textvariable=author_text)
author_entry.grid(row=0, column=3, sticky=W)

isbn_label =ttk.Label(root,text="ISBN",background="light green", font=("TkDefaultFont",15))
isbn_label.grid(row=0,column=4,sticky=W)
isbn_text = StringVar()
isbn_entry = ttk.Entry(root, width=24,textvariable=isbn_text)
isbn_entry.grid(row=0, column=5, sticky=W)

add_btn =Button(root, text="Add Book", bg="blue", fg="white",font="helvetica 10 bold", command=add_book)
add_btn.grid(row=0, column=6, sticky=W)

list_bx = Listbox(root,height=16,width="40",font="helvetica 13", bg="white")
list_bx.grid(row=3,column=1, columnspan=14,sticky=W + E, pady=40,padx=15)
list_bx.bind('<<ListboxSelect>>', get_selected_row)

scroll_bar = Scrollbar(root)
scroll_bar.grid(row=1,column=8,rowspan=14, sticky=W)

list_bx.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=list_bx.yview)

modify_btn = Button(root,text="Modify Records",bg="purple",fg="white",font="helvetica 10 bold", command=update_records)
modify_btn.grid(row=13, column=4)

delete_btn = Button(root,text="Delete Records",bg="red",fg="white",font="helvetica 10 bold", command=delete_records)
delete_btn.grid(row=13, column=5)

view_btn = Button(root,text="View Records",bg="black",fg="white",font="helvetica 10 bold", command=view_records)
view_btn.grid(row=13, column=2)

exit_btn = Button(root,text="Exit Records",bg="blue",fg="white",font="helvetica 10 bold", command=root.destroy)
exit_btn.grid(row=13, column=3)

clear_btn = Button(root,text="Clear Records",bg="maroon",fg="white",font="helvetica 10 bold", command=clear_screen)
clear_btn.grid(row=13, column=1)








root.mainloop()