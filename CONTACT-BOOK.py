import tkinter as tk
from tkinter import messagebox
import sqlite3
import re

def create_database():
    connection = sqlite3.connect("contact_book.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            address TEXT
        )
    ''')
    connection.commit()
    connection.close()

def add_new_contact_to_db(name, phone, email, address):
    connection = sqlite3.connect("contact_book.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                   (name, phone, email, address))
    connection.commit()
    connection.close()
    messagebox.showinfo("Success", "New contact added successfully!")

def get_all_contacts_from_db():
    connection = sqlite3.connect("contact_book.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    connection.close()
    return contacts

def get_contact_by_id(contact_id):
    connection = sqlite3.connect("contact_book.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
    contact = cursor.fetchone()
    connection.close()
    return contact

def update_contact_in_db(contact_id, name, phone, email, address):
    connection = sqlite3.connect("contact_book.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE contacts SET name = ?, phone = ?, email = ?, address = ? WHERE id = ?",
                   (name, phone, email, address, contact_id))
    connection.commit()
    connection.close()
    messagebox.showinfo("Success", "Contact updated successfully!")

def delete_contact_from_db(contact_id):
    connection = sqlite3.connect("contact_book.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    connection.commit()
    connection.close()
    messagebox.showinfo("Success", "Contact deleted successfully!")

def search_contacts_in_db(query):
    connection = sqlite3.connect("contact_book.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?",
                   ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    search_results = cursor.fetchall()
    connection.close()
    return search_results


def validate_name(name):
    return bool(re.match(r"^[A-Za-z\s]+$", name)) # Function to validate the name (only allows letters and spaces)

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("600x500")
        self.root.config(bg="#D3D3D3")

        create_database()

        self.search_var = tk.StringVar()

        self.search_frame = tk.Frame(self.root, bg="#ADD8E6", padx=20, pady=10)
        self.search_frame.pack(fill="x", pady=10)

        tk.Label(self.search_frame, text="Search (Name/Phone/Email):", bg="#ADD8E6").pack(side="left")
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side="left", padx=5)
        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_contacts, bg="#87CEEB")
        self.search_button.pack(side="left", padx=5)

        self.list_frame = tk.Frame(self.root, bg="#F0F8FF", padx=20, pady=10)
        self.list_frame.pack(fill="x", pady=10)

        self.contact_listbox = tk.Listbox(self.list_frame, width=70, height=10, bg="#F8F8FF")
        self.contact_listbox.pack(padx=5)
        self.contact_listbox.bind("<Double-1>", self.view_contact_details)

        self.load_contacts()


        self.add_button = tk.Button(self.root, text="Add New Contact", command=self.add_new_contact, bg="#20B2AA")
        self.add_button.pack(pady=10)


    def load_contacts(self):
        self.contact_listbox.delete(0, tk.END)
        contacts = get_all_contacts_from_db()
        for contact in contacts:
            self.contact_listbox.insert(tk.END, f"{contact[1]} - {contact[2]}")

    def view_contact_details(self, event):
        selection = self.contact_listbox.curselection()
        if selection:
            index = selection[0]
            contact_info = get_all_contacts_from_db()[index]
            contact_id, name, phone, email, address = contact_info

            details_window = tk.Toplevel(self.root)
            details_window.title(f"Contact: {name}")
            details_window.config(bg="#FFFFFF")
            details_window.geometry("400x300")

            tk.Label(details_window, text=f"Name: {name}", bg="#FFFFFF").pack(pady=5)
            tk.Label(details_window, text=f"Phone: {phone}", bg="#FFFFFF").pack(pady=5)
            tk.Label(details_window, text=f"Email: {email}", bg="#FFFFFF").pack(pady=5)
            tk.Label(details_window, text=f"Address: {address}", bg="#FFFFFF").pack(pady=5)

            tk.Button(details_window, text="Edit Contact", command=lambda: self.edit_contact(contact_id), bg="#98FB98").pack(pady=5)
            tk.Button(details_window, text="Delete Contact", command=lambda: self.delete_contact(contact_id), bg="#FF6347").pack(pady=5)

    def add_new_contact(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Contact")
        add_window.config(bg="#F0F8FF")

        form_frame = tk.Frame(add_window, bg="#F0F8FF", padx=20, pady=20)
        form_frame.pack(padx=10, pady=10)

        tk.Label(form_frame, text="Name:", bg="#F0F8FF").grid(row=0, column=0, pady=5, sticky="e")
        name_entry = tk.Entry(form_frame, width=40)
        name_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Phone:", bg="#F0F8FF").grid(row=1, column=0, pady=5, sticky="e")
        phone_entry = tk.Entry(form_frame, width=40)
        phone_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Email:", bg="#F0F8FF").grid(row=2, column=0, pady=5, sticky="e")
        email_entry = tk.Entry(form_frame, width=40)
        email_entry.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Address:", bg="#F0F8FF").grid(row=3, column=0, pady=5, sticky="e")
        address_entry = tk.Entry(form_frame, width=40)
        address_entry.grid(row=3, column=1, pady=5)


        def save_contact():
            name = name_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            address = address_entry.get()
            if name and phone and email and address:
                if not validate_name(name):
                    messagebox.showerror("Error", "Name should only contain letters and spaces!")
                else:
                    add_new_contact_to_db(name, phone, email, address)
                    add_window.destroy()
                    self.load_contacts()
            else:
                messagebox.showerror("Error", "Please fill in all fields!")

        tk.Button(add_window, text="Save Contact", command=save_contact, bg="#98FB98").pack(pady=10)


    def edit_contact(self, contact_id):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Contact")
        edit_window.config(bg="#F0F8FF")

        form_frame = tk.Frame(edit_window, bg="#F0F8FF", padx=20, pady=20)
        form_frame.pack(padx=10, pady=100)

        contact_info = get_contact_by_id(contact_id)
        name, phone, email, address = contact_info[1], contact_info[2], contact_info[3], contact_info[4]


        tk.Label(form_frame, text="Name:", bg="#F0F8FF").grid(row=0, column=0, pady=5, sticky="e")
        name_entry = tk.Entry(form_frame, width=40)
        name_entry.insert(0, name)
        name_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Phone:", bg="#F0F8FF").grid(row=1, column=0, pady=5, sticky="e")
        phone_entry = tk.Entry(form_frame, width=40)
        phone_entry.insert(0, phone)
        phone_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Email:", bg="#F0F8FF").grid(row=2, column=0, pady=5, sticky="e")
        email_entry = tk.Entry(form_frame, width=40)
        email_entry.insert(0, email)
        email_entry.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Address:", bg="#F0F8FF").grid(row=3, column=0, pady=5, sticky="e")
        address_entry = tk.Entry(form_frame, width=40)
        address_entry.insert(0, address)
        address_entry.grid(row=3, column=1, pady=5)


        def save_updated_contact():
            new_name = name_entry.get()
            new_phone = phone_entry.get()
            new_email = email_entry.get()
            new_address = address_entry.get()
            if new_name and new_phone and new_email and new_address:
                if not validate_name(new_name):
                    messagebox.showerror("Error", "Name should only contain letters and spaces!")
                else:
                    update_contact_in_db(contact_id, new_name, new_phone, new_email, new_address)
                    edit_window.destroy()
                    self.load_contacts()
            else:
                messagebox.showerror("Error", "Please fill in all fields!")

        tk.Button(edit_window, text="Save Changes", command=save_updated_contact, bg="#98FB98").pack(pady=10)


    def delete_contact(self, contact_id):
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?")
        if confirm:
            delete_contact_from_db(contact_id)
            self.load_contacts()


    def search_contacts(self):
        query = self.search_var.get()
        results = search_contacts_in_db(query)
        self.contact_listbox.delete(0, tk.END)
        if results:
            for contact in results:
                self.contact_listbox.insert(tk.END, f"{contact[1]} - {contact[2]}")  # Show matching contacts
        else:
            messagebox.showinfo("No Results", "No contacts found matching the search criteria.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
