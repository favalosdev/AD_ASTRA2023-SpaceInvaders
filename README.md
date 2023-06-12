# AD ASTRA 2023 - Space Invaders

¡Hola!

## Instalación

A nivel de sistema operativo, se require el sistema operativo GNU/Linux. También se requiere tener los paquetes `gcc`, `ffmpeg` y `make` instalados. Se una versión de python mayor o igual a python 3.9, se recomienda usar un entorno virtual con python 3.9 para hacer uso de la libreria. 

Naturalmente, se instala la libreria mediante pip y el repositorio de github:
```
pip install git+https://github.com/favalosdev/AD_ASTRA2023-SpaceInvaders.git
```
## Importación
Para usar las funciones de texto se debe importar lo siguiente :
```
from SpaceInvaders.news import ner_from_url, ner_from_file, ner_from_str
from SpaceInvaders.text_preprocessor import textPreprocessor
```


## Ejemplos

## Identificación objetos de interés en videos:

### Estrategia:

La estrategia para resolver el reto consistió en tres fases:
1. Identificación de las entidades de interés (vehículos, ríos, grúas, casas, etc.) de manera manual.
2. Entrenamiento de una red neuronal convolucional con los datos manualmente anotados.
3. Construcción de una librería con los insumos de las anteriores etapas, que permite generar el archivo csv con la información requerida.

El siguiente esquema permite esclarecer de manera visual cómo se llevó a cabo cada etapa. También se detallan las herramientas utilizdas:

