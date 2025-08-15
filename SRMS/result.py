from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class ResultClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_marks = StringVar()
        self.var_full_marks = StringVar()
        self.var_per = StringVar()

        title = Label(self.root, text="Add Student Result", font=("goudy old style", 20, "bold"), bg="#033054", fg="white").place(x=10, y=15, width=1180, height=35)

        lbl_select = Label(self.root, text="Select Student", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=100)
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=160)
        lbl_course = Label(self.root, text="Course", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=220)
        lbl_marks = Label(self.root, text="Marks Obtained", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=280)
        lbl_full_marks = Label(self.root, text="Total Marks", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=340)

        self.txt_student = ttk.Combobox(self.root, textvariable=self.var_roll, font=("goudy old style", 15, "bold"), state='readonly', justify=CENTER)
        self.txt_student.place(x=280, y=100, width=200)
        self.txt_student.bind("<<ComboboxSelected>>", self.fetch_student_data)

        self.txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15, "bold"), bg="lightyellow", state='readonly')
        self.txt_name.place(x=280, y=160, width=320)

        self.txt_course = Entry(self.root, textvariable=self.var_course, font=("goudy old style", 15, "bold"), bg="lightyellow", state='readonly')
        self.txt_course.place(x=280, y=220, width=320)

        self.txt_marks = Entry(self.root, textvariable=self.var_marks, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_marks.place(x=280, y=280, width=320)

        self.txt_full_marks = Entry(self.root, textvariable=self.var_full_marks, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_full_marks.place(x=280, y=340, width=320)

        btn_add = Button(self.root, text="Submit", font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2", command=self.add)
        btn_add.place(x=300, y=420, width=120, height=35)

        btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15), bg="lightgray", fg="black", cursor="hand2", command=self.clear)
        btn_clear.place(x=450, y=420, width=120, height=35)

        self.fetch_student()

        self.create_tables()

    def create_connection(self):
        con = sqlite3.connect(database="ResultManagementSystem.db")
        cur = con.cursor()
        return con, cur

    def create_tables(self):
        con, cur = self.create_connection()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS student (
            roll TEXT PRIMARY KEY,
            name TEXT,
            course TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS course (
            cid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            duration TEXT NOT NULL,
            charges TEXT NOT NULL,
            description TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS result (
            rid INTEGER PRIMARY KEY AUTOINCREMENT,
            roll TEXT,
            name TEXT,
            course TEXT,
            marks_obtain TEXT,
            full_marks TEXT,
            percentage TEXT
        )
        """)

        con.commit()
        con.close()

    def fetch_student(self):
        con, cur = self.create_connection()
        cur.execute("SELECT roll FROM student")
        rows = cur.fetchall()
        self.txt_student['values'] = [row[0] for row in rows]
        con.close()

    def fetch_student_data(self, ev):
        con, cur = self.create_connection()
        cur.execute("SELECT name, course FROM student WHERE roll=?", (self.var_roll.get(),))
        row = cur.fetchone()
        if row:
            self.var_name.set(row[0])
            self.var_course.set(row[1])
        con.close()

    def add(self):
        if self.var_roll.get() == "" or self.var_marks.get() == "" or self.var_full_marks.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                per = (int(self.var_marks.get()) * 100) / int(self.var_full_marks.get())
                self.var_per.set(str(round(per, 2)))

                con, cur = self.create_connection()
                cur.execute("SELECT * FROM result WHERE roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if row:
                    messagebox.showerror("Error", "Result already present", parent=self.root)
                else:
                    cur.execute("INSERT INTO result (roll, name, course, marks_obtain, full_marks, percentage) VALUES (?, ?, ?, ?, ?, ?)", (
                        self.var_roll.get(),
                        self.var_name.get(),
                        self.var_course.get(),
                        self.var_marks.get(),
                        self.var_full_marks.get(),
                        self.var_per.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Result Added Successfully", parent=self.root)
                    self.clear()
                con.close()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")
        self.var_per.set("")




if __name__ == "__main__":
    root = Tk()
    obj = ResultClass(root)
    root.mainloop()
