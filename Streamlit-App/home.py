import streamlit as st

def page():
    st.title('Home')
    st.write('Welcome to your Azure hosted Streamlit Web App!')
    st.write('''This application is deployed as a simple Docker image run on an
    Azure Web App service with a FileShare mounted as persistent storage for the
    application.''')

