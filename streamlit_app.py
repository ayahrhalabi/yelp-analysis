import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

st.title("Santa Barbara Restaurent Analysis")
st.write(
    "This webpage represents some visualization on some restaurents found "
    "in the Yelp Dataset in the city of Santa Barbara"
)

df = pd.read_csv('ca_rest.csv')
df_unique = df.drop_duplicates(subset="business_id", keep="first")

# -------- FILTERS AT TOP ----------
colf1, colf2 = st.columns(2)

with colf1:
    category = st.selectbox(
        "Select Cuisine Category",
        sorted(df_unique["categories"].unique())
    )

with colf2:
    min_star, max_star = st.slider(
        "Select Star Rating Range",
        float(df_unique["stars"].min()),
        float(df_unique["stars"].max()),
        (float(df_unique["stars"].min()), float(df_unique["stars"].max())),
        step=0.5
    )

# -------- APPLY FILTERS ----------
filtered = df_unique[
    (df_unique["categories"] == category) &
    (df_unique["stars"].between(min_star, max_star))
]

# -------- TABLE FIRST ----------
st.subheader("Restaurants")
st.dataframe(
    filtered[["name", "address", "stars"]],
    hide_index=True,
    use_container_width=True
)

# -------- MAP UNDER TABLE ----------
st.subheader("Map View")

if not filtered.empty:
    center = [filtered["latitude"].mean(), filtered["longitude"].mean()]
else:
    center = [df_unique["latitude"].mean(), df_unique["longitude"].mean()]

m = folium.Map(location=center, zoom_start=13)
cat_to_emoji = {
    "American (New)": "🍔",
    "Mexican": "🌮",
    "American (Traditional)": "🍟",
    "Japanese": "🍣",
    "Delis": "🥪",
    "Italian": "🍕",
    "Fast Food": "🍔",
    "Asian Fusion": "🍱",
    "French": "🥐",
    "Chinese": "🥡",
    "Mediterranean": "🥗",
    "Tapas Bars": "🧆",
    "Thai": "🍜",
    "Indian": "🍛",
    "Latin American": "🥙",
    "Korean": "🍚",
    "Cajun/Creole": "🦞",
    "Vietnamese": "🍜",
    "German": "🥨",
    "Pakistani": "🍛",
    "Argentine": "🥩",
    "Cuban": "🥘",
    "New Mexican Cuisine": "🌶️",
    "Modern European": "🍽️",
    "Peruvian": "🍤",
    "Creperies": "🥞",
    "Greek": "🥙",
    "Australian": "🥩",
    "Moroccan": "🍢",
    "Ethiopian": "🍲",
    "Belgian": "🍫",
    "Brazilian": "🍖",
    "British": "🥧",
    "Irish": "🍀",
    "Himalayan/Nepalese": "🍲",
    "Hawaiian": "🍍",
    "Caribbean": "🍹",
    "Indonesian": "🍢",
    "Scandinavian": "🍞",
    "Southern": "🍗"
}

for _, row in filtered.iterrows():
    emoji = cat_to_emoji.get(row["categories"], "🍽️")  # fallback emoji

    html = f"""
    <div style="font-size: 24px;">
        {emoji}
    </div>
    """

    icon = folium.DivIcon(html=html)

    folium.Marker(
        [row["latitude"], row["longitude"]],
        popup=f"<b>{row['name']}</b><br>⭐ {row['stars']}<br>{row['address']}",
        icon = icon
        ).add_to(m)

st_folium(m, width=900, height=550)


'''
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

# --- Table --- 
left_col, right_col = st.columns([1, 3])   # adjust width as needed

with left_col:
    st.subheader("Filters")
    selected_category = st.selectbox(
        "Choose a category:",
        sorted(df["categories"].unique())
    )

filtered = df_unique[df_unique["categories"] == selected_category][["name", "stars", "address"]]

# ---- Table on the right ----
with right_col:
    st.subheader(f"Restaurants in **{selected_category}**")
    st.dataframe(filtered, use_container_width=True)
'''