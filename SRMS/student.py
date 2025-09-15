from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class StudentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1100x500+220+130")
        self.root.config(bg="white")
        self.root.focus_force()

        self.var_rollno = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_dob = StringVar()
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        title = Label(self.root, text="Manage Student Details", font=("goudy old style", 20, "bold"), bg="#0f4d7d", fg="white")
        title.pack(side=TOP, fill=X)

        SearchFrame = LabelFrame(self.root, text="Search Student", font=("goudy old style", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=400, y=70, width=600, height=70)

        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("RollNo", "Name", "Email"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow").place(x=200, y=10)
        btn_search = Button(SearchFrame, text="Search", font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2", command=self.search).place(x=420, y=9, width=150, height=30)

        left_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        left_frame.place(x=20, y=70, width=350, height=400)

        lbl_roll = Label(left_frame, text="Roll No", font=("goudy old style", 15), bg="white").place(x=30, y=30)
        txt_roll = Entry(left_frame, textvariable=self.var_rollno, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=30, width=150)

        lbl_name = Label(left_frame, text="Name", font=("goudy old style", 15), bg="white").place(x=30, y=70)
        txt_name = Entry(left_frame, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=70, width=150)

        lbl_email = Label(left_frame, text="Email", font=("goudy old style", 15), bg="white").place(x=30, y=110)
        txt_email = Entry(left_frame, textvariable=self.var_email, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=110, width=150)

        lbl_gender = Label(left_frame, text="Gender", font=("goudy old style", 15), bg="white").place(x=30, y=150)
        cmb_gender = ttk.Combobox(left_frame, textvariable=self.var_gender, values=("Select", "Male", "Female", "Other"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_gender.place(x=150, y=150, width=150)
        cmb_gender.current(0)

        lbl_contact = Label(left_frame, text="Contact", font=("goudy old style", 15), bg="white").place(x=30, y=190)
        txt_contact = Entry(left_frame, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=190, width=150)

        lbl_dob = Label(left_frame, text="D.O.B", font=("goudy old style", 15), bg="white").place(x=30, y=230)
        txt_dob = Entry(left_frame, textvariable=self.var_dob, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=230, width=150)

        btn_add = Button(left_frame, text="Save", font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2", command=self.add).place(x=10, y=270, width=80, height=30)
        btn_update = Button(left_frame, text="Update", font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2", command=self.update).place(x=100, y=270, width=80, height=30)
        btn_delete = Button(left_frame, text="Delete", font=("goudy old style", 15), bg="#f44336", fg="white", cursor="hand2", command=self.delete).place(x=190, y=270, width=80, height=30)
        btn_clear = Button(left_frame, text="Clear", font=("goudy old style", 15), bg="#607d8b", fg="white", cursor="hand2", command=self.clear).place(x=280, y=270, width=60, height=30)

        table_frame = Frame(self.root, bd=3, relief=RIDGE)
        table_frame.place(x=400, y=150, width=680, height=320)

        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

        self.StudentTable = ttk.Treeview(table_frame, columns=("roll", "name", "email", "gender", "contact", "dob"), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.StudentTable.xview)
        scroll_y.config(command=self.StudentTable.yview)

        self.StudentTable.heading("roll", text="Roll No")
        self.StudentTable.heading("name", text="Name")
        self.StudentTable.heading("email", text="Email")
        self.StudentTable.heading("gender", text="Gender")
        self.StudentTable.heading("contact", text="Contact")
        self.StudentTable.heading("dob", text="D.O.B")
        self.StudentTable["show"] = "headings"

        self.StudentTable.column("roll", width=100)
        self.StudentTable.column("name", width=150)
        self.StudentTable.column("email", width=200)
        self.StudentTable.column("gender", width=100)
        self.StudentTable.column("contact", width=100)
        self.StudentTable.column("dob", width=100)

        self.StudentTable.pack(fill=BOTH, expand=1)
        self.StudentTable.bind("<ButtonRelease-1>", self.get_data)

        self.create_db()
        self.show()

#database
    def create_db(self):
        con = sqlite3.connect("srms.db")
        cur = con.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS student (roll TEXT PRIMARY KEY,name TEXT,email TEXT,gender TEXT,contact TEXT,dob TEXT ) """)
        con.commit()
        con.close()

    def add(self):
        if self.var_rollno.get() == "" or self.var_name.get() == "":
            messagebox.showerror("Error", "Roll No & Name are required", parent=self.root)
        else:
            try:
                con = sqlite3.connect("srms.db")
                cur = con.cursor()
                cur.execute("INSERT INTO student VALUES (?, ?, ?, ?, ?, ?)",
                            (self.var_rollno.get(), self.var_name.get(), self.var_email.get(),
                             self.var_gender.get(), self.var_contact.get(), self.var_dob.get()))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Student Added Successfully", parent=self.root)
                self.show()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Roll No already exists", parent=self.root)

    def show(self):
        con = sqlite3.connect("srms.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM student")
        rows = cur.fetchall()
        self.StudentTable.delete(*self.StudentTable.get_children())
        for row in rows:
            self.StudentTable.insert("", END, values=row)
        con.close()

    def get_data(self, ev):
        f = self.StudentTable.focus()
        content = self.StudentTable.item(f)
        row = content["values"]
        if row:
            self.var_rollno.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            self.var_contact.set(row[4])
            self.var_dob.set(row[5])

    def update(self):
        if self.var_rollno.get() == "":
            messagebox.showerror("Error", "Select a student to update", parent=self.root)
        else:
            con = sqlite3.connect("srms.db")
            cur = con.cursor()
            cur.execute("""
                UPDATE student SET name=?, email=?, gender=?, contact=?, dob=? WHERE roll=?
            """, (self.var_name.get(), self.var_email.get(), self.var_gender.get(),
                  self.var_contact.get(), self.var_dob.get(), self.var_rollno.get()))
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Student Updated Successfully", parent=self.root)
            self.show()

    def delete(self):
        if self.var_rollno.get() == "":
            messagebox.showerror("Error", "Select a student to delete", parent=self.root)
        else:
            con = sqlite3.connect("srms.db")
            cur = con.cursor()
            cur.execute("DELETE FROM student WHERE roll=?", (self.var_rollno.get(),))
            con.commit()
            con.close()
            messagebox.showinfo("Delete", "Student Deleted Successfully", parent=self.root)
            self.clear()

    def clear(self):
        self.var_rollno.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        if self.var_searchby.get() == "" or self.var_searchtxt.get() == "":
            messagebox.showerror("Error", "Select Search By and enter text", parent=self.root)
        else:
            con = sqlite3.connect("srms.db")
            cur = con.cursor()
            cur.execute(f"SELECT * FROM student WHERE {self.var_searchby.get()} LIKE ?", ('%' + self.var_searchtxt.get() + '%',))
            rows = cur.fetchall()
            if len(rows) != 0:
                self.StudentTable.delete(*self.StudentTable.get_children())
                for row in rows:
                    self.StudentTable.insert("", END, values=row)
            else:
                messagebox.showinfo("Result", "No Record Found", parent=self.root)
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = StudentClass(root)
    root.mainloop()

