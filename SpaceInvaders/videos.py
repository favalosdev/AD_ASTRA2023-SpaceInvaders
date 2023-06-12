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
import shutil

torch.cuda.empty_cache()
seed = 2023


def detect_objects_in_video(
    video_path: str,
    output_path: str,
    image_every_x_seconds=30,
    confidence_threshold=0.6,
    csv_name='results'
):
    """
    Detecta objetos en un archivo de video y escribe los resultados en un archivo CSV.

    Parámetros:
        video_path (str): La ruta al archivo de video.
        output_path (str): Directorio destino que contendrá el CSV y el directorio IMG con las imágenes anotadas.
        image_every_x_seconds (int, opcional): Intervalo en segundos para extraer fotogramas del video. Por defecto es 30.
        confidence_threshold (float, opcional): Umbral de confianza para la detección de objetos. Por defecto es 0.6.
        csv_name (str, opcional): Nombre del archivo CSV resultante SIN extensión. Por defecto es 'results'.

    Retorna:
        None

    Lanza:
        Cualquier excepción lanzada por las funciones subyacentes.

    Descripción:
        Este método detecta objetos en un archivo de video utilizando un modelo pre-entrenado de detección de objetos (basado en YOLO-v8) 
        y extrae información de los objetos detectados utilizando un lector OCR (Reconocimiento Óptico de Caracteres).
        El método procesa fotogramas del video en intervalos regulares especificados por 'image_every_x_seconds'.
        La información de los objetos detectados se escribe en un archivo CSV especificado por 'output_path'.

        El parámetro 'video_path' debe ser una ruta válida a un archivo de video soportado por la librería de procesamiento
        de video ffmpeg.

        El parámetro 'image_every_x_seconds' determina el intervalo en el que se extraen los fotogramas del video. Por ejemplo,
        si 'image_every_x_seconds' se establece en 30, se extraerá un fotograma cada 30 segundos del video.

        El parámetro 'confidence_threshold' controla el nivel mínimo de confianza requerido para considerar un objeto como detectado.
        Los objetos con puntajes de confianza por debajo de este umbral se ignorarán. 
        
        Las clases (tipos) de los objetos son: casa, construccion,via, vehiculo, rio, fuente hidrica, lancha, deforestacion, 
        mineria ilegal y otros.

        El archivo CSV de salida tendrá las siguientes columnas: 'ID', 'OBJECT_TYPE', 'TIME' y 'COORDINATES_TEXT'.
        Cada fila representa un objeto detectado en un fotograma e incluye el ID único del objeto, el tipo de objeto,
        el tiempo en el video en el que se detectó el objeto y el texto extraído de las coordenadas del objeto
        utilizando OCR.

    Ejemplo:
        detect_objects_in_video('ruta/video.mp4', 'salida', image_every_x_seconds=60, confidence_threshold=0.7)
    """
     
    # Definir header del .csv
    to_write = [('ID', 'OBJECT_TYPE', 'TIME', 'COORDINATES_TEXT')]
    
    if not os.path.exists(output_path):
        os.mkdir(output_path)

        if not os.path.exists(os.path.join(output_path, 'IMG')):
            os.mkdir(os.path.join(output_path, 'IMG'))
    
    else:
        shutil.rmtree(os.path.join(output_path, 'IMG'))
        os.mkdir(os.path.join(output_path, 'IMG'))


    frames_info = __probe(video_path, output_path, image_every_x_seconds)

    # Cargar el modelo que se entrenó
    model = YOLO(Path(__file__).parent / 'model.pt')
    reader = easyocr.Reader(['en', 'es'])
    
    for frame_path, time in frames_info:
        rows = __extract_information(model, reader, output_path, frame_path, confidence_threshold, time)
        to_write.extend(rows)
    
    __compose_csv(output_path, to_write, csv_name)

    # Limpiar el espacio de trabajo
    shutil.rmtree(os.path.join(output_path, 'tmp'))

def __extract_information(model: YOLO, reader: easyocr.Reader, output_path: str, image_path: str, confidence_threshold: float, time: int) -> list:

    """
    Extrae información de objetos detectados en una imagen utilizando un modelo y un lector OCR.

    Parámetros:
        model: El modelo utilizado para la detección de objetos.
        reader: El lector OCR utilizado para extraer coordenadas de texto.
        output_path: La ruta de salida donde se guarda la imagen con los objetos detectados.
        image_path: La ruta de la imagen de entrada.
        confidence_threshold: Umbral de confianza para filtrar los objetos detectados.
        time: El tiempo asociado a la imagen en un video.

    Retorna:
        Una lista de tuplas que contiene 'ID', 'OBJECT_TYPE', 'TIME' y 'COORDINATES_TEXT' sobre los objetos detectados.

    Descripción:
        Este método toma un modelo pre-entrenado para la detección de objetos, un lector OCR y una imagen de entrada.
        Utiliza el modelo para detectar objetos en la imagen y el lector OCR para extraer las coordenadas de texto.
        Los objetos detectados con una confianza por encima del umbral especificado se guardan en una lista de tuplas,
        junto con su información relevante (identificador, tipo de objeto, tiempo y coordenadas de texto).

        La función devuelve una lista de tuplas, donde cada tupla contiene información sobre un objeto detectado.
        Cada tupla tiene el siguiente formato: (identificador, tipo de objeto, tiempo, coordenadas de texto).

    Ejemplo:
        model = YOLO('ruta/modelo.pt')
        reader = easyocr.Reader(['en', 'es'])
        image_path = 'ruta/imagen.jpg'
        output_path = 'ruta/salida/'
        confidence_threshold = 0.6
        time = 5

        objects_info = extract_information(model, reader, output_path, image_path, confidence_threshold, time)
    """
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
            __draw_box(output_path, image_path, boundaries, identifier, object_type, conf)
            
            to_add.append((identifier, object_type, time, coordinates_text))
            
    return to_add

def __draw_box(output_path: str, image_path: str, boundaries: list, identifier: str, object_type: str, conf: float):
    
    """
    Dibuja un recuadro alrededor de un objeto detectado en una imagen y guarda la imagen resultante.

    Parámetros:
        output_path: La ruta de salida donde se guarda la imagen resultante.
        image_path: La ruta de la imagen de entrada.
        boundaries: Las coordenadas del recuadro del objeto detectado (x1, y1, x2, y2).
        identifier: El identificador único del objeto.
        object_type: El tipo de objeto detectado.
        conf: La confianza del modelo en la detección del objeto.

    Retorna:
        None

    Descripción:
        Este método toma una imagen de entrada, las coordenadas de un recuadro que delimita un objeto detectado,
        un identificador único para el objeto y el tipo de objeto detectado.
        Luego, dibuja un recuadro alrededor del objeto en la imagen y agrega un etiqueta con el tipo de objeto.
        La imagen resultante se guarda en la ruta de salida especificada por 'output_path'.

        El parámetro 'boundaries' especifica las coordenadas del recuadro del objeto detectado.
        Debe ser una lista o tupla con cuatro valores: (x1, y1, x2, y2), donde (x1, y1) son las coordenadas del punto
        superior izquierdo del recuadro y (x2, y2) son las coordenadas del punto inferior derecho del recuadro.

        El método utiliza la biblioteca OpenCV para leer la imagen de entrada, dibujar el recuadro y la etiqueta,
        y luego guardar la imagen resultante en 'output_path'.

    Ejemplo:
        image_path = 'ruta/imagen.jpg'
        output_path = 'ruta/salida.jpg'
        boundaries = [100, 100, 200, 200]
        identifier = 'objeto1'
        object_type = 'coche'

        draw_box(output_path, image_path, boundaries, identifier, object_type)
    """

    image = cv2.imread(image_path)
    x1, y1, x2, y2 = boundaries
    
    # Dibuja el recuadro del objeto detectado en la imagen
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Añadir un label a la imagen
    tag_label = object_type
    cv2.putText(image, tag_label + ' ' + str(conf), (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)

    # Escribir la imagen con el recuadro y el tag
    cv2.imwrite(os.path.join(output_path, 'IMG', identifier + '.jpg'), image)

def __probe(video_path: str, output_path: str, image_every_x_seconds: int) -> list:

    """
    Extrae los cuadros de un video y calcula los momentos en que se observa cada cuadro. Implementa threads para obtener
    ágilmente las imágenes.
    
    Parámetros:
        video_path (str): Ruta del archivo de video.
        output_path (str): Ruta de salida para almacenar los cuadros extraídos.
        image_every_x_seconds (int): Intervalo de tiempo en segundos para extraer los cuadros. Por ejemplo, 5 extraerá
                                     1 cuadro cada 5 segundos.
    
    Retorna:
        list: Lista de tuplas que contiene la ruta de cada cuadro extraído y su momento en el video.

    Ejemplo:
        video_path = 'ruta/video.mp4'
        output_path = 'ruta/salida'
        image_every_x_seconds = 5

        probe(video_path, output_path, image_every_x_seconds)
    """

    frames_dir = os.path.join(output_path, 'tmp')
    if not os.path.exists(frames_dir):
        os.mkdir(frames_dir)
  
    
    subprocess.run(shlex.split(f'ffmpeg -hide_banner -loglevel panic -i {video_path} -vf fps=1/{image_every_x_seconds} {frames_dir}/%05d.jpg'))
    
    # Espera a que el proceso finalice
    subprocess.call
    
    frames_paths = [os.path.join(frames_dir, file_name) for file_name in os.listdir(frames_dir) if file_name.endswith('.jpg')]
    
    # Calcular en qué momento del vídeo se observa cada frame
    # tomando en cuenta el número del frame y el número de segundos
    
    frame_timestamps = []
    for frame_path in frames_paths:
        frame_index = int(os.path.splitext(os.path.basename(frame_path))[0])
        timestamp = datetime.utcfromtimestamp(frame_index * image_every_x_seconds).strftime('%H:%M:%S')
        frame_timestamps.append(timestamp)
        
    return zip(frames_paths, frame_timestamps)

def __extract_coordinates(reader:  easyocr.Reader, image_path: str) -> str:

    """
    Extrae las coordenadas geográficas de una imagen utilizando OCR.
    
    Parámetros:
        reader (easyocr.Reader): Instancia de la clase Reader de easyocr.
        image_path (str): Ruta del archivo de imagen.
    
    Retorna:
        str: Coordenadas geográficas en el formato "latitud|longitud".
       
    Ejemplo:       
        reader = easyocr.Reader(['en', 'es'])
        image_path = 'ruta/imagen.jpg'
        
        extract_coordinates(reader, image_path)
    """
    image = np.asarray(cv2.imread(image_path))
    lat = __get_latitude(reader, image)
    long = __get_longitude(reader, image)    
    return lat + '|' + long

def __get_latitude(reader: easyocr.Reader, image: np.array) -> str:
    
    """
    Obtiene la latitud de una imagen utilizando OCR.
    
    Parámetros:
        reader (easyocr.Reader): Instancia de la clase Reader de easyocr.
        image: Imagen en formato de numpy array.
    
    Retorna:
        str: Latitud de la imagen. O 'Incalculable' si no pudo calcular adecuadamente el valor.
       
    Ejemplo:       
        reader = easyocr.Reader(['en', 'es'])
        image = np.asarray(cv2.imread('ruta/imagen.jpg'))
        
        get_latitude(reader, image)
    """

    try:
        box = image[40:64, 1080:1250, :]
        text = reader.readtext(image=box)[0][1]
        text = re.sub(r'\D', '', text)
        long = text[:2] + '°' + text[3:4] + '\''+ text[5:7] + '\'\'' + ' W'
        return long
    except:
        return 'Incalculable'

def __get_longitude(reader: easyocr.Reader, image: np.array) -> str:
    
    """ 
    Obtiene la longitud de una imagen utilizando OCR.
    
    Parámetros:
        reader (easyocr.Reader): Instancia de la clase Reader de easyocr.
        image: Imagen en formato de numpy array.
    
    Retorna:
        str: Longitud de la imagen. O 'Incalculable' si no pudo calcular adecuadamente el valor.
       
    Ejemplo:       
        reader = easyocr.Reader(['en', 'es'])
        image = np.asarray(cv2.imread('ruta/imagen.jpg'))
        
        get_longitud(reader, image)
    """

    try:
        box = image[40:63, 940:1080, :]
        text = reader.readtext(image=box)[0][1]
        text = re.sub(r'\D', '', text)
        lat = text[:1] + '°' + text[2:4] + '\'' + text[5:7] + '\'\'' + ' N'
        return lat
    except:
        return 'Incalculable'
    
def __compose_csv(output_path: str, data: list, csv_name: str):
    
    """
    Crea un archivo CSV y escribe los datos en él.

    Parámetros:
        output_path: La ruta de salida donde se creará el archivo CSV.
        data: Los datos a escribir en el archivo CSV.
        csv_name: Nombre del CSV resultante. Es pasado por parámetro desde el método principal de la libería
            de lo contrario, tomará el nombre 'results.csv'

    Retorna:
        None

    Descripción:
        Este método toma los datos proporcionados y los escribe en un archivo CSV en la ruta de salida especificada por 'output_path'.

        El parámetro 'data' es una lista de listas o tuplas que contiene los datos a escribir en el archivo CSV. Data tiene la siguiente
        estructura: [('ID', 'OBJECT_TYPE', 'TIME', 'COORDINATES_TEXT')]. Cada lista o tupla representa una fila en el archivo CSV.

    Ejemplo:
        output_path = 'ruta/archivo.csv'
        data = [('ID', 'OBJECT_TYPE', 'TIME', 'COORDINATES_TEXT'), ('1', 'Coche', '10:15:30', "45°67'32'' N| 76°3'42'' W")]

        compose_csv(output_path, data)
    """
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    csv_path = os.path.join(output_path, csv_name + '.csv')
    with open(csv_path, 'w', encoding='UTF-8') as output:
        writer = csv.writer(output)
        writer.writerows(data)