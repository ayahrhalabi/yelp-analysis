import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from io import BytesIO
import re

st.title("Santa Barbara Restaurant Navigator")
st.write(
    " Welcome! This is a simple web application of some restaurents in Santa Barabara. You can select your desired cuisine " \
        "and star rating, and an interactive map will be populated with those settings." \
        "You can also view the reviews of a specific retsuarent at the bottom of the webpage to learn more about the place"
)

# -------- Load Data from HuggingFace --------
@st.cache_data
def load_business_data():
    url = "https://huggingface.co/datasets/ayahhalabi/yelp_ca_reviews/resolve/main/ca_bus.csv"
    return pd.read_csv(url)

@st.cache_data
def load_reviews_data():
    url = "https://huggingface.co/datasets/ayahhalabi/yelp_ca_reviews/resolve/main/ca_reviews.csv"
    return pd.read_csv(url)

df = load_business_data()
df_rev = load_reviews_data()

df_unique = df.drop_duplicates(subset="business_id", keep="first")

# -------- FILTERS AT TOP ----------
colf1, colf2 = st.columns(2)

with colf1:
    category = st.selectbox(
        "Select Cuisine Category",
        sorted(df_unique["categories_grouped"].unique())
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
    (df_unique["categories_grouped"] == category) &
    (df_unique["stars"].between(min_star, max_star))
]

# -------- TABLE ----------
st.subheader("Restaurants")
st.dataframe(
    filtered[["name", "address", "postal_code", "stars"]],
    hide_index=True,
    #use_container_width=True,
    width='stretch',
    column_config={
    "name": "Name", # This changes the display name
    "address": "Address",
    "postal_code":"Postal Code",
    "stars": "Stars"
    }
)

# -------- MAP UNDER TABLE ----------
st.subheader("Map View")

if not filtered.empty:
    center = [filtered["latitude"].mean(), filtered["longitude"].mean()]
else:
    center = [df_unique["latitude"].mean(), df_unique["longitude"].mean()]

m = folium.Map(location=center, zoom_start=13)

# ICONS
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
    "Southern": "🍗",
    "Other": "🌎"
}

for _, row in filtered.iterrows():
    emoji = cat_to_emoji.get(row["categories_grouped"], "🍽️")
    html = f"<div style='font-size:20px'>{emoji}</div>"
    icon = folium.DivIcon(html=html)
    
    # Popup now shows name + stars
    popup_html = f"<b>{row['name']}</b><br>⭐ {row['stars']}<br>{row['address']}"
    
    folium.Marker(
        [row["latitude"], row["longitude"]],
        popup=popup_html,
        icon=icon
    ).add_to(m)

st_folium(m, width=900, height=550)

# -------- SELECT RESTAURANT TO SHOW REVIEWS --------
st.subheader("Restaurant Reviews")

restaurant_names = filtered["name"].tolist()
selected_restaurant = st.selectbox("Select a restaurant to see reviews:", restaurant_names)

# Filter reviews
business_id = filtered[filtered["name"] == selected_restaurant]["business_id"].values[0]
restaurant_reviews = df_rev[df_rev["business_id"] == business_id]

# Optional: Filter reviews by star rating
if not restaurant_reviews.empty:
    min_review_star, max_review_star = st.slider(
        "Filter reviews by star rating",
        float(restaurant_reviews["stars"].min()),
        float(restaurant_reviews["stars"].max()),
        (float(restaurant_reviews["stars"].min()), float(restaurant_reviews["stars"].max())),
        step=0.5
    )
    restaurant_reviews = restaurant_reviews[
        restaurant_reviews["stars"].between(min_review_star, max_review_star)
    ]

# Display reviews in separate paragraphs with quotes
if restaurant_reviews.empty:
    st.write("No reviews available.")
else:
    #for r in restaurant_reviews["text"].tolist():
        #st.markdown(f'"{r}"  \n\n') 
    reviews_html = "<div style='height:600px; overflow-y:scroll; border:1px solid #ccc; padding:10px;'>"
    for _, r in restaurant_reviews.iterrows():
        review_text = r["text"]
        review_stars = r["stars"]
        reviews_html += f"<p>⭐ {review_stars}<br>\"{review_text}\"<p> 😂{r['funny']} 🤔{r['useful']} 😎{r['cool']}"
    reviews_html += "</div>"

    st.markdown(reviews_html, unsafe_allow_html=True)
