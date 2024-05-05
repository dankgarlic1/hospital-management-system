import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Function to connect to MySQL database
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="hospital"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error connecting to MySQL database: {err}")
        return None

# Function to create doctor table if not exists
def create_doctor_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctor (
            doctor_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            mobile_no VARCHAR(15),
            dob DATE,
            address VARCHAR(255),
            no_of_patients INT DEFAULT 0
        )
    """)
    conn.commit()
    cursor.close()
    print('water')

# Function to create patient table if not exists
def create_patient_table(conn):
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
            doctor_id INT,
            FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id)
        )
    """)
    conn.commit()
    cursor.close()

# Function to create medicine table if not exists
def create_medicine_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicine (
            medicine_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            doctor_id INT,
            patient_ids VARCHAR(255),
            quantity INT,
            price DECIMAL(10, 2),
            disease VARCHAR(255),
            FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id)
        )
    """)
    conn.commit()
    cursor.close()

# Function to add patient to database
def add_patient():
    name = name_entry_patient.get()
    address = address_entry_patient.get()
    mobile_no = mobile_no_entry_patient.get()
    age = int(age_entry_patient.get()) if age_entry_patient.get() else 0  # Convert age to integer
    dob = dob_entry_patient.get()
    disease = disease_entry_patient.get()
    doctor_id = int(doctor_id_entry_patient.get()) if doctor_id_entry_patient.get() else 0  # Convert doctor_id to integer

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patient (name, address, mobile_no, age, dob, disease, doctor_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, address, mobile_no, age, dob, disease, doctor_id))
        conn.commit()
        cursor.close()
        messagebox.showinfo("Success", "Patient added successfully.")
        clear_entries_patient()
        conn.close()

# Function to add doctor to database
def add_doctor():
    name = name_entry_doctor.get()
    mobile_no = mobile_no_entry_doctor.get()
    dob = dob_entry_doctor.get()
    address = address_entry_doctor.get()

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO doctor (name, mobile_no, dob, address) VALUES (%s, %s, %s, %s)", (name, mobile_no, dob, address))
        conn.commit()
        cursor.close()
        messagebox.showinfo("Success", "Doctor added successfully.")
        clear_entries_doctor()
        conn.close()

# Function to add medicine to database
def add_medicine():
    name = name_entry_medicine.get()
    doctor_id = int(doctor_id_entry_medicine.get()) if doctor_id_entry_medicine.get() else 0
    patient_ids = patient_ids_entry_medicine.get()
    quantity = int(quantity_entry_medicine.get()) if quantity_entry_medicine.get() else 0
    price = float(price_entry_medicine.get()) if price_entry_medicine.get() else 0.0
    disease = disease_entry_medicine.get()

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO medicine (name, doctor_id, patient_ids, quantity, price, disease) VALUES (%s, %s, %s, %s, %s, %s)", (name, doctor_id, patient_ids, quantity, price, disease))
        conn.commit()
        cursor.close()
        messagebox.showinfo("Success", "Medicine added successfully.")
        clear_entries_medicine()
        conn.close()

# Function to clear patient entry fields
def clear_entries_patient():
    name_entry_patient.delete(0, tk.END)
    address_entry_patient.delete(0, tk.END)
    mobile_no_entry_patient.delete(0, tk.END)
    age_entry_patient.delete(0, tk.END)
    dob_entry_patient.delete(0, tk.END)
    disease_entry_patient.delete(0, tk.END)
    doctor_id_entry_patient.delete(0, tk.END)

# Function to clear doctor entry fields
def clear_entries_doctor():
    name_entry_doctor.delete(0, tk.END)
    mobile_no_entry_doctor.delete(0, tk.END)
    dob_entry_doctor.delete(0, tk.END)
    address_entry_doctor.delete(0, tk.END)

# Function to clear medicine entry fields
def clear_entries_medicine():
    name_entry_medicine.delete(0, tk.END)
    doctor_id_entry_medicine.delete(0, tk.END)
    patient_ids_entry_medicine.delete(0, tk.END)
    quantity_entry_medicine.delete(0, tk.END)
    price_entry_medicine.delete(0, tk.END)
    disease_entry_medicine.delete(0, tk.END)

# Function to display all patient records
def display_patient_records():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patient")
        records = cursor.fetchall()
        display_records("Patient Records", records)
        conn.close()

# Function to display all doctor records
def display_doctor_records():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctor")
        records = cursor.fetchall()
        display_records("Doctor Records", records)
        conn.close()

# Function to display all medicine records
def display_medicine_records():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medicine")
        records = cursor.fetchall()
        display_records("Medicine Records", records)
        conn.close()

# Function to display records in a messagebox
def display_records(title, records):
    if records:
        record_str = ""
        for record in records:
            record_str += "\n" + " | ".join(map(str, record))
        messagebox.showinfo(title, record_str)
    else:
        messagebox.showinfo(title, "No records found.")

# GUI setup
root = tk.Tk()
root.title("Hospital Management System")
root.geometry("500x400")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Tabs
doctor_tab = ttk.Frame(notebook)
medicine_tab = ttk.Frame(notebook)
patient_tab = ttk.Frame(notebook)

notebook.add(doctor_tab, text='Doctors')
notebook.add(medicine_tab, text='Medicines')
notebook.add(patient_tab, text='Patients')

# Doctor Tab
doctor_id_label_doctor = tk.Label(doctor_tab, text="Doctor ID:")
doctor_id_label_doctor.grid(row=4, column=0, padx=10, pady=5)
doctor_id_entry_doctor = tk.Entry(doctor_tab)
doctor_id_entry_doctor.grid(row=4, column=1, padx=10, pady=5)

name_label_doctor = tk.Label(doctor_tab, text="Name:")
name_label_doctor.grid(row=0, column=0, padx=10, pady=5)
name_entry_doctor = tk.Entry(doctor_tab)
name_entry_doctor.grid(row=0, column=1, padx=10, pady=5)

mobile_no_label_doctor = tk.Label(doctor_tab, text="Mobile No:")
mobile_no_label_doctor.grid(row=1, column=0, padx=10, pady=5)
mobile_no_entry_doctor = tk.Entry(doctor_tab)
mobile_no_entry_doctor.grid(row=1, column=1, padx=10, pady=5)

dob_label_doctor = tk.Label(doctor_tab, text="DOB (YYYY-MM-DD):")
dob_label_doctor.grid(row=2, column=0, padx=10, pady=5)
dob_entry_doctor = tk.Entry(doctor_tab)
dob_entry_doctor.grid(row=2, column=1, padx=10, pady=5)

address_label_doctor = tk.Label(doctor_tab, text="Address:")
address_label_doctor.grid(row=3, column=0, padx=10, pady=5)
address_entry_doctor = tk.Entry(doctor_tab)
address_entry_doctor.grid(row=3, column=1, padx=10, pady=5)

doctor_id_label_doctor = tk.Label(doctor_tab, text="Doctor ID:")
doctor_id_label_doctor.grid(row=4, column=0, padx=10, pady=5)
doctor_id_entry_doctor = tk.Entry(doctor_tab)
doctor_id_entry_doctor.grid(row=4, column=1, padx=10, pady=5)

add_button_doctor = tk.Button(doctor_tab, text="Add Doctor", command=add_doctor)
add_button_doctor.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

# Patient Tab
name_label_patient = tk.Label(patient_tab, text="Name:")
name_label_patient.grid(row=0, column=0, padx=10, pady=5)
name_entry_patient = tk.Entry(patient_tab)
name_entry_patient.grid(row=0, column=1, padx=10, pady=5)

address_label_patient = tk.Label(patient_tab, text="Address:")
address_label_patient.grid(row=1, column=0, padx=10, pady=5)
address_entry_patient = tk.Entry(patient_tab)
address_entry_patient.grid(row=1, column=1, padx=10, pady=5)

mobile_no_label_patient = tk.Label(patient_tab, text="Mobile No:")
mobile_no_label_patient.grid(row=2, column=0, padx=10, pady=5)
mobile_no_entry_patient = tk.Entry(patient_tab)
mobile_no_entry_patient.grid(row=2, column=1, padx=10, pady=5)

age_label_patient = tk.Label(patient_tab, text="Age:")
age_label_patient.grid(row=3, column=0, padx=10, pady=5)
age_entry_patient = tk.Entry(patient_tab)
age_entry_patient.grid(row=3, column=1, padx=10, pady=5)

dob_label_patient = tk.Label(patient_tab, text="DOB (YYYY-MM-DD):")
dob_label_patient.grid(row=4, column=0, padx=10, pady=5)
dob_entry_patient = tk.Entry(patient_tab)
dob_entry_patient.grid(row=4, column=1, padx=10, pady=5)

disease_label_patient = tk.Label(patient_tab, text="Disease:")
disease_label_patient.grid(row=5, column=0, padx=10, pady=5)
disease_entry_patient = tk.Entry(patient_tab)
disease_entry_patient.grid(row=5, column=1, padx=10, pady=5)

doctor_id_label_patient = tk.Label(patient_tab, text="Doctor ID:")
doctor_id_label_patient.grid(row=6, column=0, padx=10, pady=5)
doctor_id_entry_patient = tk.Entry(patient_tab)
doctor_id_entry_patient.grid(row=6, column=1, padx=10, pady=5)

patient_id_label_patient = tk.Label(patient_tab, text="Patient ID:")
patient_id_label_patient.grid(row=7, column=0, padx=10, pady=5)
patient_id_entry_patient = tk.Entry(patient_tab)
patient_id_entry_patient.grid(row=7, column=1, padx=10, pady=5)

add_patient_button = tk.Button(patient_tab, text="Add Patient", command=add_patient)
add_patient_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

# Medicine Tab
name_label_medicine = tk.Label(medicine_tab, text="Name:")
name_label_medicine.grid(row=0, column=0, padx=10, pady=5)
name_entry_medicine = tk.Entry(medicine_tab)
name_entry_medicine.grid(row=0, column=1, padx=10, pady=5)

doctor_id_label_medicine = tk.Label(medicine_tab, text="Doctor ID:")
doctor_id_label_medicine.grid(row=1, column=0, padx=10, pady=5)
doctor_id_entry_medicine = tk.Entry(medicine_tab)
doctor_id_entry_medicine.grid(row=1, column=1, padx=10, pady=5)

patient_ids_label_medicine = tk.Label(medicine_tab, text="Patient IDs:")
patient_ids_label_medicine.grid(row=2, column=0, padx=10, pady=5)
patient_ids_entry_medicine = tk.Entry(medicine_tab)
patient_ids_entry_medicine.grid(row=2, column=1, padx=10, pady=5)

quantity_label_medicine = tk.Label(medicine_tab, text="Quantity:")
quantity_label_medicine.grid(row=3, column=0, padx=10, pady=5)
quantity_entry_medicine = tk.Entry(medicine_tab)
quantity_entry_medicine.grid(row=3, column=1, padx=10, pady=5)

price_label_medicine = tk.Label(medicine_tab, text="Price:")
price_label_medicine.grid(row=4, column=0, padx=10, pady=5)
price_entry_medicine = tk.Entry(medicine_tab)
price_entry_medicine.grid(row=4, column=1, padx=10, pady=5)

disease_label_medicine = tk.Label(medicine_tab, text="Disease:")
disease_label_medicine.grid(row=5, column=0, padx=10, pady=5)
disease_entry_medicine = tk.Entry(medicine_tab)
disease_entry_medicine.grid(row=5, column=1, padx=10, pady=5)

add_button_medicine = tk.Button(medicine_tab, text="Add Medicine", command=add_medicine)
add_button_medicine.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

# Display Records Buttons
display_records_button_doctor = tk.Button(doctor_tab, text="Display Records", command=display_doctor_records)
display_records_button_doctor.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

display_records_button_medicine = tk.Button(medicine_tab, text="Display Records", command=display_medicine_records)
display_records_button_medicine.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

display_records_button_patient = tk.Button(patient_tab, text="Display Records", command=display_patient_records)
display_records_button_patient.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

# Create tables
conn = connect_to_db()
if conn:
    create_doctor_table(conn)
    create_patient_table(conn)
    create_medicine_table(conn)
    conn.close()

root.mainloop()
