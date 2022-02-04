from tkinter import *
from PIL import ImageTk, Image
import sqlite3

root = Tk()
root.title('Add a contact')

connection = sqlite3.connect('address_book.db')
cursor = connection.cursor()

'''
cursor.execute("""CREATE TABLE addresses (
    first_name text,
    last_name text,
    address text,
    city text,
    state text,
    zipcode text
    )""")
'''

first_name = Entry(root, width=30, relief=SUNKEN, borderwidth=2)
first_name.grid(row=0, column=1, padx=10, pady=(10,0))
last_name = Entry(root, width=30, relief=SUNKEN, borderwidth=2)
last_name.grid(row=1, column=1, padx=10)
address = Entry(root, width=30, relief=SUNKEN, borderwidth=2)
address.grid(row=2, column=1, padx=10)
city = Entry(root, width=30, relief=SUNKEN, borderwidth=2)
city.grid(row=3, column=1, padx=10)
state = Entry(root, width=30, relief=SUNKEN, borderwidth=2)
state.grid(row=4, column=1, padx=10)
zipcode = Entry(root, width=30, relief=SUNKEN, borderwidth=2)
zipcode.grid(row=5, column=1, padx=10, pady=(0, 10))

first_name_label = Label(root, text='First name')
first_name_label.grid(row=0, column=0, padx=10)
last_name_label = Label(root, text='Last name')
last_name_label.grid(row=1, column=0, padx=10)
address_label = Label(root, text='Address')
address_label.grid(row=2, column=0, padx=10)
city_label = Label(root, text='City')
city_label.grid(row=3, column=0, padx=10)
state_label = Label(root, text='State')
state_label.grid(row=4, column=0, padx=10)
zipcode_label = Label(root, text='Zipcode')
zipcode_label.grid(row=5, column=0, padx=10)

def delete():
    connection = sqlite3.connect('address_book.db')
    cursor = connection.cursor()

    if delete_entry.get():
        cursor.execute("DELETE FROM addresses WHERE oid= " + delete_entry.get())

    connection.commit()
    connection.close()

    delete_entry.delete(0, END)

def save():
    global edit_window
    global first_name1
    global last_name1
    global address1
    global city1
    global state1
    global zipcode1
    global id

    connection = sqlite3.connect('address_book.db')
    cursor = connection.cursor()

    cursor.execute("""UPDATE addresses SET
            first_name = :first,
            last_name = :last,
            address = :address,
            city = :city,
            state = :state,
            zipcode = :zip
            WHERE oid = :oid""",
            {
                'first': first_name1.get(),
                'last': last_name1.get(),
                'address': address1.get(),
                'city': city1.get(),
                'state': state1.get(),
                'zip': zipcode1.get(),
                'oid': id}   
    )

    connection.commit()
    connection.close()

    edit_window.destroy()

def update():
    global edit_window
    global first_name1
    global last_name1
    global address1
    global city1
    global state1
    global zipcode1
    global id

    id = delete_entry.get()
    if id:
        edit_window = Toplevel()
        edit_window.title('Update a contact')
        
        first_name1 = Entry(edit_window, width=30, relief=SUNKEN, borderwidth=2)
        first_name1.grid(row=0, column=1, padx=10, pady=(10,0))
        last_name1 = Entry(edit_window, width=30, relief=SUNKEN, borderwidth=2)
        last_name1.grid(row=1, column=1, padx=10)
        address1 = Entry(edit_window, width=30, relief=SUNKEN, borderwidth=2)
        address1.grid(row=2, column=1, padx=10)
        city1 = Entry(edit_window, width=30, relief=SUNKEN, borderwidth=2)
        city1.grid(row=3, column=1, padx=10)
        state1 = Entry(edit_window, width=30, relief=SUNKEN, borderwidth=2)
        state1.grid(row=4, column=1, padx=10)
        zipcode1 = Entry(edit_window, width=30, relief=SUNKEN, borderwidth=2)
        zipcode1.grid(row=5, column=1, padx=10, pady=(0, 10))
        first_name_label = Label(edit_window, text='First name')
        first_name_label.grid(row=0, column=0, padx=10)
        last_name_label = Label(edit_window, text='Last name')
        last_name_label.grid(row=1, column=0, padx=10)
        address_label = Label(edit_window, text='Address')
        address_label.grid(row=2, column=0, padx=10)
        city_label = Label(edit_window, text='City')
        city_label.grid(row=3, column=0, padx=10)
        state_label = Label(edit_window, text='State')
        state_label.grid(row=4, column=0, padx=10)
        zipcode_label = Label(edit_window, text='Zipcode')
        zipcode_label.grid(row=5, column=0, padx=10)
        update_button = Button(edit_window, text='SAVE', padx=60, command=save)
        update_button.grid(row=6, column=0, columnspan=2)

        connection = sqlite3.connect('address_book.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM addresses WHERE oid= " + id)
        results = cursor.fetchall()
        for result in results:
            first_name1.insert(0, result[0])
            last_name1.insert(0, result[1])
            address1.insert(0, result[2])
            city1.insert(0, result[3])
            state1.insert(0, result[4])
            zipcode1.insert(0, result[5])

        connection.commit()
        connection.close()

        delete_entry.delete(0, END)

def submit():
    connection = sqlite3.connect('address_book.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO addresses VALUES (:first_name, :last_name, :address, :city, :state, :zipcode)",
            {
                'first_name': first_name.get(),
                'last_name': last_name.get(),
                'address': address.get(),
                'city': city.get(),
                'state': state.get(),
                'zipcode': zipcode.get()
            })

    connection.commit()
    connection.close()

    first_name.delete(0, END)
    last_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)

submit = Button(root, text='Add contact', padx=145, command=submit)
submit.grid(row=6, column=0, columnspan=2, padx=10, pady=2)

def query():
    connection = sqlite3.connect('address_book.db')
    cursor = connection.cursor()

    cursor.execute("SELECT *, oid FROM addresses")
    all_contacts = cursor.fetchall()
    print(all_contacts)

    connection.commit()
    connection.close()

    second_window = Toplevel()
    second_window.title('List of contacts')
    second_window.geometry("400x200")
    for i in range(len(all_contacts)):
        var = str(all_contacts[i][-1]) + '. ' + ', '.join(all_contacts[i][:-1])
        label = Label(second_window, text=var)
        label.pack()
    

query_button = Button(root, text="Show contacts", command=query, padx=137)
query_button.grid(row=7, column=0, columnspan=2, padx=10, pady=2)

delete_entry = Entry(root, borderwidth=2, relief=SUNKEN, width=10)
delete_entry.grid(row=8, column=0, padx=(130,0), pady=10)

delete_button = Button(root, text="DELETE", command=delete, padx=30)
delete_button.grid(row=8, column=1, padx=(0, 60), pady=10)

update_button = Button(root, text="UPDATE", command=update, padx=28)
update_button.grid(row=9, column=1, padx=(0, 60), pady=(0, 10))

connection.commit()
connection.close()

mainloop()