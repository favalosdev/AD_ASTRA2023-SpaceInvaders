# AD ASTRA 2023 - Space Invaders

## Instalación

Se require tener instalado el paquete `ffmpeg`. Esto se hace de las siguiente manera:

### En windows:
+ Dirijase a la pagina de [ffmpeg](https://ffmpeg.org/download.html)
+ Una vez en la página dirijase hacia abajo hasta la sección "Get packages & executable files", seleccione windows y descarge el ejecutable.
+ Descomprime el archivo ZIP descargado en una ubicación de tu computadora.
+ Agregue la ruta de los ejecutables de FFmpeg a la variable de entorno PATH de tu sistema.
    + Haga clic derecho en "Este equipo" o "Mi PC" y selecciona "Propiedades".
    + Haga clic en "Configuración avanzada del sistema" en el lado izquierdo.
    + En la ventana de Propiedades del sistema, haz clic en el botón "Variables de entorno".
    + En la sección "Variables del sistema", desplázate hacia abajo y encuentra la variable "Path". Selecciona la variable y haz clic en "Editar".
    + Haga clic en "Nuevo" y agrega la ruta a la carpeta de los ejecutables de FFmpeg `C:\ruta\a\ffmpeg\bin`.
    + Haga clic en "Aceptar" para guardar los cambios.
+ Abra una nueva ventana de símbolo del sistema (command prompt) y ejecuta ffmpeg o ffprobe para verificar la instalación. Se debería ver la información de la versión impresa en la consola.
### En Linux:
+ Abra una consola y ejecute los siguientes comandos dependiendo del gestor de paquetes con el que cuente, por ejemplo para ubuntu:
    ```
    sudo apt-get update
    sudo apt-get install ffmpeg
    ```
+ Después de que se complete la instalación, puedes ejecutar `ffmpeg` o `ffprobe` en la terminal para verificar la instalación. Se debería ver la información de la versión impresa en la consola
### En Mac OS:
+ Instale Homebrew si aún no lo has hecho. Abra Terminal y ejecute el siguiente comando:
    ```
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
+ Una vez instalado Homebrew, ejecute el siguiente comando en Terminal para instalar FFmpeg:
    ```
    brew install ffmpeg
    ```
+ Después de que se complete la instalación, puede ejecutar `ffmpeg` o `ffprobe` en Terminal para verificar la instalación. Se debería ver la información de la versión impresa en la consola.

Por otra parte, se recomienda usar una versión de python mayor o igual a python 3.9. Además, se recomienda usar un entorno virtual de python para hacer uso de la libreria. Para instalar instala la libreria mediante pip y el repositorio de github:

```
pip install git+https://github.com/favalosdev/AD_ASTRA2023-SpaceInvaders.git
```

## Importación

### Vídeo

Para importar el módulo de vídeo solo basta con hacer lo siguiente:

```
from SpaceInvaders.videos import detect_objects_in_video
```

### Texto

Para usar las funciones de texto se debe importar lo siguiente :
```
from SpaceInvaders.news import ner_from_url, ner_from_file, ner_from_str
from SpaceInvaders.text_preprocessor import textPreprocessor
```

## Ejemplos

## Identificación objetos de interés en videos:

### Estrategia:

La estrategia para resolver el reto consistió en tres fases:
1. Identificación de las entidades de interés (vehículos, ríos, grúas, casas, etc.) de manera manual con ayuda de la página makesense.ai.
2. Entrenamiento de una red neuronal convolucional con los datos manualmente anotados.
3. Construcción de una librería con los insumos de las anteriores etapas, que permite generar el archivo csv con la información requerida.

El siguiente esquema permite esclarecer de manera visual cómo se llevó a cabo cada etapa. También se detallan las herramientas utilizdas:

### Texto

* Lo primero que hicimos cuando nos enteramos del reto fue definir que requerimientos y cuáles eran las funcionales que queríamos lograr para cada uno de los desafios. 
* Luego, nos dividimos según los conocimientos,  experiencia e intereses de cada uno de los miembros del equipo. Decidimos que dos personas iban a trabajar en el reto de textos y dos personas realizarían el reto de análisis de videos, mientras que nuestro cadete nos iba a brindar apoyo en investigación para la creación de la librería y en el desarrollo de tareas que se requirieran como el etiquetado de las imágenes de los videos. 
* Cada subgrupo empezó a investigar y documentarse buscando tutoriales y ejemplos del uso de las herramientas y librerías encontradas. 
* En cada subgrupo definimos y  asignamos tareas específicas para lograr el objetivo 
*En el subequipo de análisis de texto, revisamos los datos que teníamos y pensamos en cómo podíamos nutrir más el data set, entre esto realizamos búsquedas de más noticias y extrajimos el contenido de los links de las noticias del data set. 
* En el subequipo de análisis de vídeo, definimos cuáles labels íbamos a reconocer, luego de esto, cogimos cada vídeo y obtuvimos imágenes, una cada 15 segundos. En todo el equipo nos repartimos para hacer el etiquetado de las imágenes. 
* Para la realización del modelo de clasificación de textos, intentamos varias alternativas como random forest, redes neuronales, SVC, entre otras, para cada una de estas encontramos los mejores hiperparametros y comparamos las métricas de interés (f1 score y accuracy)