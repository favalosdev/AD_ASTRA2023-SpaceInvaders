import torch
torch.cuda.empty_cache()
from datetime import timedelta
import cv2 as cv
import numpy as np
import os
import re
import ffmpeg
import subprocess
import shlex
import easyocr
import matplotlib.pyplot as plt
seed = 2023

from ultralytics import YOLO

def detect_objects_in_video(video_path, output_path, image_every_x_seconds=30):   
    """ Este codigo retorna los objetos detectados en un video a partir de su path. 
        Retorna. CSV con caracteristicas de los objetos.
                 Carpeta IMG con las imagenes.
    """
    
    print("Cargando video...")
    
    images_path = output_path+"/IMG_originales/"
    p_images_path = output_path+"/IMG"
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    if not os.path.exists(images_path):
        os.makedirs(images_path)
    if not os.path.exists(p_images_path):
        os.makedirs(p_images_path)
    
    subprocess.run(shlex.split(f'ffmpeg -hide_banner -i {video_path} -vf fps=1/{image_every_x_seconds} {output_path}IMG_originales/%04d.jpg'))
    subprocess.call # Espera a que el proceso finalice
    
    print("Video cargado exitosamente...")
    
    # Iteramos sobre cada elemento para realizar la predicción
    model_trained = YOLO("model.pt") 
  
    for image in os.listdir(images_path):
        image_path = os.path.join(images_path, filename)
        if image_path.endswith('jpg') or image_path.endswith('png'):
            try:
                #images.append(image_path)
                model_trained.predict(source=image_path, save=True, conf=0.5)  # Predecimos una imagen 
            except:
                continue
    
detect_objects_in_video('videos/VideoCodefest_001-11min.mpg', 'output/')