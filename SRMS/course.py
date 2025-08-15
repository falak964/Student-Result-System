from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "ResultManagementSystem.db"
class CourseClass:
    def __init__(self, home):
        self.home = home
        self.home.title("Student Result Management System")
        self.home.geometry("1200x500+80+170")
        self.home.config(bg="white")
        self.home.focus_force()
        self._ensure_course_table()

        title = Label(self.home, text="Manage Course", font=("times new roman", 20, "bold"),bg="#CC3366", fg="white").place(x=0, y=0, relwidth=1, height=40)

        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()

        Label(self.home, text="Course Name", font=("times new roman", 15, "bold"), bg="white").place(x=10, y=60)
        Label(self.home, text="Duration", font=("times new roman", 15, "bold"), bg="white").place(x=10, y=100)
        Label(self.home, text="Charges", font=("times new roman", 15, "bold"), bg="white").place(x=10, y=140)
        Label(self.home, text="Description", font=("times new roman", 15, "bold"), bg="white").place(x=10, y=180)

        self.courseName1 = Entry(self.home, textvariable=self.var_course,font=("times new roman", 15, "bold"), bg="lightyellow")
        self.courseName1.place(x=150, y=60, width=200)

        Entry(self.home, textvariable=self.var_duration,
        font=("times new roman", 15, "bold"), bg="lightyellow").place(x=150, y=100, width=200)
        Entry(self.home, textvariable=self.var_charges,font=("times new roman", 15, "bold"), bg="lightyellow").place(x=150, y=140, width=200)

        self.description1 = Text(self.home, font=("times new roman", 15, "bold"), bg="lightyellow")
        self.description1.place(x=150, y=180, width=500, height=150)

        Button(self.home, text="Save", font=("times new roman", 15, "bold"),bg="blue", fg="white", cursor="hand2", command=self.add)\
               .place(x=150, y=400, width=120, height=50)
        Button(self.home, text="Update", font=("times new roman", 15, "bold"),bg="green", fg="white", cursor="hand2", command=self.update)\
               .place(x=290, y=400, width=120, height=50)
        Button(self.home, text="Delete", font=("times new roman", 15, "bold"),bg="grey", fg="white", cursor="hand2", command=self.delete)\
               .place(x=430, y=400, width=120, height=50)
        Button(self.home, text="Clear", font=("times new roman", 15, "bold"),bg="orange", fg="white", cursor="hand2", command=self.clear)\
               .place(x=570, y=400, width=120, height=50)

        self.var_search = StringVar()
        Label(self.home, text="Search By Course Name", font=("times new roman", 15, "bold"), bg="white")\
            .place(x=690, y=60)
        Entry(self.home, textvariable=self.var_search, font=("times new roman", 15, "bold"),
              bg="lightyellow").place(x=910, y=60, width=180)
        Button(self.home, text="Search", font=("times new roman", 15, "bold"),
               bg="blue", fg="white", cursor="hand2", command=self.search)\
        .place(x=1100, y=60, width=90, height=30)

        self.C_Frame = Frame(self.home, bd=2, relief=RIDGE)
        self.C_Frame.place(x=720, y=100, width=470, height=360)

        scroly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrolx = Scrollbar(self.C_Frame, orient=HORIZONTAL)
        self.CourseTable = ttk.Treeview(self.C_Frame,
        columns=("cid", "name", "duration", "charges", "description"),xscrollcommand=scrolx.set,yscrollcommand=scroly.set)
        scrolx.pack(side=BOTTOM, fill=X)
        scroly.pack(side=RIGHT, fill=Y)
        scrolx.config(command=self.CourseTable.xview)
        scroly.config(command=self.CourseTable.yview)

        self.CourseTable.heading("cid", text="Course ID")
        self.CourseTable.heading("name", text="Name")
        self.CourseTable.heading("duration", text="Duration")
        self.CourseTable.heading("charges", text="Charges")
        self.CourseTable.heading("description", text="Description")
        self.CourseTable["show"] = "headings"
        self.CourseTable.column("cid", width=100)
        self.CourseTable.column("name", width=100)
        self.CourseTable.column("duration", width=100)
        self.CourseTable.column("charges", width=100)
        self.CourseTable.column("description", width=150)

        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    def _ensure_course_table(self):
        """Create course table if it doesn't exist."""
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS course (cid INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,duration TEXT,charges TEXT,description TEXT) """)
        conn.commit()
        conn.close()

    def clear(self):
        self.show()
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.description1.delete('1.0', END)
        self.courseName1.config(state=NORMAL)

    def delete(self):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course name should be required", parent=self.home)
            else:
                cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Select the course from the list first", parent=self.home)

                else:
                    p = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.home)
                    if p:
                        cur.execute("DELETE FROM course WHERE name=?", (self.var_course.get(),))
                        conn.commit()
                        messagebox.showinfo("Delete", "Course deleted successfully", parent=self.home)
                        self.clear()
        except Exception as ex:

            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            conn.close()

    def get_data(self, event):
        self.courseName1.config(state="readonly")
        r = self.CourseTable.focus()
        content = self.CourseTable.item(r)
        row = content["values"]
        if not row:
            return
        
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        self.description1.delete('1.0', END)
        self.description1.insert(END, row[4])

    def add(self):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course name should be required", parent=self.home)
            else:
                cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Course name already present", parent=self.home)
                else:
                    cur.execute("INSERT INTO course (name, duration, charges, description) VALUES (?, ?, ?, ?)", (
                        self.var_course.get(),
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.description1.get("1.0", END)))
                    conn.commit()
                    messagebox.showinfo("Great", "Course added successfully", parent=self.home)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
         conn.close()

    def update(self):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course name should be required", parent=self.home)
            else:
                cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row is None:

                    messagebox.showerror("Error", "Select course from list", parent=self.home)
                else:
                    cur.execute("UPDATE course SET duration=?, charges=?, description=? WHERE name=?", (
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.description1.get("1.0", END),
                        self.var_course.get()))
                    conn.commit()

                    messagebox.showinfo("Great", "Course updated successfully", parent=self.home)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            conn.close()

    def show(self):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        try:
            self._ensure_course_table()
            cur.execute("SELECT * FROM course")
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            conn.close()

    def search(self):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        try:
            self._ensure_course_table()
            cur.execute("SELECT * FROM course WHERE name LIKE ?", ('%' + self.var_search.get() + '%',))
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', END, values=row)
        except Exception as ex:
                  messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            conn.close()
if __name__ == "__main__":
    home = Tk()
    obj = CourseClass(home)
    home.mainloop()
