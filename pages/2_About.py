import streamlit as st


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

st.title("About Smart Storage Assistant App")

st.markdown("""
The Smart Storage Assistant is an AI-powered tool designed to help Nigerian farmers find the most 
suitable storage facilities for their crops. By simply asking questions like, “Where should I store 50kg of tomatoes?”, 
farmers receive personalized recommendations based on location, storage type, and capacity. Integrated with an interactive map,
 the app visualizes recommended storage hubs to make decision-making easier and more efficient. 
 This solution leverages advanced AI technology combined with real-world data to reduce post-harvest losses and support smarter agricultural storage management.


""")

st.header("Developer's Profile")

# Create three columns
col1, col2 = st.columns(2)

# Team Member 1
with col1:
    st.image("Team/lead profile.png", width=150) 
    st.markdown("**Ogunwole 'HANEZ' Olusegun**")
    st.caption("Python Developer & 3MTT AI/ML Fellow (Cohort 3)")

