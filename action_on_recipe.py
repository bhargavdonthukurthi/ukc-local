import streamlit as st
from azure_sql import UKCAzureSQL
import pandas as pd
from constants import *
from sqlalchemy import text

def get_recipe():
    # Create an instance of the Azure SQL class
    azure_sql_instance = UKCAzureSQL(
        url=url,
        auth_token=auth_token
    )

    # Fetch the data using the query
    menu_items_df = azure_sql_instance.fetch_table_data(table_name="MENU_ITEM")
    raw_materials_df = azure_sql_instance.fetch_table_data(table_name="RAW_MATERIAL")
    unit_measure_df = azure_sql_instance.fetch_table_data(table_name="UNIT_MEASURE")
    recipe_table_df = azure_sql_instance.fetch_table_data(table_name="RECIPE")

    # Receipt Display Screen
    st.markdown("### Recipe Display")
    with st.expander("View Recipe Details"):
        if not recipe_table_df.empty:
            selected_recipe = st.selectbox(
                "Select a recipe to view details",
                recipe_table_df["MENU_ITEM_NAME"].unique().tolist()
            )

            if selected_recipe:
                recipe_details = recipe_table_df[recipe_table_df["MENU_ITEM_NAME"] == selected_recipe]
                st.markdown(f"#### Recipe for {selected_recipe}")
                st.table(recipe_details[["RAW_MATERIAL_NAME", "QUANTITY", "UNIT_MEASURE_NAME", "MEMBER_COUNT"]])
        else:
            st.info("No recipes available to display.")


    st.markdown("### ADD Recipe")
    # Dropdown for Menu Item and Raw Material
    menu_item_options = menu_items_df["NAME"].tolist()
    raw_material_options = raw_materials_df["NAME"].tolist()
    unit_measure_options = unit_measure_df["NAME"].tolist()

    # Form to enter recipe ingredients
    with st.form("recipe_form", clear_on_submit=True):
        col_packed, col_left = st.columns(2)

        with col_packed:
            # Dropdowns for selecting Menu Item and Raw Material
            selected_menu_item = st.selectbox(
                "Select Menu Item",
                menu_item_options + [None] if menu_item_options else [None],
            )
            
            quantity_input = st.number_input(
                "Enter the quantity of measure", min_value=0, step=1
            )
            member_count_input = st.number_input(
                "Enter the member count for the quantity", min_value=0, step=1, value=4
            )

        with col_left:
                
            selected_raw_material = st.selectbox(
                "Select Raw Material",
                [None] + raw_material_options if raw_material_options else [None],
            )

            selected_unit_measure = st.selectbox(
                "Select Unit of Measure",
                [None] + unit_measure_options if unit_measure_options else [None],
            )

        # Submit button within the form
        submit_button = st.form_submit_button("Save Recipe")

        if submit_button:
            if selected_menu_item and selected_raw_material:
                # SQL insert query to add data to the RECIPE table
                query = text(
                    """
                    INSERT INTO RECIPE (MENU_ITEM_NAME, RAW_MATERIAL_NAME, QUANTITY, UNIT_MEASURE_NAME, MEMBER_COUNT)
                    VALUES (:menu_item_name, :raw_material_name, :quantity, :unit_measure_name, :member_count)
                    """
                )

                # Parameters to insert into the query
                params = {
                    "menu_item_name": selected_menu_item,
                    "raw_material_name": selected_raw_material,
                    "quantity": quantity_input,
                    "unit_measure_name": selected_unit_measure,
                    "member_count": member_count_input,
                }

                # Execute the query to insert the data
                azure_sql_instance.execute_query_placeholders(query, params, type="insert")
                st.success("Recipe saved successfully!")
            else:
                st.error("Please select both a Menu Item and a Raw Material.")

    if st.button("Refresh Data"):
        try:
            # Fetch updated data and display it
            recipe_table_df = azure_sql_instance.fetch_table_data(table_name="RECIPE")
            # st.dataframe(recipe_table_df, hide_index=True)
        except Exception as e:
            st.error(f"Error refreshing data: {e}")


    st.markdown("### Existing Recipes")
    st.dataframe(recipe_table_df, hide_index=True)