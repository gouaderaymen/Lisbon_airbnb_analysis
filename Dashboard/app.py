import streamlit as st
import pandas as pd
import plotly.express as px

# Set up page configurations
st.set_page_config(page_title='Lisbon Airbnb Explorer', layout='wide')

# 1. Enhanced: Cache the data loading to prevent repetitive disk reads
@st.cache_data
def load_data():
    # Adjusted path assuming app is running inside the 'dashboard/' directory
    return pd.read_csv('data/listings_clean.csv')

# Load the dataset
try:
    df = load_data()
except FileNotFoundError:
    st.error("Data file not found. Ensure 'data/listings_clean.csv' exists relative to your project root.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filter Options")
neighborhood = st.sidebar.selectbox('Neighborhood', ['All'] + sorted(df['neighbourhood_cleansed'].dropna().unique()))
room = st.sidebar.selectbox('Room type', ['All'] + sorted(df['room_type'].dropna().unique()))

# Filter Logic
filtered = df.copy()
if neighborhood != 'All':
    filtered = filtered[filtered['neighbourhood_cleansed'] == neighborhood]
if room != 'All':
    filtered = filtered[filtered['room_type'] == room]

# Main Dashboard Interface
st.title("🇵🇹 Lisbon Airbnb Explorer")

# 2. Enhanced: Safe empty-state handling if filters return 0 results
if len(filtered) == 0:
    st.warning("⚠️ No listings match your selected criteria. Try adjusting your sidebar filters.")
else:
    # 3. Enhanced: Organized metric display using side-by-side columns
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Median Price', f"€{filtered['price'].median():.0f}")
    with col2:
        st.metric('Total Listings', f"{len(filtered):,}")

    st.plotly_chart(
        px.scatter_map(                  # Changed from scatter_mapbox to scatter_map
            filtered, 
            lat='latitude', 
            lon='longitude',
            color='price', 
            zoom=11, 
            map_style='carto-positron',   # Changed from mapbox_style to map_style
            hover_name='neighbourhood_cleansed',
            hover_data=['room_type', 'price']
        ), 
        use_container_width=True
    )
