import pandas as pd
import streamlit as st
from sqlalchemy import text

def jobs_menu(engine):
    st.subheader("Jobs Menu")

    jobs_submenu = ["View Jobs", "Add Job", "Update Job", "Delete Job"]
    jobs_choice = st.sidebar.selectbox("Select Operation", jobs_submenu)

    if jobs_choice == "View Jobs":
        view_jobs(engine)

    elif jobs_choice == "Add Job":
        add_job(engine)

    elif jobs_choice == "Update Job":
        update_job(engine)

    elif jobs_choice == "Delete Job":
        delete_job(engine)


def view_jobs(engine):
    jobs_df = pd.read_sql_query("SELECT * FROM JOB", engine)
    st.dataframe(jobs_df)


def add_job(engine):
    member_user_id = st.number_input("Member User ID")
    required_caregiving_type = st.text_input("Required Caregiving Type")
    other_requirements = st.text_area("Other Requirements")
    date_posted = st.date_input("Date Posted")

    if st.button("Add Job"):
        try:
            with engine.connect() as connection:
                query = text(
                    "INSERT INTO JOB (member_user_id, required_caregiving_type, other_requirements, date_posted) "
                    "VALUES (:member_user_id, :required_caregiving_type, :other_requirements, :date_posted)")
                connection.execute(query, {"member_user_id": member_user_id,
                                           "required_caregiving_type": required_caregiving_type,
                                           "other_requirements": other_requirements,
                                           "date_posted": date_posted})
                connection.commit()

            st.success("Job added successfully.")

        except Exception as e:
            st.error(f"Error adding job: {e}")

def update_job(engine):
    job_id = st.number_input("Enter Job ID to update", min_value=1)
    field_to_update = st.selectbox("Select field to update",
                                   ["member_user_id", "required_caregiving_type", "other_requirements", "date_posted"])
    new_value = st.text_input(f"Enter new {field_to_update}")

    if st.button("Update Job"):
        try:
            with engine.connect() as connection:
                query = text(f"UPDATE JOB SET {field_to_update} = :new_value WHERE job_id = :job_id")
                connection.execute(query, {"new_value": new_value, "job_id": job_id})
                connection.commit()

            st.success("Job updated successfully.")

        except Exception as e:
            st.error(f"Error updating job: {e}")

def delete_job(engine):
    job_id = st.number_input("Enter Job ID to delete", min_value=1)

    if st.button("Delete Job"):
        try:
            with engine.connect() as connection:
                query = text("DELETE FROM JOB WHERE job_id = :job_id")
                connection.execute(query, {"job_id": job_id})
                connection.commit()

            st.success("Job deleted successfully.")

        except Exception as e:
            st.error(f"Error deleting job: {e}")