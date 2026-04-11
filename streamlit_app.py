import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Santa Barbara Restaurant Navigator", layout="centered")

st.title("Santa Barbara Restaurant Navigator")
st.write(
    "Welcome! This is a web app for exploring restaurants in Santa Barbara. "
    "You can select a cuisine and star rating to see matching restaurants on a map, "
    "and view reviews for a specific restaurant below."
)

BUSINESS_URL = "https://huggingface.co/datasets/ayahhalabi/yelp_ca_reviews/resolve/main/ca_bus.csv"
REVIEWS_URL = "https://huggingface.co/datasets/ayahhalabi/yelp_ca_reviews/resolve/main/ca_reviews.csv"

CAT_TO_EMOJI = {
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
    "Other": "🌎",
}


@st.cache_data(show_spinner=False)
def load_business_data():
    usecols = [
        "business_id",
        "name",
        "address",
        "postal_code",
        "stars",
        "latitude",
        "longitude",
        "categories_grouped",
    ]
    df = pd.read_csv(
        BUSINESS_URL,
        usecols=usecols,
        low_memory=False,
    )
    return df


@st.cache_data(show_spinner=False)
def load_reviews_for_business(business_id: str) -> pd.DataFrame:
    usecols = ["business_id", "text", "stars", "funny", "useful", "cool"]
    chunks = pd.read_csv(
        REVIEWS_URL,
        usecols=usecols,
        chunksize=100_000,
        low_memory=False,
    )

    matches = []
    for chunk in chunks:
        sub = chunk[chunk["business_id"] == business_id]
        if not sub.empty:
            matches.append(sub)

    if matches:
        return pd.concat(matches, ignore_index=True)

    return pd.DataFrame(columns=usecols)


df = load_business_data()

df_unique = (
    df.drop_duplicates(subset="business_id", keep="first")
      .copy()
)

df_unique = df_unique.dropna(subset=["categories_grouped", "stars", "latitude", "longitude"])

# -------- FILTERS AT TOP ----------
colf1, colf2 = st.columns(2)

with colf1:
    cuisine_options = sorted(df_unique["categories_grouped"].dropna().unique().tolist())
    category = st.selectbox("Select Cuisine Category", cuisine_options)

with colf2:
    min_star = float(df_unique["stars"].min())
    max_star = float(df_unique["stars"].max())
    star_range = st.slider(
        "Select Star Rating Range",
        min_value=min_star,
        max_value=max_star,
        value=(min_star, max_star),
        step=0.5,
    )

# -------- APPLY FILTERS ----------
filtered = df_unique[
    (df_unique["categories_grouped"] == category)
    & (df_unique["stars"].between(star_range[0], star_range[1]))
].copy()

# -------- TABLE ----------
st.subheader("Restaurants")

if filtered.empty:
    st.info("No restaurants match the selected filters.")
else:
    st.dataframe(
        filtered[["name", "address", "postal_code", "stars"]],
        hide_index=True,
        use_container_width=True,
        column_config={
            "name": "Name",
            "address": "Address",
            "postal_code": "Postal Code",
            "stars": "Stars",
        },
    )

# -------- MAP ----------
st.subheader("Map View")

if not filtered.empty:
    center = [filtered["latitude"].mean(), filtered["longitude"].mean()]
else:
    center = [df_unique["latitude"].mean(), df_unique["longitude"].mean()]

m = folium.Map(
    location=center,
    zoom_start=13,
)
for _, row in filtered.iterrows():
    emoji = CAT_TO_EMOJI.get(row["categories_grouped"], "🍽️")
    icon = folium.DivIcon(html=f"<div style='font-size:20px'>{emoji}</div>")
    popup_html = f"<b>{row['name']}</b><br>⭐ {row['stars']}<br>{row['address']}"

    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=popup_html,
        icon=icon,
    ).add_to(m)

st_folium(m, width=900, height=550)

# -------- REVIEWS ----------
st.subheader("Restaurant Reviews")

if filtered.empty:
    st.info("Select filters that return at least one restaurant to view reviews.")
else:
    # Use a unique display label so duplicate restaurant names do not cause issues.
    filtered = filtered.assign(
        display_label=filtered["name"] + " — " + filtered["address"].fillna("")
    )

    selected_label = st.selectbox(
        "Select a restaurant to see reviews:",
        filtered["display_label"].tolist(),
    )

    selected_row = filtered.loc[filtered["display_label"] == selected_label].iloc[0]
    business_id = selected_row["business_id"]

    with st.spinner("Loading reviews..."):
        restaurant_reviews = load_reviews_for_business(business_id)

    if restaurant_reviews.empty:
        st.write("No reviews available.")
    else:
        min_review_star = float(restaurant_reviews["stars"].min())
        max_review_star = float(restaurant_reviews["stars"].max())

        review_star_range = st.slider(
            "Filter reviews by star rating",
            min_value=min_review_star,
            max_value=max_review_star,
            value=(min_review_star, max_review_star),
            step=0.5,
            key=f"review_slider_{business_id}",
        )

        restaurant_reviews = restaurant_reviews[
            restaurant_reviews["stars"].between(review_star_range[0], review_star_range[1])
        ].copy()

        if restaurant_reviews.empty:
            st.write("No reviews match the selected star range.")
        else:
            reviews_html = """
            <div style="height:600px; overflow-y:scroll; border:1px solid #ccc; padding:10px; border-radius:8px;">
            """
            for _, r in restaurant_reviews.iterrows():
                review_text = str(r.get("text", "")).replace("\n", "<br>")
                review_stars = r.get("stars", "")
                funny = r.get("funny", 0)
                useful = r.get("useful", 0)
                cool = r.get("cool", 0)

                reviews_html += (
                    f"<p style='margin-bottom:16px;'>"
                    f"⭐ {review_stars}<br>"
                    f"“{review_text}”<br>"
                    f"😂 {funny} &nbsp; 🤔 {useful} &nbsp; 😎 {cool}"
                    f"</p>"
                )

            reviews_html += "</div>"
            st.markdown(reviews_html, unsafe_allow_html=True)