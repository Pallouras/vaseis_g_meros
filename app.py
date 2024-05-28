import streamlit as st
import mysql.connector
import pandas as pd
import requests
from streamlit_lottie import st_lottie
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'port': 4306,  # Update the port number to 3305 because in installation i gave port 3305
    'database':'ergasia2'
}

def loti(url):
    r = requests.get(url)
    if r.status_code != 200:
       return None
    else:
        return r.json()
def create_connection():
    """Create a connection to the MySQL database."""
    db = mysql.connector.connect(**config)
    return db

def create_database(db):
    """Create the 'ergasia2' database if it doesn't exist."""
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ergasia2")
    cursor.close()

def create_patient_table(db):
    """Create the patient table in the database."""
    cursor = db.cursor()

    create_patient_table_query = """
    CREATE TABLE IF NOT EXISTS patient (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        birth_date DATE,
        mobile_phone VARCHAR,
        address_line_1 VARCHAR(255),
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMPCHAR(20),
        email VARCHAR(255),
    )
    """

    cursor.execute(create_patient_table_query)
    db.commit()
    st.write("Patient table created successfully.")

def modify_patient_table(db):
    cursor = db.cursor()

    alter_table_query = """
    ALTER TABLE patient
    ADD COLUMN doctor_name VARCHAR(255),
    ADD COLUMN doctor_id INT,
    ADD COLUMN disease VARCHAR(255),
    ADD COLUMN fee INTEGER(5),
    ADD COLUMN tests VARCHAR(255),
    ADD COLUMN cnic VARCHAR(20)
    """

    cursor.execute(alter_table_query)
    db.commit()
    st.write("Patient table modified successfully.")



def create_appointments_table(db):
    """Create the appointments table in the database."""
    cursor = db.cursor()

    create_appointments_table_query = """
    CREATE TABLE IF NOT EXISTS appointments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        patient_id INT,
        appointment_date DATE,
        appointment_time TIME,
        doctor_name VARCHAR(255),
        doctor_id INT,
        notes TEXT,
        FOREIGN KEY (patient_id) REFERENCES patient(id)
    )
    """



def insert_patient_record(db, name, birth_date, mobile_phone, email, address_line_1):
    """Insert a new patient record into the 'patient' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE ergasia2")

    insert_patient_query = """
    INSERT INTO patient (name, birth_date, mobile_phone, email, address_line_1)
    VALUES (%s, %s, %s, %s, %s)
    """

    patient_data = (name, birth_date, mobile_phone, email, address_line_1)

    cursor.execute(insert_patient_query, patient_data)
    db.commit()
    st.write("Patient record inserted successfully.") 

def fetch_all_patient(db):
    """Fetch all records from the 'patient' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE ergasia2")

    # Fetch all patient
    select_patient_query = "SELECT * FROM patient"
    cursor.execute(select_patient_query)
    patient = cursor.fetchall()

    return patient       

def fetch_patient_by_id(db, patient_id):
    """Fetch a patient's record from the 'patient' table based on ID."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE ergasia2")

    # Fetch the patient by ID
    select_patient_query = "SELECT * FROM patient WHERE id = %s"
    cursor.execute(select_patient_query, (patient_id,))
    patient = cursor.fetchone()

    return patient

def fetch_patient_by_contact(db, mobile_phone):
    """Fetch a patient's record from the 'patient' table based on mobile phone."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE ergasia2")

    # Fetch the patient by contact number
    select_patient_query = "SELECT * FROM patient WHERE mobile_phone = %s"
    cursor.execute(select_patient_query, (mobile_phone,))
    patient = cursor.fetchone()

    return patient


def fetch_patient_by_cnis(db, cnis):
    """Fetch a patient's record from the 'patient' table based on CNIS."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE ergasia2")

    # Fetch the patient by CNIS
    select_patient_query = "SELECT * FROM patient WHERE cnis = %s"
    cursor.execute(select_patient_query, (cnis,))
    patient = cursor.fetchone()

    return patient

     

def delete_patient_record(db, delete_option, delete_value):
    """Delete a patient record from the 'patient' table based on ID, name, or contact number."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE ergasia2")

    # Delete the patient record
    if delete_option == "ID":
        delete_patient_query = "DELETE FROM patient WHERE id = %s"
    elif delete_option == "Name":
        delete_patient_query = "DELETE FROM patient WHERE name = %s"
    elif delete_option == "Contact Number":
        delete_patient_query = "DELETE FROM patient WHERE mobile_phone = %s"

    cursor.execute(delete_patient_query, (delete_value,))
    db.commit()
    st.write("Patient record deleted successfully.")

def insert_appointment_record(db, patient_id, appointment_date, appointment_time, doctor_name, notes,doctor_id):
    """Insert a new appointment record into the 'appointments' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE ergasia2")
    appointment_time = appointment_time.strftime("%H:%M:%S")
    appointment_date = appointment_date.strftime("%Y-%m-%d")
    insert_appointment_query = """
    INSERT INTO appointments (patient_id, appointment_date, appointment_time, doctor_name,doctor_id, notes)
    VALUES (%s, %s, %s, %s, %s)
    """

    appointment_data = (patient_id, appointment_date, appointment_time, doctor_name,doctor_id, notes)

    cursor.execute(insert_appointment_query, appointment_data)
    db.commit()
    print("Appointment record inserted successfully.")


def fetch_all_appointments(db):
    """Fetch all records from the 'appointments' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE ergasia2")

    # Fetch all appointments
    select_appointments_query = """
    SELECT id, patient_id, DATE_FORMAT(appointment_date, '%Y-%m-%d') AS appointment_date, 
           appointment_time, doctor_name, notes
    FROM appointments
    """
    cursor.execute(select_appointments_query)
    appointments = cursor.fetchall()

    return appointments

def show_all_appointments(db):
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE ergasia2")
    select_query = """
    SELECT id, patient_id, appointment_date, CAST(appointment_time AS CHAR), doctor_name, notes FROM appointments
    """
    cursor.execute(select_query)
    records = cursor.fetchall()

    if records:
        st.subheader("All Appointment Records")
        df = pd.DataFrame(records, columns=['ID', 'Patient ID', 'Appointment Date', 'Appointment Time', 'Doctor Name', 'Notes'])
        st.dataframe(df)
    else:
        st.write("No appointments found")           

def edit_appointment_record(db, appointment_id, new_appointment_date, new_appointment_time, new_doctor_name, new_notes):
    """Edit an appointment record in the 'appointments' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE ergasia2")

    # Update the appointment record
    update_appointment_query = """
    UPDATE appointments
    SET appointment_date = %s, appointment_time = CAST(%s AS TIME), doctor_name = %s, notes = %s
    WHERE id = %s
    """
    appointment_data = (new_appointment_date, new_appointment_time, new_doctor_name, new_notes, appointment_id)

    cursor.execute(update_appointment_query, appointment_data)
    db.commit()
    

def fetch_appointment_by_id(db, appointment_id):
    """Fetch an appointment's record from the 'appointments' table based on ID."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE ergasia2")

    # Fetch the appointment by ID
    select_appointment_query = """
       SELECT id, patient_id, appointment_date, CAST(appointment_time AS CHAR), doctor_name, notes
       FROM appointments
       WHERE id = %s
       """
    cursor.execute(select_appointment_query, (appointment_id,))
    appointment = cursor.fetchone()

    return appointment  


def fetch_appointment_by_patient_id(db, patient_id):

    query = """
    SELECT id, patient_id, appointment_date, CAST(appointment_time AS CHAR), doctor_name, notes
    FROM appointments
    WHERE patient_id = %s
    """
    cursor = db.cursor()
    cursor.execute("USE ergasia2")
    cursor.execute(query, (patient_id,))
    appointment = cursor.fetchone()
    #cursor.close()
    return appointment  


def fetch_appointment_by_doctor_name(db, doctor_name):
    query = """
    SELECT id, patient_id, appointment_date, CAST(appointment_time AS CHAR), doctor_name, notes
    FROM appointments
    WHERE doctor_name = %s
    """
    cursor = db.cursor()
    cursor.execute("USE ergasia2")
    cursor.execute(query, (doctor_name,))
    appointment = cursor.fetchone()
    #cursor.close()
    return appointment        


def search_appointment(db):
    search_option = st.selectbox("Select search option", ["ID", "Patient ID", "Doctor Name"],key="search_option")
    search_value = st.text_input("Enter search value",key="search_value")

    if st.button("Search"):
        if search_option == "ID":
            appointment = fetch_appointment_by_id(db, search_value)
        elif search_option == "Patient ID":
            appointment = fetch_appointment_by_patient_id(db, search_value)
        elif search_option == "Doctor Name":
            appointment = fetch_appointment_by_doctor_name(db, search_value)

        if appointment:
            st.subheader("Appointment Details")
            df = pd.DataFrame([appointment], columns=['ID', 'Patient ID', 'Appointment Date', 'Appointment Time', 'Doctor Name', 'Notes'])
            st.dataframe(df)
            st.session_state.edit_appointment = appointment
        else:
            st.write("Appointment not found")
    if 'edit_appointment' in st.session_state:
        edit_appointment(db)        

def edit_appointment(db):
    #if 'edit_appointment' in st.session_state:
        appointment = st.session_state.edit_appointment
        st.subheader("Edit Appointment Details")
        new_appointment_date = st.date_input("Appointment Date", value=appointment[2])
        new_appointment_time = st.text_input("Appointment Time", value=appointment[3])
        new_doctor_name = st.text_input("Doctor Name", value=appointment[4])
        new_notes = st.text_input("Notes", value=appointment[5])

        if st.button("Update Appointment"):
            edit_appointment_record(db, appointment[0], new_appointment_date, new_appointment_time, new_doctor_name, new_notes)
            st.write("Appointment record updated successfully.")
            del st.session_state.edit_appointment

def update_patient_record(db):
    """Update a patient's record in the 'patient' table."""

    search_option = st.selectbox("Select search option", ["ID", "Contact Number", "CNIS"], key="search_option")
    search_value = st.text_input("Enter search value", key="search_value")

    if st.button("Search :magic_wand:"):
        if search_option == "ID":
            patient = fetch_patient_by_id(db, search_value)
        elif search_option == "Contact Number":
            patient = fetch_patient_by_contact(db, search_value)
        elif search_option == "CNIS":
            patient = fetch_patient_by_cnis(db, search_value)

        if patient:
            st.subheader("Patient Details")
            df = pd.DataFrame([patient], columns=['ID', 'Name', 'Birth Date', 'Contact Number', 'Email', 'Address', 'Date Added'])
            st.dataframe(df)
            st.session_state.edit_patient = patient
        else:
            st.write("Patient not found")

    if 'edit_patient' in st.session_state:
        edit_patient(db)


def edit_patient(db):
    """Edit a patient's record in the '' table."""

    st.subheader("Edit Patient Details")
    new_name = st.text_input("Enter new name", value=st.session_state.edit_patient[1])
    new_birth_date = st.number_input("Enter new birth date", value=st.session_state.edit_patient[2])
    new_contact = st.text_input("Enter new contact number", value=st.session_state.edit_patient[3])
    new_email = st.text_input("Enter new email", value=st.session_state.edit_patient[4])
    new_address_line_1 = st.text_input("Enter new address", value=st.session_state.edit_patient[5])

    if st.button("Update :roller_coaster:"):
        patient_id = st.session_state.edit_patient[0]
        update_patient_info(db, patient_id, new_name, new_birth_date, new_contact, new_email, new_address_line_1)
        


def update_patient_info(db, patient_id, new_name, new_birth_date, new_contact, new_email, new_address_line_1):
    """Update a patient's record in the 'patient' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE ergasia2")

    # Update the patient record
    update_patient_query = """
    UPDATE patient
    SET name = %s, birth_date = %s, mobile_phone = %s, email = %s, address_line_1 = %s
    WHERE id = %s
    """
    patient_data = (new_name, new_birth_date, new_contact, new_email, new_address_line_1, patient_id)

    cursor.execute(update_patient_query, patient_data)
    db.commit()
    st.write("Patient record updated successfully.")


##custom
def get_doctors_and_periods_for_patient(db, patient_name):
    query = """
    SELECT 
        CONCAT(D.first_name, ' ', D.last_name) AS doctor_name,
        DP.relation_start_date,
        DP.relation_end_date
    FROM 
        DOCTOR_PATIENT DP
    JOIN 
        DOCTOR D ON DP.doctor_id = D.doctor_id
    JOIN 
        PATIENT P ON DP.patient_id = P.patient_id
    WHERE 
        P.name = %s;
    """
    cursor = db.cursor()
    cursor.execute("USE ergasia2")
    cursor.execute(query, (patient_name,))
    result = cursor.fetchall()
    return result


def get_medicines_prescribed_to_patient(db, patient_name):
    query = """
    SELECT 
        P.name AS patient_name,
        CONCAT(D.first_name, ' ', D.last_name) AS doctor_name,
        M.medicine_name,
        PVH.visit_type
    FROM 
        PRESCRIPTION PR
    JOIN 
        PATIENT P ON PR.patient_id = P.patient_id
    JOIN 
        DOCTOR D ON PR.doctor_id = D.doctor_id
    JOIN 
        PRESCRIPTION_MEDICINE PM ON PR.prescription_id = PM.prescription_id
    JOIN 
        MEDICINE M ON PM.medicine_id = M.medicine_id
    JOIN 
        PATIENT_VISIT_HISTORY PVH ON PR.patient_id = PVH.patient_id
    WHERE 
        P.name = %s;
    """
    cursor = db.cursor()
    cursor.execute("USE ergasia2")
    cursor.execute(query, (patient_name,))
    result = cursor.fetchall()
    return result


def get_all_visits_for_patient_to_doctor(db, patient_name, doctor_name):
    query = """
    SELECT 
        PVH.visit_id,
        PVH.visit_date,
        PVH.visit_type,
        P.name AS patient_name,
        CONCAT(D.first_name, ' ', D.last_name) AS doctor_name
    FROM 
        PATIENT_VISIT_HISTORY PVH
    JOIN 
        PATIENT P ON PVH.patient_id = P.patient_id
    JOIN 
        DOCTOR D ON PVH.doctor_id = D.doctor_id
    WHERE 
        P.name = %s
        AND CONCAT(D.first_name, ' ', D.last_name) = %s;
    """
    cursor = db.cursor()
    cursor.execute("USE ergasia2")
    cursor.execute(query, (patient_name, doctor_name))
    result = cursor.fetchall()
    return result

def get_doctors_and_hospitals(db):
    query = """
    SELECT 
        CONCAT(D.first_name, ' ', D.last_name) AS doctor_name,
        D.specialization,
        MC.name AS medical_center_name,
        MC.city AS medical_center_area
    FROM 
        DOCTOR_MEDICAL_CENTER DMC
    JOIN 
        DOCTOR D ON DMC.doctor_id = D.doctor_id
    JOIN 
        MEDICAL_CENTER MC ON DMC.center_id = MC.center_id;
    """
    cursor = db.cursor()
    cursor.execute("USE ergasia2")
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def get_mean_test_values_for_patient(db, patient_name):
    query = """
    SELECT 
        AVG(CAST(REGEXP_SUBSTR(RV.blood_pressure, '^\d+') AS UNSIGNED)) AS mean_systolic_pressure,
        AVG(CAST(REGEXP_SUBSTR(RV.blood_pressure, '\d+$') AS UNSIGNED)) AS mean_diastolic_pressure,
        AVG(CAST(REGEXP_SUBSTR(RV.height, '^\d+\.\d+') AS DECIMAL(10, 2))) AS mean_height,
        AVG(CAST(REGEXP_SUBSTR(RV.weight, '^\d+') AS DECIMAL(10, 2))) AS mean_weight
    FROM 
        ROUTINE_VISIT RV
    JOIN 
        PATIENT P ON RV.visit_id = P.patient_id
    WHERE 
        P.name = %s;
    """
    cursor = db.cursor()
    cursor.execute("USE ergasia2")
    cursor.execute(query, (patient_name,))
    result = cursor.fetchall()
    return result






def main():
    # Title and sidebar
    st.title("Patient Management System :hospital:")
    lott1 = loti( "https://assets6.lottiefiles.com/packages/lf20_olluraqu.json")
    lotipatient = loti("https://assets6.lottiefiles.com/packages/lf20_vPnn3K.json")
    db = create_connection()

    #create_database(db)

    #config['database'] = 'userdb'  # Update the database name
    #db = create_connection()

    #create_patient_table(db)
    #create_appointments_table(db)
    #modify_patient_table(db)

    menu = ["Home","Add patient Record","Show patiet Records", "Search and Edit Patient","Deetel Patient Record",
            "Add patient Appointments","Show All Appointments","Search and Edit Patient Appointments","View Doctor Details","Query Reports"]
    options = st.sidebar.radio("Select an Option :dart:",menu)
    if options== "Home":
        st.subheader("Welcome to Hospital Mnagement System")
        st.write("Navigate from sidebar to access database")
        st_lottie(lott1,height=500)
        #st.image('hospital.jpg', width=600)

    elif options == "Add patient Record":
       st.subheader("Enter patient details :woman_in_motorized_wheelchair:")
       st_lottie(lotipatient,height = 200)
       name = st.text_input("Enter name of patient",key = "name")
       birth_date = st.number_input("Enter birth date of patient",key = "birth_date",value = 1)
       contact = st.text_input("Enter contact of patient",key = "contact")
       email = st.text_input("Enter Email of patient",key = "email")
       address_line_1 = st.text_input("Enter Address of patient",key= "address_line_1")
       if st.button("add patient record"):
          cursor = db.cursor()
          select_query = """
          SELECT * FROM patient WHERE mobile_phone=%s
          """
          cursor.execute(select_query,(contact,))
          existing_patient = cursor.fetchone()
          if existing_patient:
            st.warning("A patient with the same contact number already exist")
          else:  
            insert_patient_record(db, name, birth_date, contact, email, address_line_1)

    elif options=="Show patiet Records":
        patient = fetch_all_patient(db)
        if patient:
            st.subheader("All patient Records :magic_wand:")
            df = pd.DataFrame(patient, columns=['ID', 'Name', 'Birth Date','Gender', 'Contact Number', 'Email', 'Address 1','Address 2','City' 'Postal Code',
                                                'Country','Work Phone','Home Phone','Emergency Contact Person','Emergency Contact Phone','Insurance ID','Insurance Owner','Date Added','Patient Owner Relation'])
            st.dataframe(df)
        else:
            st.write("No patient found")
    elif options == "Search and Edit Patient":
         update_patient_record(db)
           

    elif options == "Deetel Patient Record":
         st.subheader("Search a patient to delate :skull_and_crossbones:")
         delete_option = st.selectbox("Select delete option", ["ID", "Name", "Contact Number"], key="delete_option")
         delete_value = st.text_input("Enter delete value", key="delete_value")

         if st.button("Delete"):
            delete_patient_record(db, delete_option, delete_value)

    elif options == "Add patient Appointments":
          patient_id = st.number_input("Enter patient ID:", key="appointment_patient_id")
          appointment_date = st.date_input("Enter appointment date:", key="appointment_date")
          appointment_time = st.time_input("Enter appointment time:", key="appointment_time")
          doctor_name = st.text_input("Enter doctor's name:", key="appointment_doctor_name")
          notes = st.text_area("Enter appointment notes:", key="appointment_notes")

          if st.button("Add Appointment"):
               insert_appointment_record(db, patient_id, appointment_date, appointment_time, doctor_name, notes)
               st.write("Appointment record added successfully.")    
    
    #custom
    elif options == "Query Reports":
        st.subheader("Query Reports")
    query_option = st.selectbox("Select Query", [
        "Doctors and Periods for Patient",
        "Medicines Prescribed to Patient",
        "All Visits of Patient to Doctor",
        "Doctor and Hospital Info",
        "Average Test Values of Patient"
    ])

    if query_option == "Doctors and Periods for Patient":
        patient_name = st.text_input("Enter patient's name")
        if st.button("Fetch Data"):
            results = get_doctors_and_periods_for_patient(db, patient_name)
            if results:
                df = pd.DataFrame(results, columns=['Doctor Name', 'Relation Start Date', 'Relation End Date'])
                st.dataframe(df)
            else:
                st.write("No data found for the given patient name.")

    elif query_option == "Medicines Prescribed to Patient":
        patient_name = st.text_input("Enter patient's name")
        if st.button("Fetch Data"):
            results = get_medicines_prescribed_to_patient(db, patient_name)
            if results:
                df = pd.DataFrame(results, columns=['Patient Name', 'Doctor Name', 'Medicine Name', 'Visit Type'])
                st.dataframe(df)
            else:
                st.write("No data found for the given patient name.")

    elif query_option == "All Visits of Patient to Doctor":
        patient_name = st.text_input("Enter patient's name")
        doctor_name = st.text_input("Enter doctor's name")
        if st.button("Fetch Data"):
            results = get_all_visits_for_patient_to_doctor(db, patient_name, doctor_name)
            if results:
                df = pd.DataFrame(results, columns=['Visit ID', 'Visit Date', 'Visit Type', 'Patient Name', 'Doctor Name'])
                st.dataframe(df)
            else:
                st.write("No data found for the given patient and doctor name.") 

    elif query_option == "Doctor and Hospital Info":
        if st.button("Fetch Data"):
            results = get_doctors_and_hospitals(db)
            if results:
                df = pd.DataFrame(results, columns=['Doctor Name', 'Specialization', 'Medical Center Name', 'Medical Center Area'])
                st.dataframe(df)
            else:
                st.write("No data found.") 

    elif query_option == "Average Test Values of Patient":
        patient_name = st.text_input("Enter patient's name")
        if st.button("Fetch Data"):
            results = get_mean_test_values_for_patient(db, patient_name)
            if results:
                df = pd.DataFrame(results, columns=['Mean Systolic Pressure', 'Mean Diastolic Pressure', 'Mean Height', 'Mean Weight'])
                st.dataframe(df)
            else:
                st.write("No data found for the given patient name.")                       
      

    db.close()

if __name__ == "__main__":
    main()
