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
+ 
## Instalación de la librería

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

Para usar las funciones de texto se debe realizar lo siguiente:

```
from SpaceInvaders.news import ner_from_url, ner_from_file, ner_from_str
from SpaceInvaders.text_preprocessor import textPreprocessor
```

## Ejemplos

### Función `detect_objects_in_video(text: str, output_path: str)`:

Un llamado de ejemplo es el sguiente:

```
detect_objects_in_video(detect_objects_in_video('VideoCodefest_001-11min.mpg', './output/'))
```

Es MUY importante notar que el argumento ```output_path``` no hace referencia al nombre del archivo
a guardar en formato .csv si no al directorio en el que se guardará el archivo. Por defecto, este archivo
tiene como nombre 'results.csv'. Si se quiere configurar el nombre, se puede usar como guía el siguiente
llamado:

```
detect_objects_in_video(detect_objects_in_video('VideoCodefest_001-11min.mpg', './output/', csv_name='custom'))
```

También es MUY importante notar que el nombre se pasa sin la extensión. La librería se encarga de ponerla automáticamente.

---

Para la identificación de entidades en texto se puede usar las siguientes funciones:
### Función `ner_from_str(text: str, output_path: str)`: 
Esta función recibe como parámetros el texto a analizar y la ruta del archivo en el que se guardará el resultado. Se analizan y clasifican las entidades, y estas se guardan en un diccionario con las siguientes llaves: 'org', 'per', 'loc', 'misc'. Cada llave tiene como valor una lista con las entidades encontradas en el texto. Luego se encuentran las identidades de fechas y estas se guardan en el diccionario con la llave 'date'. Después, se hace una predicción con un modelo clasificador basado en redes neuronales que se entrenó y se guardó en un pipeline. Esta clasificación se guarda en el diccionario con la llave 'impact'. Finalmente, el diccionario se guarda en un archivo .json en la ruta especificada.

```
from SpaceInvaders.news import ner_from_str
from SpaceInvaders.text_preprocessor import textPreprocessor

ner_from_str("En las últimas semanas, se ha tendido en medio de la opinión pública las cifras sobre deforestación en Colombia presentadas por el Ministerio de Ambiente y Desarrollo Sostenible, después de analizar los reportes del Sistema de Monitoreo de Bosques y Carbono del Instituto de Hidrología, Meteorología y Estudios Ambientales (Ideam). De acuerdo con la cartera, en las últimas dos décadas se han deforestado en el país 3,1 millones de hectáreas de bosque, siendo la Amazonia colombiana, el sector más afectado. Según el ministerio, en el periodo entre 2001 y 2021, la Amazonia perdió al menos 1,8 millones de hectáreas (ha), lo que estimó un promedio de 88.490 ha, anualmente. Así mismo, se aseguró que en comparación del primer semestre de 2021, la deforestación en esta zona del país en los primeros seis meses de 2022, aumentó un 11% con 54.460 ha y se estima que la tendencia al alza continúe.", "str.json")```
```

### Función `ner_from_file(text_path: str, output_path: str)`: 
Esta funcioin recibe como parámetros la ruta del archivo de texto a analizar y la ruta del archivo en el que se guardará el resultado. Se extrae el texto del archivo y se le pasa el texto extraido a la función ner_from_str. Este metodo recibe archivos de la extención .txt, .docx y .pdf.

```
from SpaceInvaders.news ner_from_file
from SpaceInvaders.text_preprocessor import textPreprocessor

ner_from_file("texto.pdf", "file.json")
```
### Función `ner_from_url(url: str, output_path: str)`:
Esta función recibe como parámetros la URL de la noticia a analizar y la ruta del archivo en el que se guardará el resultado. Se extrae el texto de la noticia con la librería newspaper3k y se le pasa el texto extraído a la función ner_from_str.

``` 
from SpaceInvaders.news import ner_from_url
from SpaceInvaders.text_preprocessor import textPreprocessor

ner_from_url("https://cods.uniandes.edu.co/mineria-una-amenaza-latente-para-la-amazonia/", "url.json")
``` 

### Identificación objetos de interés en videos:

### Estrategia:

### Vídeo
La estrategia para resolver el reto consistió en tres fases:
1. Identificación de las entidades de interés (vehículos, ríos, grúas, casas, etc.) de manera manual con ayuda de la página makesense.ai.
2. Entrenamiento de una red neuronal pre-entrenada con los datos manualmente anotados obtenidos en el anterior paso. La arquitectura utilizada fue YOLO en su octava versión provista por la librería ```ultralytics```
3. Abstraccion y definición de los contratos funcionales.

El siguiente diagrama ayuda a digerir lo anteriormente dicho:

![estrategia-video](https://github.com/favalosdev/AD_ASTRA2023-SpaceInvaders/assets/25191695/3406d535-20ec-479e-9a53-37218745668b)

### Texto
La estrategia para resolver el reto de los textos consistió en cuatro fases:

1. Identificación de las entidades de interés (organizaciones, personas, lugares, fechas, miscelánea). Asimismo, se identificaron las posibles clasificaciones de los textos (Deforestación, Contaminación, Minería o Ninguna).
2. Se revisaron los datos proporcionados y se llevó a cabo un proceso de limpieza y verificación de la calidad de los datos. Posteriormente, se realizó un enriquecimiento del conjunto de datos mediante web scraping para obtener el texto completo de cada una de las noticias. Luego se revisaron y corrigieron manualmente las etiquetas de los textos.
3. Se probaron varios modelos de Named Entity Recognition (NER). Se exploraron alternativas como Spacy, Flair, entre otras. Para las entidades de fechas, se crearon expresiones regulares para su identificación.
4. Se desarrolló un modelo de clasificación de textos. Se realizó un proceso de preprocesamiento de los textos, se vectorizaron y se entrenaron varios modelos de clasificación. Se evaluaron diferentes alternativas como Random Forest, redes neuronales, Support Vector Classifier, entre otras. Para cada una de estas opciones, se ajustaron los hiperparámetros y se compararon las métricas de interés (f1 score y accuracy).

El siguiente diagrama ayuda a digerir lo anteriormente dicho:
