import pandas as pd
import streamlit as st
from sqlalchemy import text


def appointments_menu(engine):
    st.subheader("Appointments Menu")

    appointments_submenu = ["View Appointments", "Add Appointment", "Update Appointment", "Delete Appointment"]
    appointments_choice = st.sidebar.selectbox("Select Operation", appointments_submenu)

    if appointments_choice == "View Appointments":
        view_appointments(engine)

    elif appointments_choice == "Add Appointment":
        add_appointment(engine)

    elif appointments_choice == "Update Appointment":
        update_appointment(engine)

    elif appointments_choice == "Delete Appointment":
        delete_appointment(engine)


def view_appointments(engine):
    appointments_df = pd.read_sql_query("SELECT * FROM APPOINTMENT", engine)
    st.dataframe(appointments_df)


def add_appointment(engine):
    caregiver_user_id = st.number_input("Caregiver User ID")
    member_user_id = st.number_input("Member User ID")
    appointment_date = st.date_input("Appointment Date")
    appointment_time = st.time_input("Appointment Time")
    work_hours = st.number_input("Work Hours", min_value=0.0)
    status = st.text_input("Status")

    if st.button("Add Appointment"):
        try:
            with engine.connect() as connection:
                query = text("INSERT INTO APPOINTMENT (caregiver_user_id, member_user_id, appointment_date, "
                             "appointment_time, work_hours, status) "
                             "VALUES (:caregiver_user_id, :member_user_id, :appointment_date, "
                             ":appointment_time, :work_hours, :status)")
                connection.execute(query, {"caregiver_user_id": caregiver_user_id,
                                           "member_user_id": member_user_id,
                                           "appointment_date": str(appointment_date),
                                           "appointment_time": str(appointment_time),
                                           "work_hours": work_hours,
                                           "status": status})
                connection.commit()

            st.success("Appointment added successfully.")

        except Exception as e:
            st.error(f"Error adding appointment: {e}")


def update_appointment(engine):
    appointment_id = st.number_input("Enter Appointment ID to update", min_value=1)
    field_to_update = st.selectbox("Select field to update",
                                   ["caregiver_user_id", "member_user_id", "appointment_date",
                                    "appointment_time", "work_hours", "status"])
    new_value = st.text_input(f"Enter new {field_to_update}")

    if st.button("Update Appointment"):
        try:
            with engine.connect() as connection:
                query = text(
                    f"UPDATE APPOINTMENT SET {field_to_update} = :new_value WHERE appointment_id = :appointment_id")
                connection.execute(query, {"new_value": new_value, "appointment_id": appointment_id})
                connection.commit()

            st.success("Appointment updated successfully.")

        except Exception as e:
            st.error(f"Error updating appointment: {e}")


def delete_appointment(engine):
    appointment_id = st.number_input("Enter Appointment ID to delete", min_value=1)

    if st.button("Delete Appointment"):
        try:
            with engine.connect() as connection:
                query = text("DELETE FROM APPOINTMENT WHERE appointment_id = :appointment_id")
                connection.execute(query, {"appointment_id": appointment_id})
                connection.commit()

            st.success("Appointment deleted successfully.")

        except Exception as e:
            st.error(f"Error deleting appointment: {e}")
