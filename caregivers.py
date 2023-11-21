import pandas as pd
import streamlit as st
from sqlalchemy import text


def caregivers_menu(engine):
    st.subheader("Caregivers Menu")

    caregivers_submenu = ["View Caregivers", "Add Caregiver", "Update Caregiver", "Delete Caregiver"]
    caregivers_choice = st.sidebar.selectbox("Select Operation", caregivers_submenu)

    if caregivers_choice == "View Caregivers":
        view_caregivers(engine)

    elif caregivers_choice == "Add Caregiver":
        add_caregiver(engine)

    elif caregivers_choice == "Update Caregiver":
        update_caregiver(engine)

    elif caregivers_choice == "Delete Caregiver":
        delete_caregiver(engine)


def view_caregivers(engine):
    caregivers_df = pd.read_sql_query("SELECT * FROM caregiver", engine)
    st.dataframe(caregivers_df)


def add_caregiver(engine):
    photo = st.text_input("Photo URL")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    caregiving_type = st.text_input("Caregiving Type")
    hourly_rate = st.number_input("Hourly Rate", min_value=0.0)

    if st.button("Add Caregiver"):
        try:
            with engine.connect() as connection:
                query = text(
                    "INSERT INTO caregiver (photo, gender, caregiving_type, hourly_rate) "
                    "VALUES (:photo, :gender, :caregiving_type, :hourly_rate)")
                connection.execute(query, {"photo": photo, "gender": gender,
                                           "caregiving_type": caregiving_type, "hourly_rate": hourly_rate})
                connection.commit()

            st.success("Caregiver added successfully.")

        except Exception as e:
            st.error(f"Error adding caregiver: {e}")


def update_caregiver(engine):
    caregiver_user_id = st.number_input("Enter Caregiver User ID to update", min_value=1)
    field_to_update = st.selectbox("Select field to update", ["photo", "gender", "caregiving_type", "hourly_rate"])
    new_value = st.text_input(f"Enter new {field_to_update}")

    if st.button("Update Caregiver"):
        try:
            with engine.connect() as connection:
                query = text(
                    f"UPDATE caregiver SET {field_to_update} = :new_value WHERE caregiver_user_id = :caregiver_user_id")
                connection.execute(query, {"new_value": new_value, "caregiver_user_id": caregiver_user_id})
                connection.commit()

            st.success("Caregiver updated successfully.")

        except Exception as e:
            st.error(f"Error updating caregiver: {e}")


def delete_caregiver(engine):
    caregiver_user_id = st.number_input("Enter Caregiver User ID to delete", min_value=1)

    if st.button("Delete Caregiver"):
        try:
            with engine.connect() as connection:
                query = text("DELETE FROM caregiver WHERE caregiver_user_id = :caregiver_user_id")
                connection.execute(query, {"caregiver_user_id": caregiver_user_id})
                connection.commit()

            st.success("Caregiver deleted successfully.")

        except Exception as e:
            st.error(f"Error deleting caregiver: {e}")
