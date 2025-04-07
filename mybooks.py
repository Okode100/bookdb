root = Tk()
root.title("My Books Database Application")
root.configure(background="light green")
root.geometry("1000x600")
root.resizable(width=False, height=False)

# === Form Frame for Entries ===
form_frame = ttk.Frame(root, padding="10 10 10 10")
form_frame.grid(row=0, column=0, columnspan=7, sticky=W)

title_label = ttk.Label(form_frame, text="Title", background="gold", font=("TkDefaultFont", 13))
title_label.grid(row=0, column=0, sticky=W, padx=5, pady=5)
title_text = StringVar()
title_entry = ttk.Entry(form_frame, width=30, textvariable=title_text)
title_entry.grid(row=0, column=1, sticky=W, padx=5)

author_label = ttk.Label(form_frame, text="Author", background="light green", font=("TkDefaultFont", 13))
author_label.grid(row=0, column=2, sticky=W, padx=5)
author_text = StringVar()
author_entry = ttk.Entry(form_frame, width=30, textvariable=author_text)
author_entry.grid(row=0, column=3, sticky=W, padx=5)

isbn_label = ttk.Label(form_frame, text="ISBN", background="light green", font=("TkDefaultFont", 13))
isbn_label.grid(row=0, column=4, sticky=W, padx=5)
isbn_text = StringVar()
isbn_entry = ttk.Entry(form_frame, width=25, textvariable=isbn_text)
isbn_entry.grid(row=0, column=5, sticky=W, padx=5)

add_btn = Button(form_frame, text="Add Book", bg="blue", fg="white", font="helvetica 10 bold", command=add_book)
add_btn.grid(row=0, column=6, padx=10)

# === Listbox and Scrollbar ===
list_frame = ttk.Frame(root)
list_frame.grid(row=1, column=0, columnspan=7, padx=20, pady=20, sticky=W)

list_bx = Listbox(list_frame, height=16, width=110, font="helvetica 13", bg="white")
list_bx.grid(row=0, column=0, sticky=W + E)

scroll_bar = Scrollbar(list_frame, orient="vertical", command=list_bx.yview)
scroll_bar.grid(row=0, column=1, sticky='ns')

list_bx.configure(yscrollcommand=scroll_bar.set)
list_bx.bind('<<ListboxSelect>>', get_selected_row)

# === Buttons Section ===
button_frame = ttk.Frame(root, padding="10")
button_frame.grid(row=2, column=0, columnspan=7)

view_btn = Button(button_frame, text="View Records", bg="black", fg="white", font="helvetica 10 bold", command=view_records)
view_btn.grid(row=0, column=0, padx=10, pady=5)

clear_btn = Button(button_frame, text="Clear Records", bg="maroon", fg="white", font="helvetica 10 bold", command=clear_screen)
clear_btn.grid(row=0, column=1, padx=10, pady=5)

modify_btn = Button(button_frame, text="Modify Records", bg="purple", fg="white", font="helvetica 10 bold", command=update_records)
modify_btn.grid(row=0, column=2, padx=10, pady=5)

delete_btn = Button(button_frame, text="Delete Records", bg="red", fg="white", font="helvetica 10 bold", command=delete_records)
delete_btn.grid(row=0, column=3, padx=10, pady=5)

exit_btn = Button(button_frame, text="Exit", bg="blue", fg="white", font="helvetica 10 bold", command=root.destroy)
exit_btn.grid(row=0, column=4, padx=10, pady=5)

root.mainloop()