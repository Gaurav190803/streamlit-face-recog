import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase,WebRtcMode
from utils.webcam import video_frame_callback, get_ice_servers, video_processor
import cv2
import yaml 
import av
# Path: code\app.py

st.set_page_config(layout="centered")
#Config
cfg = yaml.load(open('config.yaml','r'),Loader=yaml.FullLoader)
PICTURE_PROMPT = cfg['INFO']['PICTURE_PROMPT']
WEBCAM_PROMPT = cfg['INFO']['WEBCAM_PROMPT']

st.sidebar.title("Settings")

TOLERANCE = st.sidebar.slider("Tolerance",0.0,1.0,0.75,0.01,key="tolerence")
#Infomation section 
st.sidebar.title("Display Information")
new_face_text = st.sidebar.text_input(label = "New Face Text",value = "Hi new user, Please note your temporary ID below to make new entry in database")

st.sidebar.checkbox(label="Id",key="disp_id",value = True)
st.sidebar.checkbox(label="Name",key="disp_name",value = True)
st.sidebar.checkbox(label="Number",key="disp_number",value = True)
st.sidebar.checkbox(label="Face Confidence Score",key="disp_face_conf",value = True)
st.sidebar.checkbox(label="Face Similarity Score",key="disp_similarity_thresh",value = True)


st.title("Face Recognition App")
st.write(WEBCAM_PROMPT)
webrtc_ctx = webrtc_streamer(
    key="object-detection",
    rtc_configuration={
    "iceServers": get_ice_servers(),
    },
    video_processor_factory=video_processor,
    async_processing=True,
    media_stream_constraints={"video": True, "audio": False},
)

new_user_text_container = st.empty()
id_container = st.empty()
name_container = st.empty()
phone_container = st.empty()
conf_container = st.empty()
sim_container = st.empty()

while True:
    if(webrtc_ctx.video_processor):
        if(webrtc_ctx.video_processor.new_user_detected):
            new_user_text_container.warning(new_face_text, icon="⚠️")
    if(st.session_state.disp_id):
        if(webrtc_ctx.video_processor):
            id = webrtc_ctx.video_processor.id
        else:
            id = "Unknown"
        id_container.info(f'Id: {id}')
    else:
        id_container.empty()
    if(st.session_state.disp_name):
        if(webrtc_ctx.video_processor):
            name = webrtc_ctx.video_processor.name
        else:
            name = "Unknown"
        name_container.info(f'Name: {name}')
    else:
        name_container.empty()
        
    if(st.session_state.disp_number):
        if(webrtc_ctx.video_processor):
            phone = webrtc_ctx.video_processor.phone
        else:
            phone = "Unknown"
        phone_container.info(f'Phone Number: {phone}')
    else:
        phone_container.empty()
        
    if(st.session_state.disp_face_conf):
        if(webrtc_ctx.video_processor):
            conf = f'{webrtc_ctx.video_processor.face_conf:.2f}'
        else:
            conf = "Unknown"
        conf_container.info(f'Confidence Score: {conf}')
    else:
        conf_container.empty()
        
    if(st.session_state.disp_similarity_thresh):
        if(webrtc_ctx.video_processor):
            sim = f'{webrtc_ctx.video_processor.face_sim:.2f}'
        else:
            sim = "Unknown"
        sim_container.info(f'Similarity Score: {sim}')
    else:
        sim_container.empty()
        
   