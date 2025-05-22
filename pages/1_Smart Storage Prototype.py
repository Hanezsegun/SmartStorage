import os
import folium
import re
import requests
import pydeck as pdk
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import leafmap.foliumap as leafmap

st.markdown(
    """
    <style>
        /* Reduce sidebar width */
        [data-testid="stSidebar"] {
            width: 240px !important;
            min-width: 240px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
) 


st.title("🗺️ Smart Storage Locator")

# Dummy storage map
crop_storage_map = {
    "tomato": "Cold",
    "pepper": "Cold",
    "maize": "Dry",
    "beans": "Dry",
    "orange": "Cold",
    "cassava": "Dry",
    "sorghum": "Dry",
    "guinea corn": "Dry",
    "yam": "Dry",
    "banana": "Cold",
    "rice": "Dry"
}


# Dummy Dataset (1)
storage_data = pd.DataFrame([
    {"Geo-zone": "North Central", "State": "Kwara", "Facility": "Ilorin Cold Hub", "Latitude": 8.4966, "Longitude": 4.5421, "Capacity": "Large", "Type": "Cold Storage"},
    {"Geo-zone": "North Central", "State": "Nasarawa", "Facility": "Lafia Storage Center", "Latitude": 8.4966, "Longitude": 8.5156, "Capacity": "Medium", "Type": "Dry Storage"},
    {"Geo-zone": "North Central", "State": "Benue", "Facility": "Makurdi Agro Storage", "Latitude": 7.7337, "Longitude": 8.5122, "Capacity": "Large", "Type": "Dry Storage"},
    {"Geo-zone": "North East", "State": "Borno", "Facility": "Maiduguri Smart Storage", "Latitude": 11.8333, "Longitude": 13.1500, "Capacity": "Large", "Type": "Cold Storage"},
    {"Geo-zone": "North East", "State": "Adamawa", "Facility": "Yola Cold Storage", "Latitude": 9.2333, "Longitude": 12.4667, "Capacity": "Medium", "Type": "Cold Storage"},
    {"Geo-zone": "North West", "State": "Kano", "Facility": "Kano Agro Storage", "Latitude": 12.0000, "Longitude": 8.5167, "Capacity": "Small", "Type": "Dry Storage"},
    {"Geo-zone": "North West", "State": "Kaduna", "Facility": "Kaduna Smart Hub", "Latitude": 10.5167, "Longitude": 7.4333, "Capacity": "Large", "Type": "Cold Storage"},
    {"Geo-zone": "North West", "State": "Sokoto", "Facility": "Sokoto Crop Vault", "Latitude": 13.0600, "Longitude": 5.2400, "Capacity": "Medium", "Type": "Dry Storage"},
    {"Geo-zone": "South South", "State": "Rivers", "Facility": "Port Harcourt Hub", "Latitude": 4.8156, "Longitude": 7.0498, "Capacity": "Medium", "Type": "Cold Storage"},
    {"Geo-zone": "South South", "State": "Delta", "Facility": "Asaba Cold Depot", "Latitude": 6.2000, "Longitude": 6.7333, "Capacity": "Large", "Type": "Cold Storage",},
    {"Geo-zone": "South West", "State": "Oyo", "Facility": "Ibadan Cold Chain", "Latitude": 7.3775, "Longitude": 3.9470, "Capacity": "Large", "Type": "Cold Storage",},
    {"Geo-zone": "South West", "State": "Lagos", "Facility": "Lagos Mega Storage", "Latitude": 6.5244, "Longitude": 3.3792, "Capacity": "Large", "Type": "Cold Storage",},
    {"Geo-zone": "South East", "State": "Enugu", "Facility": "Enugu Storage Facility", "Latitude": 6.5244, "Longitude": 7.5139, "Capacity": "Small", "Type": "Dry Storage"},
    {"Geo-zone": "South East", "State": "Anambra", "Facility": "Awka Storage Complex", "Latitude": 6.2100, "Longitude": 7.0700, "Capacity": "Medium", "Type": "Cold Storage"}
])

# Dummy Dataset (2)
storage_data2 = pd.DataFrame([
    {"Geo-zone": "North Central", "State": "Kwara", "Facility": "Ilorin Cold Hub", "Latitude": 8.4966, "Longitude": 4.5421, "Capacity": 50, "Type": "Cold Storage", "Crops": "Tomato"},
    {"Geo-zone": "North Central", "State": "Nasarawa", "Facility": "Lafia Storage Center", "Latitude": 8.4966, "Longitude": 8.5156, "Capacity": 500, "Type": "Dry Storage", "Crops": "Tomato"},
    {"Geo-zone": "North Central", "State": "Benue", "Facility": "Makurdi Agro Storage", "Latitude": 7.7337, "Longitude": 8.5122, "Capacity": 1000, "Type": "Dry Storage", "Crops": "Pepper"},
    {"Geo-zone": "North Central", "State": "Kogi", "Facility": "Lokoja Dry Vault", "Latitude": 7.8023, "Longitude": 6.7333, "Capacity": 700, "Type": "Dry Storage", "Crops": "Cassava"},
    {"Geo-zone": "North East", "State": "Borno", "Facility": "Maiduguri Smart Storage", "Latitude": 11.8333, "Longitude": 13.1500, "Capacity": 1000, "Type": "Cold Storage", "Crops": "Maize"},
    {"Geo-zone": "North East", "State": "Adamawa", "Facility": "Yola Cold Storage", "Latitude": 9.2333, "Longitude": 12.4667, "Capacity": 500, "Type": "Cold Storage", "Crops": "Beans"},
    {"Geo-zone": "North East", "State": "Gombe", "Facility": "Gombe Dry Unit", "Latitude": 10.2833, "Longitude": 11.1667, "Capacity": 800, "Type": "Dry Storage", "Crops": "Guinea Corn"},
    {"Geo-zone": "North East", "State": "Taraba", "Facility": "Jalingo Yam Vault", "Latitude": 8.8904, "Longitude": 11.3616, "Capacity": 600, "Type": "Dry Storage", "Crops": "Yam"},
    {"Geo-zone": "North West", "State": "Kano", "Facility": "Kano Agro Storage", "Latitude": 12.0000, "Longitude": 8.5167, "Capacity": 50, "Type": "Dry Storage", "Crops": "Orange"},
    {"Geo-zone": "North West", "State": "Kaduna", "Facility": "Kaduna Smart Hub", "Latitude": 10.5167, "Longitude": 7.4333, "Capacity": 1000, "Type": "Cold Storage", "Crops": "Tomato"},
    {"Geo-zone": "North West", "State": "Sokoto", "Facility": "Sokoto Crop Vault", "Latitude": 13.0600, "Longitude": 5.2400, "Capacity": 500, "Type": "Dry Storage", "Crops": "Tomato"},
    {"Geo-zone": "North West", "State": "Kebbi", "Facility": "Birnin Kebbi Sorghum Store", "Latitude": 12.4539, "Longitude": 4.1979, "Capacity": 700, "Type": "Dry Storage", "Crops": "Sorghum"},
    {"Geo-zone": "North West", "State": "Zamfara", "Facility": "Gusau Dry Depot", "Latitude": 12.1700, "Longitude": 6.6600, "Capacity": 600, "Type": "Dry Storage", "Crops": "Cassava"},
    {"Geo-zone": "South South", "State": "Rivers", "Facility": "Port Harcourt Hub", "Latitude": 4.8156, "Longitude": 7.0498, "Capacity": 500, "Type": "Cold Storage", "Crops": "Pepper"},
    {"Geo-zone": "South South", "State": "Delta", "Facility": "Asaba Cold Depot", "Latitude": 6.2000, "Longitude": 6.7333, "Capacity": 1000, "Type": "Cold Storage", "Crops": "Maize"},
    {"Geo-zone": "South South", "State": "Edo", "Facility": "Benin Banana Vault", "Latitude": 6.3405, "Longitude": 5.6170, "Capacity": 600, "Type": "Cold Storage", "Crops": "Banana"},
    {"Geo-zone": "South South", "State": "Akwa Ibom", "Facility": "Uyo Crop Depot", "Latitude": 5.0333, "Longitude": 7.9333, "Capacity": 800, "Type": "Cold Storage", "Crops": "Tomato"},
    {"Geo-zone": "South West", "State": "Oyo", "Facility": "Ibadan Cold Chain", "Latitude": 7.3775, "Longitude": 3.9470, "Capacity": 1000, "Type": "Cold Storage", "Crops": "Tomato"},
    {"Geo-zone": "South West", "State": "Lagos", "Facility": "Lagos Mega Storage", "Latitude": 6.5244, "Longitude": 3.3792, "Capacity": 50, "Type": "Cold Storage", "Crops": "Beans"},
    {"Geo-zone": "South West", "State": "Osun", "Facility": "Osogbo Root Depot", "Latitude": 7.7697, "Longitude": 4.5560, "Capacity": 700, "Type": "Dry Storage", "Crops": "Cassava"},
    {"Geo-zone": "South West", "State": "Ekiti", "Facility": "Ado-Ekiti Storage Center", "Latitude": 7.6167, "Longitude": 5.2167, "Capacity": 400, "Type": "Dry Storage", "Crops": "Yam"},
    {"Geo-zone": "South East", "State": "Enugu", "Facility": "Enugu Storage Facility", "Latitude": 6.5244, "Longitude": 7.5139, "Capacity": 500, "Type": "Dry Storage", "Crops": "Beans"},
    {"Geo-zone": "South East", "State": "Anambra", "Facility": "Awka Storage Complex", "Latitude": 6.2100, "Longitude": 7.0700, "Capacity": 500, "Type": "Cold Storage", "Crops": "Orange"},
    {"Geo-zone": "South East", "State": "Imo", "Facility": "Owerri Smart Storage", "Latitude": 5.4833, "Longitude": 7.0333, "Capacity": 500, "Type": "Cold Storage", "Crops": "Banana"},
    {"Geo-zone": "South East", "State": "Abia", "Facility": "Umuahia Crop Hub", "Latitude": 5.5333, "Longitude": 7.4833, "Capacity": 600, "Type": "Dry Storage", "Crops": "Yam"},
    {"Geo-zone": "North Central", "State": "Plateau", "Facility": "Jos Cold Chain", "Latitude": 9.8965, "Longitude": 8.8583, "Capacity": 900, "Type": "Cold Storage", "Crops": "Tomato"},
    {"Geo-zone": "North Central", "State": "FCT", "Facility": "Abuja Mega Depot", "Latitude": 9.0765, "Longitude": 7.3986, "Capacity": 1500, "Type": "Dry Storage", "Crops": "Rice"},
    {"Geo-zone": "South South", "State": "Cross River", "Facility": "Calabar Crop Cold Store", "Latitude": 4.9589, "Longitude": 8.3269, "Capacity": 750, "Type": "Cold Storage", "Crops": "Banana"},
    {"Geo-zone": "North East", "State": "Yobe", "Facility": "Damaturu Dry Depot", "Latitude": 11.7463, "Longitude": 11.9608, "Capacity": 600, "Type": "Dry Storage", "Crops": "Guinea Corn"},
    {"Geo-zone": "South West", "State": "Ogun", "Facility": "Abeokuta Agro Facility", "Latitude": 7.1500, "Longitude": 3.3500, "Capacity": 1000, "Type": "Cold Storage", "Crops": "Rice"}
])
storage_data2["Crops"] = storage_data2["Crops"].str.lower()



tab1, tab2 = st.tabs(["Smart Storage Overview", "Smart Storage Assitant"])

with tab1:
    zone = st.selectbox("Select your geo-zone:", storage_data["Geo-zone"].unique())

    #  Filter by selected zone
    zone_df = storage_data[storage_data["Geo-zone"] == zone]

    # Sidebar filters
    selected_type = st.sidebar.multiselect("Select Storage Type", storage_data["Type"].unique(), default=storage_data["Type"].unique())
    selected_capacity = st.sidebar.multiselect("Select Storage Capacity", storage_data["Capacity"].unique(), default=storage_data["Capacity"].unique())


    # Apply type and capacity filters within the selected zone
    filtered_storage = zone_df[
        zone_df["Type"].isin(selected_type) & zone_df["Capacity"].isin(selected_capacity)
    ]

    st.subheader("Available Storage Facilities in Your Zone")
    st.dataframe(filtered_storage[["State", "Facility", "Type", "Capacity"]])

    # Create Folium map
    m = folium.Map(location=[9.0820, 8.6753], zoom_start=6)

    # Add filtered markers
    for _, row in filtered_storage.iterrows():
        popup_content = (
            f"<b>{row['Facility']}</b><br>"
            f"State: {row['State']}<br>"
            f"Capacity: {row['Capacity']}<br>"
            f"Type: {row['Type']}"
        )
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=popup_content,
            icon=folium.Icon(color="blue" if row["Type"] == "Cold Storage" else "green", icon="tint" if row["Type"] == "Cold Storage" else "archive",
            prefix='fa')
        ).add_to(m)

    # Display map
    st.subheader("Facility Locations")
    #folium_static(m)
    st_folium(m, width=700, height=500)



with tab2:
    user_query = st.chat_input("Ask where to store your produce...")

    if user_query:
        with st.spinner("Finding best storage options..."):
            crop_found = None
            quantity = None

            for crop in crop_storage_map.keys():
                if crop in user_query.lower():
                    crop_found = crop
                    break

            qty_match = re.search(r"(\d+)(\s?kg)?", user_query)
            if qty_match:
                quantity = int(qty_match.group(1))

            if not crop_found:
                st.warning(f"Sorry, No available storage facility for this crops. Please try again.")
            else:
                needed_type = crop_storage_map[crop_found]
                filtered = storage_data2[
                    (storage_data2["Type"] == f"{needed_type} Storage") &
                    (storage_data2["Capacity"] >= (quantity or 0)) &
                    (storage_data2["Crops"].apply(lambda crops: crop_found in crops))
                ]

                if filtered.empty:
                    st.error(f"No {needed_type.lower()} storage facility found for {crop_found} with capacity of {quantity or 'any'} kg.")
                else:
                    st.success(f"Storage options for {quantity or 'your'} kg of {crop_found}:")

                    # Create map with markers
                    m = leafmap.Map(center=[9.0820, 8.6753], zoom=6)
                    for _, row in filtered.iterrows():
                        popup_text = f"""
                        <b>{row.Facility}</b><br>
                        State: {row.State}<br>
                        Type: {row.Type}<br>
                        Capacity: {row.Capacity} kg
                        """
                        m.add_marker(location=[row.Latitude, row.Longitude], popup=popup_text)

                    m.to_streamlit(width=700, height=500)

                    for _, row in filtered.iterrows():
                        st.markdown(f"**{row.Facility}**, {row.State} ({row['Type']}) - Capacity: {row.Capacity} kg")
    else:
        st.info("Enter a crop storage question to begin.")
