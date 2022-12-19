import streamlit as st
import streamlit.components.v1 as components
import glob
import json
import os


def set_state(key, val):
    '''set session state key value pair as a function'''
    st.session_state[key] = val

def read_contract_data(client, contract_id):
    '''read contract data from persistent storage'''
    if '.json' in contract_id:
        contract_id = contract_id.split('.json')[0]

    f_in = os.path.join(st.session_state['conf']['CONTRACTS_HOME'], client,
            f'{contract_id}.json')
    with open(f_in, 'r') as f:
        d = json.load(f)

    st.session_state['contract'] = d

def fileshare_ls(path_list, extension=True):
    '''return list of results from ls path_list/*'''
    ls = [os.path.basename(f) for f in
            glob.glob(
                os.path.join(*path_list + ['*'])
            )
        ]

    if not extension:
        ls = [l.split('.')[0] for l in ls]

    return ls

def save_contract():
    '''save contract json to fileshare, overwrite previous'''
    updated_json = st.session_state['contract']
    save_path = os.path.join(
            st.session_state['conf']['CONTRACTS_HOME'],
            st.session_state['contract']['base']['Client'],
            str(st.session_state['contract']['base']['id']) + '.json'
        )

    with open(save_path, 'w') as save_file:
        json.dump(updated_json, save_file)


def next():
    pass






def stepped_progress(all_steps, complete, in_progress, button_pages):
    '''
    Create a simple visualization of a stepped-progressbar in the sidebar.
    The visualization is rendered as static html/css and includes links to
    a new streamlit page for each step in the progress to allow users to
    edit/update/etc to move the process through.

    params
        all_steps: (list[str]) list of names for each step in the process. This
                   list is used to name each of the buttons for pages
        complete: (list[bool]) list of bools to indicate for each step
                  in this process, is it complete or not? 1 = complete, 0 = not
        in_progress: (list[bool]) list of bools to indicate for each step in the
                     process if the step is actively in progress.
        button_pages: (list[callbacks]) list of function for new pages to open
                      when each button is clicked

    return
        NA
    '''
    # validate input data
    inputs_tuples = list(zip(
        ['all_steps', 'complete', 'in_progress', 'button_pages'],
        [all_steps, complete, in_progress, button_pages]
    ))
    for l1_name, l1 in inputs_tuples:
        for l2_name, l2 in inputs_tuples:
            if len(l1) != len(l2):
                raise Exception(
                f"""Input lists must be same length:
                          {l1_name}:{len(l1)}
                          {l2_name}:{len(l2)}
                """)

    # create sidebar progress visualization and buttons
    side_cols = st.sidebar.columns(2)

    # read the css used to visualize the stepped progress bar
    with open('prog.css','r') as f:
        css_str = f.read()

    # Create the progress visualization in the left column
    with side_cols[0]:
        header = f'<html><head><style>{css_str}</style></head>'
        body = '<body><ol class="progress">'
        for idx,step in enumerate(all_steps):
            # we build out the css class list according to contract data
            # for each step in the contract
            body += '<li class="'
            if complete[idx]:
                body += 'complete '
            else:
                body += 'incomplete '

            if in_progress[idx]:
                body += 'current '
            if idx == len(all_steps) - 1:
                body += 'final_item'
            body += '"></li>'

        body += '</ol></body></html>'

        components.html(header + body, width=500, height=500)

    # Create the list of pages for each step in the process
    # this list should be aligned to the progress stages in the visual in column 0
    with side_cols[1]:
        for idx,step in enumerate(all_steps):
            st.button(step, on_click=set_state, args=('current_page', button_pages[idx]))
