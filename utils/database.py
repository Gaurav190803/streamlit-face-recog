import pickle as pkl 
import os 
import cv2 
import numpy as np
import yaml
from collections import defaultdict
import streamlit as st
from utils.models import get_embeddings
import uuid

information = defaultdict(dict)
cfg = yaml.load(open('config.yaml','r'),Loader=yaml.FullLoader)
DATASET_DIR = cfg['PATH']['DATASET_DIR']
PKL_PATH = cfg['PATH']['PKL_PATH']

def get_database():
    if(not os.path.isfile(PKL_PATH)):
        return {}
    with open(PKL_PATH,'rb') as f:
        database = pkl.load(f)
    return database

def updateDb(id,name,phone_num):
    database = get_database()
    database[id]["name"] = name
    database[id]["phone"] = phone_num
    with open(PKL_PATH,'wb') as f:
        pkl.dump(database,f)
    return True

def get_info_from_id(id): 
    database = get_database() 
    for idx, person in database.items(): 
        if person['id'] == id: 
            name = person['name']
            image = person['image']
            phone = person["phone"]
            return True,name, image, phone       
    return False, None, None, None

def deleteOne(id):
    database = get_database()
    id = str(id)
    del database[id]
    with open(PKL_PATH,'wb') as f:
        pkl.dump(database,f)
    return True

def addNew(image,embedding):
    database = get_database()
    id = str(uuid.uuid4())[:8]
    print(id)
    database[id] = {"id":id,
                    "name":"",
                    "phone":"",
                    "image":image,
                    "embedding":embedding}
    with open(PKL_PATH,'wb') as f:
        pkl.dump(database,f)
    return id
    
