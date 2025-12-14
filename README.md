
# 🍽️ Santa Barbara Restaurant Navigator

An interactive **Streamlit web application** for exploring restaurants in **Santa Barbara** using Yelp-style data. Users can filter restaurants by cuisine and star rating, view them on an interactive map, and read real customer reviews for individual restaurants.

🔗 **Live App:** [https://yelpanalysis.streamlit.app/](https://yelpanalysis.streamlit.app/)

## 📌 Overview

The **Santa Barbara Restaurant Navigator** helps users discover restaurants that match their preferences by combining:

* ⭐ Yelp star ratings
* 🍴 Cuisine categories
* 🗺️ Interactive geospatial visualization
* 📝 Real customer reviews

The app is designed to be intuitive, visually engaging, and useful for both casual users and data-driven exploration.

## ✨ Key Features

### 🔍 Restaurant Filtering

* Filter restaurants by **cuisine category** (e.g., American (New), Mexican, Italian, etc.)
* Select a **star rating range** using an interactive slider

### 🗺️ Interactive Map View

* Restaurants are displayed on a **Leaflet map**
* Each location is represented with a custom marker
* Map updates dynamically based on selected filters

### 📋 Restaurant Table

* Displays filtered restaurants with:

  * Name
  * Address
  * Postal code
  * Average star rating

### 📝 Review Explorer

* Select a specific restaurant to view its reviews
* Filter reviews by **star rating**
* Read detailed customer feedback directly within the app


## 🛠️ Tech Stack

* **Python**
* **Streamlit** – frontend and app framework
* **Pandas** – data cleaning and manipulation
* **Folium / Leaflet** – interactive mapping
* **Yelp Dataset** – restaurant and review data

## 🚀 How to Use the App

1. Select a **cuisine category**
2. Adjust the **star rating range**
3. Explore matching restaurants on the **map** and in the **table**
4. Choose a restaurant to read **individual reviews**
5. Filter reviews further by rating if desired

## 📊 Data

The app is powered by Yelp-style restaurant and review data, including:

* Business details (name, location, categories)
* Star ratings
* User-written reviews

⚠️ This project is for **educational and analytical purposes** only and complies with Yelp dataset usage guidelines.

## 💡 Why This Project Matters

This project demonstrates:

* End-to-end **data analysis and visualization**
* Building **interactive dashboards** with Streamlit
* Integrating **geospatial data** into a web app
* Turning raw review data into an intuitive user experience

It’s ideal for showcasing skills in **data science**, **analytics**, and **product-oriented thinking**.


## 🧪 Run Locally

```bash
git clone https://github.com/ayahrhalabi/santa-barbara-restaurant-navigator.git
cd santa-barbara-restaurant-navigator
pip install -r requirements.txt
streamlit run app.py
```

## 📌 Future Improvements

* Sentiment analysis on review text
* Price range and hours filtering
* Review keyword extraction
* Performance optimization for larger dataset


## 📜 License

This project is licensed under the **MIT License**.
