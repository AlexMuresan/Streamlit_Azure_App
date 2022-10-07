#!/bin/bash
cd Streamlit-App
nginx -t &&
service nginx start &&
streamlit run Home.py --server.port=8501 --server.address=0.0.0.0