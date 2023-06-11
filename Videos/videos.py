import numpy as np
import os
import re
import subprocess
import shlex
import matplotlib.pyplot as plt
import torch
from ultralytics import YOLO
import uuid
import csv
import cv2
from datetime import datetime
import easyocr
import pkg_resources
from pathlib import Path
torch.cuda.empty_cache()
seed = 2023


"""
"""
def detect_objects_in_video(
    video_path: str,
    output_path: str,
    image_every_x_seconds=30,
    confidence_threshold=0.6
):
    # Definir header del .csv
    to_write = [('ID', 'OBJECT_TYPE', 'TIME', 'COORDINATES_TEXT')]
    
    frames_info = __probe(video_path, output_path, image_every_x_seconds)
    # Cargar el modelo que se entrenó
    model = YOLO(Path(__file__).parent / 'model_m_25.pt')
    reader = easyocr.Reader(['en', 'es'])
    
    for frame_path, time in frames_info:
        rows = __extract_information(model, reader, output_path, frame_path, confidence_threshold, time)
        to_write.extend(rows)
    
    __compose_csv(output_path, to_write)

def __extract_information(model: YOLO, reader: easyocr.Reader, output_path: str, image_path: str, confidence_threshold: float, time: int) -> list:
    to_add = []
    
    # Obtener las coordenadas
    coordinates_text = __extract_coordinates(reader, image_path)
    
    # Detectar los objetos
    result = model.predict(image_path)[0]
    
    # Iterar por cada uno de los objetos detectados
    for box in result.boxes:
        conf = round(box.conf[0].item(), 2)

        # Filtrar dependiendo de la confianza del modelo
        if conf > confidence_threshold:
            object_type = result.names[box.cls[0].item()].upper()
            boundaries = [round(x) for x in box.xyxy[0].tolist()]
            identifier = str(uuid.uuid4())
            
            # Dibujar en la imagen el recuadro
            __draw_box(output_path, image_path, boundaries, identifier, object_type)
            
            to_add.append((identifier, object_type, time, coordinates_text))
            
    return to_add

def __draw_box(output_path: str, image_path: str, boundaries: list, identifier: str, object_type: str):
    image = cv2.imread(image_path)
    x1, y1, x2, y2 = boundaries
    
    # Dibuja el recuadro del objeto detectado en la imagen
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Añadir un label a la imagen
    tag_label = object_type
    cv2.putText(image, tag_label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)

    # Escribir la imagen con el recuadro y el tag
    cv2.imwrite(os.path.join(output_path, 'IMG', identifier + '.jpg'), image)

"""
Obtener muestra de imágenes con ffmpeg.
"""
def __probe(video_path: str, images_path: str, image_every_x_seconds: int)-> list:
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    frames_dir = 'tmp'
    
    subprocess.run(shlex.split(f'ffmpeg -hide_banner -loglevel panic -i {video_path} -vf fps=1/{image_every_x_seconds} {frames_dir}/%04d.jpg'), shell=True)
    
    # Espera a que el proceso finalice
    subprocess.call
    
    frames_paths = [os.path.join(frames_dir, file_name) for file_name in os.listdir(frames_dir) if file_name.endswith('.jpg')]
    
    video_info = subprocess.check_output(shlex.split(f'ffprobe -v error -select_streams v:0 -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {video_path}'))
    
    # Esperar que el proceso finalice, otra vez
    subprocess.call
    
    video_duration = float(video_info.decode('utf-8').strip())
    
    # Calcular en qué momento del vídeo se observa cada frame
    # tomando en cuenta el número del frame y el número de segundos
    
    frame_timestamps = []
    for frame_path in frames_paths:
        frame_index = int(os.path.splitext(os.path.basename(frame_path))[0])
        timestamp = datetime.utcfromtimestamp(frame_index * image_every_x_seconds).strftime('%H:%M:%S')
        frame_timestamps.append(timestamp)
        
    return zip(frames_paths, frame_timestamps)


"""
Extraer las coordenadas de un vídeo a través de
una librería que soporte OCR.
"""
def __extract_coordinates(reader:  easyocr.Reader, image_path: str) -> str:
    image = np.asarray(cv2.imread(image_path))
    lat = __get_latitude(reader, image)
    long = __get_longitude(reader, image)    
    return lat + '|' + long

def __get_latitude(reader: easyocr.Reader, image: np.array) -> str:
    box = image[40:63, 943:1050, :]
    text = __get_text(reader, box)
    return text + 'W' if text else 'Incalculable'

def __get_longitude(reader: easyocr.Reader, image: np.array) -> str:
    box = image[40:63, 1095:1219, :]
    text = __get_text(reader, box)
    return text + 'N' if text else 'Incalculable'

def __get_text(reader: easyocr.Reader, image: np.array) -> str:
    try:
        raw = reader.readtext(image=image, decoder='beamsearch')[0][1]
        print(raw)
        raw = re.sub(r'[^0-9]', '', raw)
        return raw
    except:
        return None
    

"""
"""
def __compose_csv(output_path: str, data: list):
    if not os.path.exists('output'):
        os.mkdir('output')
    csv_path = os.path.join(output_path, 'results.csv')
    with open(csv_path, 'w', encoding='UTF-8') as output:
        writer = csv.writer(output)
        writer.writerows(data)