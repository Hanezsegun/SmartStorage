import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
from io import StringIO
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Page config (no forced theme)
st.set_page_config(
    page_title="Smart Storage", 
    page_icon=":package:", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title (no forced color)
st.title(":package: Smart Storage Assistant")
#st.markdown("(Youth Innovation for Post-harvet Loss Reduction and Optimization)")


# ==============================================
# HOMEPAGE
# ==============================================
# Title and Subtitle Section (Centered with animation class)

st.markdown("---")

st.markdown(
        """
        <div style="text-align: center;" class="animate-fade-in">
            <h1 style="font-size: 2.8em; margin-bottom: 0; color: #1B2E4F;">Reducing Post-Harvest Losses with Smart Innovation</h1>
            
        </div>
        """,
        unsafe_allow_html=True,
)

with st.container():
        # Hero Section with two columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
                    st.markdown("""
            <div class="animate-fade-in">
                <h2>📊 Visualize Risk. Target Solutions.</h2>
                <p style="font-size: 1.1rem; line-height: 1.6;">
                    In Nigeria, up to 50% of perishable crops are lost after harvest. AI Storage Assistant combines data analytics, risk mapping, 
                    and smart technology to help youth-led agri-businesses minimize these losses and maximize profits.


            </div>
            """, unsafe_allow_html=True)

         
        
st.markdown("---")
# Key Benefits Section
st.markdown("""
    <div class="animate-fade-in">
        <h2 style="color:#4CAF50 ;text-align: center; margin-bottom: 20px;">Key Features</h2>
    </div>
    """, unsafe_allow_html=True)


# Modern card layout for benefits
col1, col2 = st.columns(2)
    
with col1:
        with st.container():
            st.markdown("""
            <div style="padding: 20px; border-radius: 10px; background-color: #e8f5e9; height: 100%;">
                <h3 style="color: #F4B400;">⚙️ Smart Storage Insights</h3>
                <p>Design intelligent storage interventions tailored to regional loss patterns.</p>
            </div>
            """, unsafe_allow_html=True)
    
    
with col2:
        with st.container():
            st.markdown("""
            <div style="padding: 20px; border-radius: 10px; background-color: #e8f5e9; height: 100%; margin-top: 15px;">
                <h3 style="color: #2E7D32;">🚜 Storage Assistance</h3>
                <p>Quickly discover best storage facilities for different farm produce.</p>
            </div>
            """, unsafe_allow_html=True)
    
st.markdown("---")
            


#### OPTIONAL FEATURES: PROJECT HIGHLIGHTS ####

# ==============================================
# HOMEPAGE
# ==============================================


