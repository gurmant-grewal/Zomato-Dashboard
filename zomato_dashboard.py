import pandas as pd
import streamlit as st
import plotly.express as px

# Country code mapping dictionary
country_code_map = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zealand",
    162: "Philippines",
    166: "Qatar",
    184: "Singapore",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "UAE",
    215: "United Kingdom",
    216: "United States"
}

# Load dataset
df = pd.read_csv("zomato.csv", encoding='latin-1')

# Add a Country column using mapping
df['Country'] = df['Country Code'].map(country_code_map)

# Handle missing values in cuisines
df['Cuisines'] = df['Cuisines'].fillna('Unknown').str.split(', ')
df = df.explode('Cuisines')
# --- Streamlit UI ---
st.set_page_config(page_title="Zomato Dashboard", layout="wide")
st.title("🍽️ Zomato Cuisine Popularity Dashboard")
st.markdown("Explore popular cuisines by country and city.")

# --- Country Filter ---
if 'Country' not in df.columns:
    st.error("❌ 'Country' column not found in dataset.")
else:
    selected_country = st.selectbox("Select Country", sorted(df['Country'].dropna().unique()))
    df = df[df['Country'] == selected_country]

    # --- City Filter ---
    selected_city = st.selectbox("Select City", sorted(df['City'].dropna().unique()))
    df = df[df['City'] == selected_city]

    # --- Cuisine Count ---
    cuisine_counts = df['Cuisines'].value_counts().reset_index()
    cuisine_counts.columns = ['Cuisine', 'Count']

    # --- Slider for Top N ---
    top_n = st.slider("Select Top N Cuisines", 5, 30, 10)
    top_cuisines = cuisine_counts.head(top_n)

    # --- Bar Chart ---
    fig = px.bar(top_cuisines, x='Cuisine', y='Count',
                 title=f"Top {top_n} Cuisines in {selected_city}, {selected_country}",
                 color='Count', text='Count', height=500)
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.caption("Built with ❤️ using Streamlit and Plotly.")
