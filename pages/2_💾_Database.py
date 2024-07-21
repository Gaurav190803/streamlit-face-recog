import streamlit as st 
import pickle 
import yaml 
import pandas as pd 
import os
cfg = yaml.load(open("config.yaml", "r"), Loader=yaml.FullLoader)
PKL_PATH = cfg['PATH']["PKL_PATH"]
st.set_page_config(layout="wide")

if(not os.path.isfile(PKL_PATH)):
    database = {}
#Load databse 
else:
    with open(PKL_PATH, 'rb') as file:
        database = pickle.load(file)

st.markdown(
    """
    <style>
    .padding {
        padding: 115px;
    }
    </style>
    """, unsafe_allow_html=True
)

# Define columns
id_col, name_col,phone_col,image_col = st.columns([0.1,0.3,0.2,0.1])
with id_col:
    st.markdown(f"<div class='padding'>ID</div>", unsafe_allow_html=True)
with name_col:
    st.markdown(f"<div class='padding'>NAME</div>", unsafe_allow_html=True)
with phone_col:
    st.markdown(f"<div class='padding'>PHONE</div>", unsafe_allow_html=True)
with image_col:
    st.markdown("<div class='padding'>IMAGE</div>",unsafe_allow_html=True)
for idx, person in database.items():
    size = person["image"].shape[0]/8
    st.markdown(
    f"""
    <style>
    .padding {{
        padding: {size}px;
    }}
    </style>
    """, unsafe_allow_html=True
)
    with id_col:
        st.markdown(f"<div class='padding'>{person['id']}</div>", unsafe_allow_html=True)
    with name_col:
        st.markdown(f"<div class='padding'>{person['name']}</div>", unsafe_allow_html=True)
    with phone_col:
        st.markdown(f"<div class='padding'>{person['phone']}</div>", unsafe_allow_html=True)
    with image_col:
        st.image(person['image'], use_column_width=True)
