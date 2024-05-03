import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Function to connect to MySQL database
def connect_to_db():
    try:
        print("Connecting to the database...")
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="hospital"
        )
        print("Connected to the database successfully.")
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error connecting to MySQL database: {err}")
        return None

# Function to create patient table if not exists
def create_patient_table(conn):
    try:
        print("Creating patient table...")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient (
                patient_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                address VARCHAR(255),
                mobile_no VARCHAR(15),
                age INT,
                dob DATE,
                disease VARCHAR(255),
                doctor_id INT
            )
        """)
        conn.commit()
        print("Patient table created successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error creating patient table: {err}")
    finally:
        if cursor:
            cursor.close()

# Function to create doctor table if not exists
def create_doctor_table(conn):
    try:
        print("Creating doctor table...")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctor (
                doctor_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                specialization VARCHAR(255),
                contact_no VARCHAR(15),
                address VARCHAR(255)
            )
        """)
        conn.commit()
        print("Doctor table created successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error creating doctor table: {err}")
    finally:
        if cursor:
            cursor.close()

# Function to create medicine table if not exists
def create_medicine_table(conn):
    try:
        print("Creating medicine table...")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medicine (
                medicine_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                manufacturer VARCHAR(255),
                price DECIMAL(10, 2)
            )
        """)
        conn.commit()
        print("Medicine table created successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error creating medicine table: {err}")
    finally:
        if cursor:
            cursor.close()

# Function to add patient to database
def add_patient(name, address, mobile_no, age, dob, disease, doctor_id):
    conn = None
    try:
        print("Adding patient to the database...")
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO patient (name, address, mobile_no, age, dob, disease, doctor_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, address, mobile_no, age, dob, disease, doctor_id))
            conn.commit()
            print("Patient added successfully.")
            clear_entries()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error adding patient: {err}")
    finally:
        if conn:
            conn.close()

# Function to add doctor to database
def add_doctor(name, specialization, contact_no, address):
    conn = None
    try:
        print("Adding doctor to the database...")
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO doctor (name, specialization, contact_no, address)
                VALUES (%s, %s, %s, %s)
            """, (name, specialization, contact_no, address))
            conn.commit()
            print("Doctor added successfully.")
            clear_entries()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error adding doctor: {err}")
    finally:
        if conn:
            conn.close()

# Function to add medicine to database
def add_medicine(name, manufacturer, price):
    conn = None
    try:
        print("Adding medicine to the database...")
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO medicine (name, manufacturer, price)
                VALUES (%s, %s, %s)
            """, (name, manufacturer, price))
            conn.commit()
            print("Medicine added successfully.")
            clear_entries()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error adding medicine: {err}")
    finally:
        if conn:
            conn.close()

# Function to clear entry fields
def clear_entries():
    for entry in patient_entries:
        entry.delete(0, tk.END)
    for entry in doctor_entries:
        entry.delete(0, tk.END)
    for entry in medicine_entries:
        entry.delete(0, tk.END)

# Function to search patient
def search_patient():
    conn = None
    try:
        print("Searching patient...")
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            search_query = """
                SELECT * FROM patient WHERE mobile_no = %s
            """
            mobile_no = patient_entries[2].get()  # Mobile number is at index 2 in patient_entries list
            cursor.execute(search_query, (mobile_no,))
            rows = cursor.fetchall()
            if rows:
                print("Patient found:")
                for row in rows:
                    print(row)
            else:
                print("Patient not found.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error searching patient: {err}")
    finally:
        if conn:
            conn.close()

# Function to search doctor
def search_doctor():
    conn = None
    try:
        print("Searching doctor...")
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            search_query = """
                SELECT * FROM doctor WHERE contact_no = %s
            """
            contact_no = doctor_entries[2].get()  # Contact number is at index 2 in doctor_entries list
            cursor.execute(search_query, (contact_no,))
            rows = cursor.fetchall()
            if rows:
                print("Doctor found:")
                for row in rows:
                    print(row)
            else:
                print("Doctor not found.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error searching doctor: {err}")
    finally:
        if conn:
            conn.close()

# Function to search medicine
def search_medicine():
    conn = None
    try:
        print("Searching medicine...")
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            search_query = """
                SELECT * FROM medicine WHERE name = %s
            """
            medicine_name = medicine_entries[0].get()  # Medicine name is at index 0 in medicine_entries list
            cursor.execute(search_query, (medicine_name,))
            rows = cursor.fetchall()
            if rows:
                print("Medicine found:")
                for row in rows:
                    print(row)
            else:
                print("Medicine not found.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error searching medicine: {err}")
    finally:
        if conn:
            conn.close()

# GUI setup
root = tk.Tk()
root.title("Hospital Management System")
root.geometry("800x600")

# Patient Details Frame
patient_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
patient_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.2)

# Labels and Entry fields for Patient Details
patient_labels = ["Name:", "Address:", "Mobile No:", "Age:", "Date of Birth:", "Disease:", "Doctor ID:"]
patient_entries = []
for i, label_text in enumerate(patient_labels):
    tk.Label(patient_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5)
    entry = tk.Entry(patient_frame)
    entry.grid(row=i, column=1, padx=5, pady=5)
    patient_entries.append(entry)

# Submit Button for Patient Details
submit_patient_button = tk.Button(patient_frame, text="Submit", command=lambda: add_patient(*[entry.get() for entry in patient_entries]))
submit_patient_button.grid(row=len(patient_labels), column=0, columnspan=2, pady=10, padx=5, sticky="ew")

# Doctor Details Frame
doctor_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
doctor_frame.place(relx=0.05, rely=0.3, relwidth=0.9, relheight=0.2)

# Labels and Entry fields for Doctor Details
doctor_labels = ["Name:", "Specialization:", "Contact No:", "Address:"]
doctor_entries = []
for i, label_text in enumerate(doctor_labels):
    tk.Label(doctor_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5)
    entry = tk.Entry(doctor_frame)
    entry.grid(row=i, column=1, padx=5, pady=5)
    doctor_entries.append(entry)

# Submit Button for Doctor Details
submit_doctor_button = tk.Button(doctor_frame, text="Submit", command=lambda: add_doctor(*[entry.get() for entry in doctor_entries]))
submit_doctor_button.grid(row=len(doctor_labels), column=0, columnspan=2, pady=10, padx=5, sticky="ew")

# Medicine Details Frame
medicine_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
medicine_frame.place(relx=0.05, rely=0.55, relwidth=0.9, relheight=0.2)

# Labels and Entry fields for Medicine Details
medicine_labels = ["Name:", "Manufacturer:", "Price:"]
medicine_entries = []
for i, label_text in enumerate(medicine_labels):
    tk.Label(medicine_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5)
    entry = tk.Entry(medicine_frame)
    entry.grid(row=i, column=1, padx=5, pady=5)
    medicine_entries.append(entry)

# Submit Button for Medicine Details
submit_medicine_button = tk.Button(medicine_frame, text="Submit", command=lambda: add_medicine(*[entry.get() for entry in medicine_entries]))
submit_medicine_button.grid(row=len(medicine_labels), column=0, columnspan=2, pady=10, padx=5, sticky="ew")

# Search Components
search_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
search_frame.place(relx=0.05, rely=0.8, relwidth=0.9, relheight=0.15)

# Search buttons for patient, doctor, and medicine
tk.Button(search_frame, text="Search Patient", command=search_patient).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(search_frame, text="Search Doctor", command=search_doctor).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(search_frame, text="Search Medicine", command=search_medicine).pack(side=tk.LEFT, padx=5, pady=5)

print("Creating patient table...")
create_patient_table(connect_to_db())  # Create patient table when the program starts
print("Creating doctor table...")
create_doctor_table(connect_to_db())  # Create doctor table when the program starts
print("Creating medicine table...")
create_medicine_table(connect_to_db())  # Create medicine table when the program starts

root.mainloop()
