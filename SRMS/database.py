import sqlite3

def create_db():
    conn = sqlite3.connect("ResultManagementSystem.db")
    cur = conn.cursor()

    cur.execute(""" CREATE TABLE IF NOT EXISTS course( cid INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,duration TEXT,charges TEXT,description TEXT)""")

    cur.execute(""" CREATE TABLE IF NOT EXISTS student( roll INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,email TEXT,gender TEXT,dob TEXT,contact TEXT,admission TEXT,course TEXT,state TEXT,city TEXT,pin TEXT,address TEXT) """)

    cur.execute(""" CREATE TABLE IF NOT EXISTS result( rid INTEGER PRIMARY KEY AUTOINCREMENT,roll TEXT,name TEXT,course TEXT,marks_obtain TEXT,full_marks TEXT,percentage TEXT)""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS AllUsers(eid INTEGER PRIMARY KEY AUTOINCREMENT, f_name TEXT,l_name TEXT,contact TEXT,email TEXT,question TEXT,answer TEXT,password TEXT,u_name TEXT)    """)

    conn.commit()
    conn.close()
create_db()


