import pandas as pd
import streamlit as st
from sqlalchemy import text


def address_menu(engine):
    st.subheader("Addresses Menu")

    users_submenu = ["View Addresses", "Add Addresses", "Update Addresses", "Delete Addresses"]
    users_choice = st.sidebar.selectbox("Select Operation", users_submenu)

    if users_choice == "View Addresses":
        view_addresses(engine)

    elif users_choice == "Add Addresses":
        add_address(engine)

    elif users_choice == "Update Addresses":
        update_address(engine)

    elif users_choice == "Delete Addresses":
        delete_address(engine)


def view_addresses(engine):
    addresses_df = pd.read_sql_query("SELECT * FROM ADDRESS", engine)
    st.dataframe(addresses_df)


def view_addresses(engine):
    addresses_df = pd.read_sql_query("SELECT * FROM ADDRESS", engine)
    st.dataframe(addresses_df)


def add_address(engine):
    member_user_id = st.number_input("Member User ID")
    house_number = st.text_input("House Number")
    street = st.text_input("Street")
    town = st.text_input("Town")

    if st.button("Add Address"):
        try:
            with engine.connect() as connection:
                query = text(
                    "INSERT INTO ADDRESS (member_user_id, house_number, street, town) "
                    "VALUES (:member_user_id, :house_number, :street, :town)")
                connection.execute(query, {"member_user_id": member_user_id, "house_number": house_number,
                                           "street": street, "town": town})
                connection.commit()

            st.success("Address added successfully.")

        except Exception as e:
            st.error(f"Error adding address: {e}")


def update_address(engine):
    member_user_id = st.number_input("Enter Member User ID to update", min_value=1)
    field_to_update = st.selectbox("Select field to update", ["house_number", "street", "town"])
    new_value = st.text_input(f"Enter new {field_to_update}")

    if st.button("Update Address"):
        try:
            with engine.connect() as connection:
                query = text(
                    f"UPDATE ADDRESS SET {field_to_update} = :new_value WHERE member_user_id = :member_user_id")
                connection.execute(query, {"member_user_id": member_user_id, "new_value": new_value})
                connection.commit()

            st.success("Address updated successfully.")

        except Exception as e:
            st.error(f"Error updating address: {e}")


def delete_address(engine):
    member_user_id = st.number_input("Enter Member User ID to delete", min_value=1)

    if st.button("Delete Address"):
        try:
            with engine.connect() as connection:
                query = text("DELETE FROM ADDRESS WHERE member_user_id = :member_user_id")
                connection.execute(query, {"member_user_id": member_user_id})
                connection.commit()

            st.success("Address deleted successfully.")

        except Exception as e:
            st.error(f"Error deleting address: {e}")
