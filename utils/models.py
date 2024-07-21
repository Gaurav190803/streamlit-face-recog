from ultralytics import YOLO
face_detect_model = YOLO("models/yolov8n-face.pt")

from transformers import ViTImageProcessor, ViTModel
processor = ViTImageProcessor.from_pretrained('models/face-embedding-model')
face_recog_model = ViTModel.from_pretrained('models/face-embedding-model')

def get_embeddings(face):
    return face_recog_model(**processor(face,return_tensors = "pt")).pooler_output.detach().numpy()[0]