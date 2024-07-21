import logging
import os
from streamlit_webrtc import VideoProcessorBase
import streamlit as st
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from scipy.spatial.distance import cosine
import cv2 as cv
from utils.database import get_database,addNew

logger = logging.getLogger(__name__)
import av
from utils.models import face_detect_model,face_recog_model,processor, get_embeddings

TOLERENCE = 0.75

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    results = face_detect_model(img,conf = 0.5)
    return av.VideoFrame.from_ndarray(results[0].plot(),format='bgr24')

def set_tolerence(tolerence):
    global TOLERENCE
    TOLERENCE = tolerence

class video_processor(VideoProcessorBase):
    def __init__(self):
        self.id = ""
        self.name = ""
        self.phone = ""
        self.face_conf = 0
        self.face_sim = 0
        self.new_user_detected = False
    
    def recv(self,frame):
        global TOLERENCE
        img = frame.to_ndarray(format="rgb24")
        results = face_detect_model(img,conf = 0.5)
        if len(results[0].boxes.conf) == 0:
            self.face_conf = 0
        else:
            self.face_conf = float(results[0].boxes.conf[0])
            a,b,c,d = results[0].boxes.xyxy[0]
            face = img[int(b):int(d),int(a):int(c)]
            embedding = get_embeddings(face)
            person,score = find_face(embedding)
            if score >= TOLERENCE:
                # st.session_state.new_user_found = False
                self.face_sim = score
                self.name = person["name"]
                self.phone = person["phone"]
                self.id = person["id"]
                self.new_user_detected = False
                
            else:
                self.new_user_detected = True
                id = addNew(img,embedding)
                self.id = id
                # st.session_state.new_user_found = True
                

            
        return av.VideoFrame.from_ndarray(results[0].plot(),format='rgb24')
    


def get_ice_servers():
    try:
        account_sid = "AC1c0ef38a8dd50c2b99f0c9930b547516"
        auth_token = "d4d13264da8209eb709353598fbbe45c"
    except KeyError:
        logger.warning(
            "Twilio credentials are not set. Fallback to a free STUN server from Google."  # noqa: E501
        )
        return [{"urls": ["stun:stun.l.google.com:19302"]}]

    client = Client(account_sid, auth_token)

    try:
        token = client.tokens.create()
    except TwilioRestException as e:
        st.warning(
            f"Error occurred while accessing Twilio API. Fallback to a free STUN server from Google. ({e})"  # noqa: E501
        )
        return [{"urls": ["stun:stun.l.google.com:19302"]}]

    return token.ice_servers

def find_face(embedding):
    database = get_database()
    if(database == {}):
        return {},0
    highest_sim = 0
    matched_id = ""
    for id,person in database.items():
        score = 1 - cosine(embedding,database[id]["embedding"])
        if(score > highest_sim):
            highest_sim = score
            matched_id = id
    return database[matched_id],highest_sim
        