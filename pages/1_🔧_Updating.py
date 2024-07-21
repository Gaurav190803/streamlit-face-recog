import streamlit as st 
import cv2
import yaml 
import pickle 
import time
from utils.database import updateDb, get_info_from_id, deleteOne
import numpy as np
st.set_page_config(layout="wide")
st.title("Face Recognition App")
st.write("This app is used to add new faces to the dataset")

def dbupdate():
    updateDb(id,st.session_state.new_name,st.session_state.new_phone)
    st.success("Details updated succesfully")
    
def dbdelete():
    deleteOne(id)
    st.success("User deleted succesfully")

id_container = st.empty()
button_container = st.empty()

id = id_container.text_input(label = "Enter Id to add/update")
button1 = button_container.button(label = "Search")

if(button1):
    exists , name, image, phone  = get_info_from_id(id)
    if(not exists):
        st.error("Id does not exist. Please use the tracking page again or recheck entered id")
    else :
        button_container.empty()
        st.success("Please fill or update the details")
        id_container.text_input(label = "Enter Id to add/update",value=id,disabled=True)
        with st.form(key = "form"):
            new_name = st.text_input(label = "Enter full name",value = name,key="new_name")
            new_phone = st.text_input(label = "Enter phone number",value = phone,key = "new_phone")
            st.image(image,width = 260)
            submitted = st.form_submit_button(label = "Update User",on_click=dbupdate)
            deleted = st.form_submit_button(label = "Delete User",on_click=dbdelete)
        
        
        

                