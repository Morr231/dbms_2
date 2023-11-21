import pandas as pd
import streamlit as st
from sqlalchemy import text


def users_menu(engine):
    st.subheader("Users Menu")

    users_submenu = ["View Users", "Add User", "Update User", "Delete User"]
    users_choice = st.sidebar.selectbox("Select Operation", users_submenu)

    if users_choice == "View Users":
        view_users(engine)

    elif users_choice == "Add User":
        add_user(engine)

    elif users_choice == "Update User":
        update_user(engine)

    elif users_choice == "Delete User":
        delete_user(engine)


def view_users(engine):
    users_df = pd.read_sql_query("SELECT * FROM users", engine)
    st.dataframe(users_df)


def add_user(engine):
    email = st.text_input("Email")
    given_name = st.text_input("Given Name")
    surname = st.text_input("Surname")
    city = st.text_input("City")
    phone_number = st.text_input("Phone Number")
    profile_description = st.text_area("Profile Description")
    password = st.text_input("Password", type="password")

    if st.button("Add User"):
        with engine.connect() as connection:
            query = text(
                "INSERT INTO users (email, given_name, surname, city, phone_number, profile_description, password) "
                "VALUES (:email, :given_name, :surname, :city, :phone_number, :profile_description, :password)")
            connection.execute(query, {"email": email, "given_name": given_name, "surname": surname, "city": city,
                                       "phone_number": phone_number, "profile_description": profile_description, "password": password})
            connection.commit()
            st.success("User added successfully.")


def update_user(engine):
    user_id = st.number_input("Enter User ID to update", min_value=1)
    field_to_update = st.selectbox("Select field to update",
                                   ["email", "given_name", "surname", "city", "phone_number", "profile_description",
                                    "password"])
    new_value = st.text_input(f"Enter new {field_to_update}")

    if st.button("Update User"):
        try:
            # Create a connection from the engine
            with engine.connect() as connection:
                query = text(f"UPDATE users SET {field_to_update} = :new_value WHERE user_id = :user_id")
                connection.execute(query, {"user_id": user_id, "new_value": new_value})
                connection.commit()

            st.success("User updated successfully.")

        except Exception as e:
            st.error(f"Error updating user: {e}")


def delete_user(engine):
    user_id = st.number_input("Enter User ID to delete", min_value=1)

    if st.button("Delete User"):
        try:
            with engine.connect() as connection:
                query = text("DELETE FROM users WHERE user_id = :user_id")
                connection.execute(query, {"user_id": user_id})
                connection.commit()

            st.success("User deleted successfully.")

        except Exception as e:
            st.error(f"Error deleting user: {e}")
