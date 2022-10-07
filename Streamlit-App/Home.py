import os
import csv
import numpy as np
import pandas as pd
import streamlit as st


@st.cache
def get_chart_data():
    chart_data = pd.DataFrame(
        np.random.randn(50, 3)**2,
        columns=["a", "b", "c"]
    )

    return chart_data


def open_file(file_path):
    if not os.path.exists(file_path):
        file = open(file_path, "a+")
        writer = csv.writer(file)
        header = ["Stage_1", "Stage_2", "Stage_3", "Stage_4"]
        writer.writerow(header)
    else:
        file = open(file_path, "a")

    return file


if __name__ == "__main__":
    # Hides the gradient bar at the top
    hide_decoration_bar_style = '''
        <style>
            header {visibility: hidden;}
        </style>
    '''
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    # Sidebar Code
    with st.sidebar:
        st.markdown("# Document Information")
        st.markdown("## Name")
        st.markdown("Blueprint Consulting Services")
        st.markdown("## Representative")
        st.markdown("Ryan Neal")
        st.markdown("## Location")
        st.markdown("Greater Seattle Area, West Coast, Western US")
        st.markdown("## Contract Type")
        st.markdown("Mix Purchase and Delivery")
        st.markdown("## Contact")
        st.markdown("info@bpcs.com")

    # Main Page Code
    st.markdown("## Coca Cola Multi-Stage Process")
    st.markdown(
        "This application simulates a multi-stage document approval process."
    )

    # Progress Bar Code
    progress_steps = {
        0: "Stage 1",
        1: "Stage 2",
        2: "Stage 3",
        3: "Stage 4",
        4: "Complete"
    }

    if 'csv_row' not in st.session_state:
        st.session_state.csv_row = []

    if 'progress_idx' not in st.session_state:
        st.session_state.progress_idx = 0

    progress_state = st.empty()
    if st.session_state.progress_idx < 4:
        progress_bar = st.progress(0)
    progress_state.write(progress_steps[st.session_state.progress_idx])

    container_1 = st.empty()
    button_next = container_1.button('Next')
    container_stats = st.empty()

    finish_button = None
    
    if button_next and (st.session_state.progress_idx < 4):
        st.session_state.progress_idx += 1
        progress_bar.progress(st.session_state.progress_idx * 33)
        progress_state.write(progress_steps[st.session_state.progress_idx])
        container_stats.empty()

    if st.session_state.progress_idx == 0:
        with container_stats.container():
            st.markdown("## Contract Statistics")
            st.markdown("### Stage 1: Line Chart")
            chart_data = pd.DataFrame(
                np.random.randn(20, 3),
                columns=['a', 'b', 'c'],
                )
            st.line_chart(chart_data)
            stage_1_input = st.text_input("Decided Value")
        
        st.session_state.csv_row.append(stage_1_input)
    
    if st.session_state.progress_idx == 1:
        with container_stats.container():
            st.markdown("## Contract Statistics")
            st.markdown("### Stage 2: Bar Chart")
            chart_data = pd.DataFrame(
                np.random.randn(50, 3),
                columns=["a", "b", "c"]
            )
            st.bar_chart(chart_data)
            stage_2_input = st.text_input("Decided Value")
        
        st.session_state.csv_row.append(stage_2_input)

    if st.session_state.progress_idx == 2:
        with container_stats.container():
            st.markdown("## Contract Statistics")
            st.markdown("### Stage 3: Map Hotspots")
            df = pd.DataFrame(
                np.random.randn(200, 2) / [110, 115] + [47.60, -122.315],
                columns=['lat', 'lon']
            )
            st.map(df)
            stage_3_input = st.text_input("Decided Value")

        st.session_state.csv_row.append(stage_3_input)

    if st.session_state.progress_idx == 3:
        with container_stats.container():
            st.markdown("## Contract Statistics")
            st.markdown("### Stage 4: Bar Chart")
            
            chart_data = get_chart_data()
            st.bar_chart(chart_data)
            stage_4_input = st.text_input("Decided Value")
        
        st.session_state.csv_row.append(stage_4_input)

        m = st.markdown("""
                <style>
                div.stButton > button:first-child {
                    background-color: rgba(244, 0, 8, 0.2);
                }
                </style>""", unsafe_allow_html=True)

            # b = st.button("test")
        finish_button = container_1.button("Finish", key="ButtonFinish1")
        progress_bar.progress(100)

    if st.session_state.progress_idx == 3 and finish_button:
        st.session_state.progress_idx += 1
        st.markdown("## Contract Validation Finished!")
        progress_state.write(progress_steps[st.session_state.progress_idx])
        container_stats.empty()
        container_1.empty()
        
        file = open_file("./database.csv")
        csv_writer = csv.writer(file)
        csv_writer.writerow(st.session_state.csv_row[1:])
        file.close()
