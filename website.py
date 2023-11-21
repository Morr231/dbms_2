import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

import users
import members
import addresses
import caregivers
import jobs
import job_applications
import appointments
import os
load_dotenv()


DATABASE_URI = os.environ.get("DATABASE_URI")
engine = create_engine(DATABASE_URI)
st.set_page_config(page_title="DBMS 2 assignment", layout="wide", initial_sidebar_state="expanded")


def main():
    st.title("DBMS 2 assignment")

    menu = ["Users",
            "Caregivers",
            "Members",
            "Addresses",
            "Jobs",
            "Job Applications",
            "Appointments"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Users":
        users.users_menu(engine)

    elif choice == "Caregivers":
        caregivers.caregivers_menu(engine)

    elif choice == "Members":
        members.members_menu(engine)

    elif choice == "Addresses":
        addresses.address_menu(engine)

    elif choice == "Jobs":
        jobs.jobs_menu(engine)

    elif choice == "Job Applications":
        job_applications.job_applications_menu(engine)

    elif choice == "Appointments":
        appointments.appointments_menu(engine)


if __name__ == "__main__":
    print(os.environ.get("DATABASE_URI"))
    main()
