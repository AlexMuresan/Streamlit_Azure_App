import streamlit as st
import os
import glob
import datetime
import time

import util


def page():
    ''' 
    page for initializing a (new) contract. Mostly just give basic deatils
    '''

    st.title('Initial Contract Data')

    renewal = st.checkbox('Renewal', help='''Check this box if this contract
            is a renewal of a previous contract to enable autofill options
            for many fields.''')

    col1, col2 = st.columns(2)

    if renewal:
        client = None
        contract_id = None

        with col1:
            client = st.selectbox(
                    'Select the existing Client name',
                    util.fileshare_ls(
                        [st.session_state['conf']['CONTRACTS_HOME']]
                    )
                )
        with col2:
            contract_id = st.selectbox(
                    'Select the previous contract ID to renew.',
                    util.fileshare_ls(
                        [
                            st.session_state['conf']['CONTRACTS_HOME'],
                            client
                        ],
                        extension=False
                    ),
                    disabled=False if client else True
                )

            contract_id_new = st.number_input(
                'Enter a new contract ID for this renewal.',
                value=int(contract_id) + 1,
                step=1
            )


        # grab data of old contract to cache for session auto-fills
        if client and contract_id:
            if not st.session_state.get('init_saved'):
                util.read_contract_data(client, contract_id)
                st.session_state['contract']['complete'] = [0, 0, 0, 0, 0]
                st.session_state['contract']['in_progress'] = [1, 0, 0, 0, 0]



    else:
        with col1:
            client = st.text_input(
                    'Client', 
                    help='The name of the client for which a contract is being created'
                )
        with col2:
            contract_id = st.text_input(
                    'Contract ID',
                    help='Enter a unique contract ID'
                )


    owner = st.text_input(
            'Owner',
            value=st.session_state['contract']['base']['Owner'] if renewal else '',
            help='The owner of this contract and primary internal point of contact'
        )

    location = st.text_input(
            'Location',
            value=st.session_state['contract']['base']['Location'] if renewal else '',
            help='The location of the client\'s distribution.'
        )

    start, end = st.date_input(
            'Select contract dates',
            value=(
                datetime.date.today(),
                datetime.date.today() + datetime.timedelta(days=14)
            )
        )

    footer_col1, footer_col2 = st.columns(2)

    with footer_col1:
        if st.button('Save'):
            st.session_state['init_saved'] = True
            with st.spinner("Saving contract..."):
                new_data = {
                        'base': {
                            'Client': client,
                            'id': str(contract_id_new),
                            'Owner': owner,
                            'Location': location,
                            'start_date': str(start),
                            'end_date': str(end)
                        },
                        'complete':    [1, 0, 0, 0, 0],
                        'in_progress': [0, 1, 0, 0, 0]
                    }
                contract_data = st.session_state['contract']
                contract_data.update(new_data)
                st.session_state['contract'] = contract_data
                util.save_contract()
                time.sleep(2)
                #util.read_contract_data(client, str(contract_id_new))
            st.success("Saved!")
            if st.button('OK'):
                st.session_state['tmp'] = True








