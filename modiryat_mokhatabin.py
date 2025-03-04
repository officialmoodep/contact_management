import os
from tkinter import *
from tkinter import messagebox
import sqlite3


desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')  # برای ویندوز


db_path = os.path.join(desktop_path, "database.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    family TEXT,
    address TEXT,
    phone TEXT
)
""")
conn.commit()


def insert_contact():
    name, family, address, phone = entry_name.get(), entry_family.get(), entry_address.get(), entry_phone.get()
    if name and family and phone:
        cursor.execute("INSERT INTO contacts (name, family, address, phone) VALUES (?, ?, ?, ?)", 
                       (name, family, address, phone))
        conn.commit()
        update_listbox()
        clear_entries()
    else:
        messagebox.showwarning("⚠ خطا", "لطفاً تمام فیلدها را پر کنید!")

def edit_contact():
    try:
        selected = listbox.curselection()[0]
        contact_id = listbox.get(selected).split()[0]
        cursor.execute("SELECT * FROM contacts WHERE id=?", (contact_id,))
        contact = cursor.fetchone()
        if contact:
            entry_name.delete(0, END)
            entry_family.delete(0, END)
            entry_address.delete(0, END)
            entry_phone.delete(0, END)
            entry_name.insert(0, contact[1])
            entry_family.insert(0, contact[2])
            entry_address.insert(0, contact[3])
            entry_phone.insert(0, contact[4])
            cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
            conn.commit()
            update_listbox()
    except IndexError:
        messagebox.showwarning("⚠ خطا", "لطفاً یک مخاطب را انتخاب کنید!")

def delete_contact():
    try:
        selected = listbox.curselection()[0]
        contact_id = listbox.get(selected).split()[0]
        cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
        conn.commit()


        cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='contacts'")
        conn.commit()

        update_listbox()
        clear_entries()
    except IndexError:
        messagebox.showwarning("⚠ خطا", "لطفاً یک مخاطب را انتخاب کنید!")

def show_contact():
    try:
        selected = listbox.curselection()[0]
        contact_id = listbox.get(selected).split()[0]
        cursor.execute("SELECT * FROM contacts WHERE id=?", (contact_id,))
        contact = cursor.fetchone()
        if contact:
            show_window = Toplevel(root)
            show_window.title("📄 نمایش مخاطب")
            show_window.geometry("350x250")
            show_window.configure(bg="#23272A")

            Label(show_window, text=f"📝 نام: {contact[1]}", font=("Arial", 12), bg="#23272A", fg="white").pack(pady=5)
            Label(show_window, text=f"👨‍👩‍👧 نام خانوادگی: {contact[2]}", font=("Arial", 12), bg="#23272A", fg="white").pack(pady=5)
            Label(show_window, text=f"📍 آدرس: {contact[3]}", font=("Arial", 12), bg="#23272A", fg="white").pack(pady=5)
            Label(show_window, text=f"📞 تلفن: {contact[4]}", font=("Arial", 12), bg="#23272A", fg="white").pack(pady=5)

            Button(show_window, text="❌ بستن", command=show_window.destroy, bg="#F04747", fg="white",
                   font=("Arial", 11, "bold"), bd=3, relief="ridge", width=12).pack(pady=10)
    except IndexError:
        messagebox.showwarning("⚠ خطا", "لطفاً یک مخاطب را انتخاب کنید!")

def update_listbox(query="SELECT * FROM contacts"):
    listbox.delete(0, END)
    cursor.execute(query)
    for contact in cursor.fetchall():
        listbox.insert(END, f"{contact[0]} - {contact[1]} {contact[2]} - {contact[3]} - {contact[4]}")

def clear_entries():
    entry_name.delete(0, END)
    entry_family.delete(0, END)
    entry_address.delete(0, END)
    entry_phone.delete(0, END)

def cancel_app():
    answer = messagebox.askyesno("⚠ خروج", "آیا مطمئن هستید که می‌خواهید خارج شوید؟")
    if answer:
        root.quit()

def search_contact():
    search_term = entry_search.get()
    if search_term:
        query = f"SELECT * FROM contacts WHERE name LIKE '%{search_term}%' OR family LIKE '%{search_term}%'"
        update_listbox(query)
    else:
        messagebox.showwarning("⚠ خطا", "لطفاً نام یا نام خانوادگی برای جستجو وارد کنید.")

def clear_search():
    entry_search.delete(0, END)
    update_listbox()


root = Tk()
root.title("📞 مدیریت مخاطبین")
root.geometry("650x550")
root.configure(bg="#2C2F33")


btn_style = {"font": ("Arial", 11, "bold"), "bd": 3, "relief": "ridge", "width": 12, "height": 1}


frame = Frame(root, bg="#23272A", padx=15, pady=15)
frame.pack(pady=10)

Label(frame, text="📝 نام:", bg="#23272A", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
Label(frame, text="👨‍👩‍👧 نام خانوادگی:", bg="#23272A", fg="white", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w")
Label(frame, text="📍 آدرس:", bg="#23272A", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=2, sticky="w")
Label(frame, text="📞 تلفن:", bg="#23272A", fg="white", font=("Arial", 12, "bold")).grid(row=1, column=2, sticky="w")

entry_name = Entry(frame, font=("Arial", 11), bd=2, relief="solid")
entry_family = Entry(frame, font=("Arial", 11), bd=2, relief="solid")
entry_address = Entry(frame, font=("Arial", 11), bd=2, relief="solid")
entry_phone = Entry(frame, font=("Arial", 11), bd=2, relief="solid")
entry_name.grid(row=0, column=1, padx=10, pady=5)
entry_family.grid(row=1, column=1, padx=10, pady=5)
entry_address.grid(row=0, column=3, padx=10, pady=5)
entry_phone.grid(row=1, column=3, padx=10, pady=5)


frame_search = Frame(root, bg="#23272A", padx=15, pady=15)
frame_search.pack(pady=10)

Label(frame_search, text="🔍 جستجو:", bg="#23272A", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
entry_search = Entry(frame_search, font=("Arial", 11), bd=2, relief="solid")
entry_search.grid(row=0, column=1, padx=10, pady=5)

Button(frame_search, text="🔍 جستجو", command=search_contact, bg="#7289DA", fg="white", **btn_style).grid(row=0, column=2, padx=5, pady=5)



btn_frame = Frame(root, bg="#23272A")
btn_frame.pack()

Button(btn_frame, text="➕ افزودن", command=insert_contact, bg="#7289DA", fg="white", **btn_style).grid(row=0, column=0, padx=5, pady=5)
Button(btn_frame, text="✏️ ویرایش", command=edit_contact, bg="#FAA61A", fg="black", **btn_style).grid(row=0, column=1, padx=5, pady=5)
Button(btn_frame, text="❌ حذف", command=delete_contact, bg="#F04747", fg="white", **btn_style).grid(row=0, column=2, padx=5, pady=5)
Button(btn_frame, text="👁 نمایش", command=show_contact, bg="#43B581", fg="white", **btn_style).grid(row=0, column=3, padx=5, pady=5)
Button(btn_frame, text="🚪 خروج", command=cancel_app, bg="#F04747", fg="white", **btn_style).grid(row=1, column=0, padx=5, pady=5)


listbox = Listbox(root, width=80, height=15, font=("Arial", 10), bg="#2C2F33", fg="white", bd=2, relief="solid")
listbox.pack(pady=10)

update_listbox()
root.mainloop()