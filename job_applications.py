import pandas as pd
import streamlit as st
from sqlalchemy import text


def job_applications_menu(engine):
    st.subheader("Job Applications Menu")

    job_applications_submenu = ["View Job Applications", "Add Job Application", "Delete Job Application"]
    job_applications_choice = st.sidebar.selectbox("Select Operation", job_applications_submenu)

    if job_applications_choice == "View Job Applications":
        view_job_applications(engine)

    elif job_applications_choice == "Add Job Application":
        add_job_application(engine)

    elif job_applications_choice == "Delete Job Application":
        delete_job_application(engine)


def view_job_applications(engine):
    job_applications_df = pd.read_sql_query("SELECT * FROM JOB_APPLICATION", engine)
    st.dataframe(job_applications_df)


def add_job_application(engine):
    caregiver_user_id = st.number_input("Caregiver User ID")
    job_id = st.number_input("Job ID")
    date_applied = st.date_input("Date Applied")

    if st.button("Add Job Application"):
        try:
            with engine.connect() as connection:
                query = text("INSERT INTO JOB_APPLICATION (caregiver_user_id, job_id, date_applied) "
                             "VALUES (:caregiver_user_id, :job_id, :date_applied)")
                connection.execute(query, {"caregiver_user_id": caregiver_user_id,
                                           "job_id": job_id,
                                           "date_applied": date_applied})
                connection.commit()

            st.success("Job Application added successfully.")

        except Exception as e:
            st.error(f"Error adding job application: {e}")


def update_job_application(engine):
    caregiver_user_id = st.number_input("Enter Caregiver User ID for Job Application to update", min_value=1)
    job_id = st.number_input("Enter Job ID for Job Application to update", min_value=1)
    new_date_applied = st.date_input("Enter new Date Applied")

    if st.button("Update Job Application"):
        try:
            with engine.connect() as connection:
                query = text("UPDATE JOB_APPLICATION SET date_applied = :new_date_applied "
                             "WHERE caregiver_user_id = :caregiver_user_id AND job_id = :job_id")
                connection.execute(query, {"new_date_applied": new_date_applied,
                                           "caregiver_user_id": caregiver_user_id,
                                           "job_id": job_id})
                connection.commit()

            st.success("Job Application updated successfully.")

        except Exception as e:
            st.error(f"Error updating job application: {e}")


def delete_job_application(engine):
    caregiver_user_id = st.number_input("Enter Caregiver User ID for Job Application to delete", min_value=1)
    job_id = st.number_input("Enter Job ID for Job Application to delete", min_value=1)

    if st.button("Delete Job Application"):
        try:
            with engine.connect() as connection:
                query = text(
                    "DELETE FROM JOB_APPLICATION WHERE caregiver_user_id = :caregiver_user_id AND job_id = :job_id")
                connection.execute(query, {"caregiver_user_id": caregiver_user_id, "job_id": job_id})
                connection.commit()

            st.success("Job Application deleted successfully.")

        except Exception as e:
            st.error(f"Error deleting job application: {e}")
