import pandas as pd
import streamlit as st
from sqlalchemy import text


def members_menu(engine):
    st.subheader("Members Menu")

    users_submenu = ["View Members", "Add Member", "Update Member", "Delete Member"]
    users_choice = st.sidebar.selectbox("Select Operation", users_submenu)

    if users_choice == "View Members":
        view_members(engine)

    elif users_choice == "Add Member":
        add_member(engine)

    elif users_choice == "Update Member":
        update_member(engine)

    elif users_choice == "Delete Member":
        delete_member(engine)


def view_members(engine):
    members_df = pd.read_sql_query("SELECT * FROM MEMBER", engine)
    st.dataframe(members_df)


def add_member(engine):
    house_rules = st.text_area("House Rules")

    if st.button("Add Member"):
        try:
            with engine.connect() as connection:
                query = text("INSERT INTO MEMBER (house_rules) VALUES (:house_rules)")
                connection.execute(query, {"house_rules": house_rules})
                connection.commit()

            st.success("Member added successfully.")

        except Exception as e:
            st.error(f"Error adding member: {e}")


def update_member(engine):
    member_user_id = st.number_input("Enter Member User ID to update", min_value=1)
    field_to_update = st.selectbox("Select field to update", ["house_rules"])
    new_value = st.text_area(f"Enter new {field_to_update}")

    if st.button("Update Member"):
        try:
            with engine.connect() as connection:
                query = text(f"UPDATE MEMBER SET {field_to_update} = :new_value WHERE member_user_id = :member_user_id")
                connection.execute(query, {"new_value": new_value, "member_user_id": member_user_id})
                connection.commit()

            st.success("Member updated successfully.")

        except Exception as e:
            st.error(f"Error updating member: {e}")


def delete_member(engine):
    member_user_id = st.number_input("Enter Member User ID to delete", min_value=1)

    if st.button("Delete Member"):
        try:
            with engine.connect() as connection:
                query = text("DELETE FROM MEMBER WHERE member_user_id = :member_user_id")
                connection.execute(query, {"member_user_id": member_user_id})
                connection.commit()

            st.success("Member deleted successfully.")

        except Exception as e:
            st.error(f"Error deleting member: {e}")
