from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import database  


class RegisterClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("500x600+100+100")
        self.root.config(bg="white")

        self.txt_fname = StringVar()
        self.txt_lname = StringVar()
        self.txt_contact = StringVar()
        self.txt_email = StringVar()
        self.cmb_quest = StringVar()
        self.txt_answer = StringVar()
        self.txt_password = StringVar()
        self.txt_confirmpass = StringVar()
        self.txt_UserType = StringVar()

        # UI
        title = Label(self.root, text="Register", font=("goudy old style", 20, "bold"), bg="white", fg="#2f3640").pack(side=TOP, fill=X)

        Label(self.root, text="First Name", font=("times new roman", 15), bg="white").place(x=50, y=60)
        Entry(self.root, textvariable=self.txt_fname, font=("times new roman", 15), bg="lightyellow").place(x=200, y=60)
        Label(self.root, text="Last Name", font=("times new roman", 15), bg="white").place(x=50, y=100)
        Entry(self.root, textvariable=self.txt_lname, font=("times new roman", 15), bg="lightyellow").place(x=200, y=100)
        Label(self.root, text="Contact No.", font=("times new roman", 15), bg="white").place(x=50, y=140)
        Entry(self.root, textvariable=self.txt_contact, font=("times new roman", 15), bg="lightyellow").place(x=200, y=140)
        Label(self.root, text="Email", font=("times new roman", 15), bg="white").place(x=50, y=180)
        Entry(self.root, textvariable=self.txt_email, font=("times new roman", 15), bg="lightyellow").place(x=200, y=180)
        Label(self.root, text="Security Question", font=("times new roman", 15), bg="white").place(x=50, y=220)
        cmb_quest = ttk.Combobox(self.root, textvariable=self.cmb_quest, font=("times new roman", 13), state='readonly', justify=CENTER)
        cmb_quest['values'] = ("Select", "Your First Pet Name", "Your Birth Place", "Your Best Friend Name")
        cmb_quest.place(x=200, y=220)
        cmb_quest.current(0)
        Label(self.root, text="Answer", font=("times new roman", 15), bg="white").place(x=50, y=260)
        Entry(self.root, textvariable=self.txt_answer, font=("times new roman", 15), bg="lightyellow").place(x=200, y=260)
        Label(self.root, text="Password", font=("times new roman", 15), bg="white").place(x=50, y=300)
        Entry(self.root, textvariable=self.txt_password, font=("times new roman", 15), bg="lightyellow", show="*").place(x=200, y=300)
        Label(self.root, text="Confirm Password", font=("times new roman", 15), bg="white").place(x=50, y=340)
        Entry(self.root, textvariable=self.txt_confirmpass, font=("times new roman", 15), bg="lightyellow", show="*").place(x=200, y=340)
        Label(self.root, text="User Type", font=("times new roman", 15), bg="white").place(x=50, y=380)
        cmb_usertype = ttk.Combobox(self.root, textvariable=self.txt_UserType, font=("times new roman", 13), state='readonly', justify=CENTER)
        cmb_usertype['values'] = ("Admin", "User")
        cmb_usertype.place(x=200, y=380)
        cmb_usertype.current(0)

        btn_register = Button(self.root, text="Register", font=("times new roman", 15), bg="#009688", fg="white", cursor="hand2", command=self.register_data)
        btn_register.place(x=200, y=430, width=150, height=35)

    def register_data(self):
        if self.txt_fname.get() == "" or self.txt_lname.get() == "" or self.txt_contact.get() == "" or self.txt_email.get() == "" or self.cmb_quest.get() == "Select" or self.txt_answer.get() == "" or self.txt_password.get() == "" or self.txt_confirmpass.get() == "":
            messagebox.showerror("Error", "All Fields Are Required", parent=self.root)
            return

        if self.txt_password.get() != self.txt_confirmpass.get():
            messagebox.showerror("Error", "Password and Confirm Password must be same", parent=self.root)
            return

        pass1 = self.txt_password.get()
        l, u, p, d = 0, 0, 0, 0
        if len(pass1) >= 8:
            for i in pass1:
                if i.islower():
                    l += 1
                elif i.isupper():
                    u += 1
                elif i.isdigit():
                    d += 1
                elif i in ['@', '&', '#', '!', '_']:
                    p += 1
            if not (l >= 1 and u >= 1 and d >= 1 and p >= 1):
                messagebox.showerror("Error", "Password must have at least 1 uppercase, 1 lowercase, 1 digit, and 1 special character", parent=self.root)
                return
        else:
            messagebox.showerror("Error", "Password must be at least 8 characters long", parent=self.root)
            return

        contact = self.txt_contact.get()
        if not (contact.isdigit() and len(contact) == 10):
            messagebox.showerror("Error", "Contact must be a 10 digit number", parent=self.root)
            return

        email = self.txt_email.get()
        if not (email.endswith("@gmail.com") and "@" in email):
            messagebox.showerror("Error", "Only Gmail addresses are allowed", parent=self.root)
            return

        try:
            con = sqlite3.connect(database.py)  
            cur = con.cursor()
            cur.execute("SELECT * FROM AllUsers WHERE email=?", (self.txt_email.get(),))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error", "User already registered, Please try with another email", parent=self.root)
                return

            cur.execute(
                "INSERT INTO AllUsers (f_name, l_name, contact, email, question, answer, password, u_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    self.txt_fname.get(),
                    self.txt_lname.get(),
                    self.txt_contact.get(),
                    self.txt_email.get(),
                    self.cmb_quest.get(),
                    self.txt_answer.get(),
                    self.txt_password.get(),
                    self.txt_UserType.get()
                )
            )
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Registration Successful", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
if __name__ == "__main__":
    root = Tk()
    obj = RegisterClass(root)
    root.mainloop()
