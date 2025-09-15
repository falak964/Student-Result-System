from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3, os, pathlib

DB_PATH = "ResultManagementSystem.db"

class ResultManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.config(bg="white")
        try:
            self.root.state("zoomed")
        except Exception:
            sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            self.root.geometry(f"{sw}x{sh}+0+0")

        self.root.grid_rowconfigure(2, weight=1)  # content row expands
        self.root.grid_columnconfigure(0, weight=1)

        title = Label(
            self.root, text="Student Result Management",font=("goudy old style", 22, "bold"),bg="#0f4d7d", fg="white", padx=20 ) title.grid(row=0, column=0, sticky="ew")

        mbar = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        mbar.grid(row=1, column=0, sticky="ew", padx=8, pady=(6, 4))
        for i in range(6):
            mbar.grid_columnconfigure(i, weight=1)  # even spacing

        btn_course  = Button(mbar, text="Course", font=("goudy old style", 14, "bold"),bg="blue", fg="white", cursor="hand2",command=self.open_course)
        btn_student = Button(mbar, text="Student", font=("goudy old style", 14, "bold"),bg="blue", fg="white", cursor="hand2",
        command=self.open_student)
        btn_result  = Button(mbar, text="Result", font=("goudy old style", 14, "bold"),bg="blue", fg="white", cursor="hand2",
        command=self.open_result)
        btn_view    = Button(mbar, text="View Student Result", font=("goudy old style", 14, "bold"),bg="blue", fg="white", cursor="hand2", command=self.open_view_result)
        btn_logout  = Button(mbar, text="Logout", font=("goudy old style", 14, "bold"),bg="blue", fg="white", cursor="hand2",
        command=self.logout)
        btn_exit    = Button(mbar, text="Exit", font=("goudy old style", 14, "bold"),bg="blue", fg="white", cursor="hand2",
         command=self.root.quit)

        btn_course.grid (row=0, column=0, padx=8, pady=6, sticky="ew")
        btn_student.grid(row=0, column=1, padx=8, pady=6, sticky="ew")
        btn_result.grid (row=0, column=2, padx=8, pady=6, sticky="ew")
        btn_view.grid   (row=0, column=3, padx=8, pady=6, sticky="ew")
        btn_logout.grid (row=0, column=4, padx=8, pady=6, sticky="ew")
        btn_exit.grid   (row=0, column=5, padx=8, pady=6, sticky="ew")

        content = Frame(self.root, bg="white")
        content.grid(row=2, column=0, sticky="nsew")
        content.grid_rowconfigure(1, weight=1)   
        content.grid_columnconfigure(0, weight=1)

        self.image_holder = Frame(content, bg="white")
        self.image_holder.grid(row=1, column=0, sticky="n", pady=(10, 10))
        self.image_label = Label(self.image_holder, bg="white")
        self.image_label.pack()

        self._src_img = None
        for p in ("images/bg.png", "images/bg.png", "images/Result.png"):
            if pathlib.Path(p).exists():
                try:
                    self._src_img = Image.open(p)
                    break
                except Exception:
                    self._src_img = None
        self._img_cache = None
        self.root.bind("<Configure>", self._on_resize)
        cards = Frame(content, bg="white")
        cards.grid(row=2, column=0, pady=(0, 15))
        for i in range(3):
            cards.grid_columnconfigure(i, weight=1)

        self.lbl_course = Label(cards, text="Total Courses\n[0]",font=("goudy old style", 18, "bold"),bd=5, relief=RIDGE, bg="purple", fg="white",width=18, height=2)
        self.lbl_student = Label(cards, text="Total Students\n[0]",font=("goudy old style", 18, "bold"),bd=5, relief=RIDGE, bg="orange", fg="white",width=18, height=2)
        self.lbl_result = Label(cards, text="Total Results\n[0]", font=("goudy old style", 18, "bold"),bd=5, relief=RIDGE, bg="tomato", fg="white",width=18, height=2)

        self.lbl_course.grid (row=0, column=0, padx=18, pady=4, sticky="n")
        self.lbl_student.grid(row=0, column=1, padx=18, pady=4, sticky="n")
        self.lbl_result.grid (row=0, column=2, padx=18, pady=4, sticky="n")

        footer = Label(self.root,
                       text="Contact Me: shubhamkumbhar45660@gmail.com",
                       font=("goudy old style", 12), bg="#262626", fg="white")footer.grid(row=3, column=0, sticky="ew")

        self.update_counts()

    def _on_resize(self, _event=None):
        """Resize background image to fit nicely and stay centered."""
        if not self._src_img:
            # no image available; show a subtle placeholder one time
            if not getattr(self, "_placeholder_drawn", False):
                self.image_label.config(
                    text="(No background image found)",
                    font=("goudy old style", 14), fg="#777", bg="white", padx=40, pady=60
                )
                self._placeholder_drawn = True
            return

        avail_w = max(600, int(self.root.winfo_width() * 0.7))
        avail_h = max(320, int(self.root.winfo_height() * 0.45))

        iw, ih = self._src_img.size
        scale = min(avail_w / iw, avail_h / ih)
        new_w, new_h = int(iw * scale), int(ih * scale)

        img = self._src_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        self._img_cache = ImageTk.PhotoImage(img)  # keep ref
        self.image_label.config(image=self._img_cache)

    def update_counts(self):
        course = student = result = 0
        try:
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            for table, var in (("course", "course"), ("student", "student"), ("result", "result")):
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                cnt = cur.fetchone()[0]
                if var == "course":  course  = cnt
                if var == "student": student = cnt
                if var == "result":  result  = cnt
            con.close()
        except Exception:
            pass  

        self.lbl_course.config(text=f"Total Courses\n[{course}]")
        self.lbl_student.config(text=f"Total Students\n[{student}]")
        self.lbl_result.config(text=f"Total Results\n[{result}]")

    def _safe_open(self, filename):
        try:
            if pathlib.Path(filename).exists():
                os.system(f'python "{filename}"')
            else:
                messagebox.showinfo("Not Found", f"'{filename}' is not available.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open '{filename}'.\n{e}")

    def open_course(self):        self._safe_open("course.py")
    def open_student(self):       self._safe_open("student.py")
    def open_result(self):        self._safe_open("result.py")
    def open_view_result(self):   self._safe_open("viewstudentresult.py")

    def logout(self):
        if messagebox.askyesno("Logout", "Do you really want to logout?"):
            self.root.destroy()
            try:
                os.system('python login.py')
            except Exception:
                pass


if __name__ == "__main__":
    root = Tk()
    app = ResultManagementSystem(root)
    root.mainloop()

