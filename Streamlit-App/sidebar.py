import streamlit as st
import glob
import os

import util


def get_contract_list():
    '''get list of all contracts from persistent storage'''
    return [os.path.basename(f) for f in
        glob.glob(os.path.join(
            st.session_state['conf']['CONTRACTS_HOME'],
            '*'))]

def get_contract_ids(client):
    '''get existing contract ids for a given client'''
    return [os.path.basename(f) for f in
        glob.glob(os.path.join(
            st.session_state['conf']['CONTRACTS_HOME'],
            client,
            '*'))]


def page():
    '''creates the sidebar nav in streamlit app'''

    with st.sidebar:
        # non-contract nav
        col1, col2 = st.columns(2)

        with col1:
            if st.button('Home'):
                st.session_state['current_page'] = 'home'
        with col2:
            if st.button('Debug'):
                st.session_state['current_page'] = 'debug'

        st.markdown("""---""")

        client = st.selectbox('Select a contract', get_contract_list())
        contract_id = st.selectbox('Select a contract ID',
                get_contract_ids(client))

        col1_2, col2_2 = st.columns(2)

        with col1_2:
            if st.button('New Contract'):
                st.session_state['current_page'] = 'initialize'
                st.session_state['init_saved'] = False
                st.session_state['contract'] = {
                        'all_steps': ['Initialize', 'Cluster', 'Train', 'Optimize', 'Review'],
                        'complete': [0, 0, 0, 0, 0],
                        'in_progress': [1, 0, 0, 0, 0],
                        'button_pages': ['initialize', 'clusters', 'train', 'optimize', 'review']
                    }


        with col2_2:
            if st.button('Load Contract'):
                st.session_state['current_page'] = 'initialize'
                util.read_contract_data(client, contract_id)
        
        st.markdown("""---""")


        if st.session_state.get('contract'):
            util.stepped_progress(
                    st.session_state['contract']['all_steps'],
                    st.session_state['contract']['complete'],
                    st.session_state['contract']['in_progress'],
                    st.session_state['contract']['button_pages']
                )

            st.write(st.session_state['contract'])









