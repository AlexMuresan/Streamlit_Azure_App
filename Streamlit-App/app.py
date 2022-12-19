import streamlit as st
import json


import debug
import clusters
import home
import sidebar
import initialize
import train


DB_PATH = '/aci/data/'
CONF_FILE = 'conf.json'


def load_conf():
    '''read conf file into session state'''
    with open(CONF_FILE,'r') as f:
        st.session_state['conf'] = json.load(f)

def load_page():
    '''load the appropriate page based on st.session_state'''
    if not st.session_state.get('current_page'):
        st.session_state['current_page'] = 'home'

    page = st.session_state['current_page']

    if page == 'home':
        home.page()
    elif page == 'debug':
        debug.page()
    elif page == 'initialize':
        initialize.page()
    elif page == 'clusters':
        clusters.page()
    elif page == 'train':
        train.page()

if __name__ == "__main__":
    load_conf()
    sidebar.page()
    load_page()

