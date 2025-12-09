import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

st.title("Santa Barbara Resrtaurent Analysis")
st.write(
    "This webpage "
)

df = pd.read_csv('ca_rest.csv')
df_unique = df.drop_duplicates(subset="business_id", keep="first")

# --- Calculate map center ---
center_lat = df_unique["latitude"].mean()
center_lon = df_unique["longitude"].mean()

# --- Create Folium map ---
m = folium.Map(location=[center_lat, center_lon],
               zoom_start=12,
               tiles="OpenStreetMap")

marker_cluster = MarkerCluster().add_to(m)

popup_cols = st.multiselect(
    "Choose columns to show in popup:",
    df_unique.columns.tolist(),
    default=[c for c in ["name", "categories", "address"] if c in df_unique.columns]
)

# --- Helper for popup HTML ---
def make_popup(row):
    if not popup_cols:
        return ""
    return "<br>".join([f"<b>{col}:</b> {row[col]}" for col in popup_cols if col in df_unique.columns])

# --- Add markers ---
for _, row in df_unique.iterrows():
    lat = row["latitude"]
    lon = row["longitude"]

    popup_html = make_popup(row)
    folium.Marker(
        location=[lat, lon],
        popup=popup_html if popup_html else None
    ).add_to(marker_cluster)

# --- Display map ---
st.subheader("Yelp Businesses Map")
st_folium(m, height=600, width=900)
