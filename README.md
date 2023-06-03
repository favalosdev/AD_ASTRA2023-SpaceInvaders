# AD ASTRA 2023 - Space Invaders

¡Hola!

## Instalación

A nivel de sistema operativo, se require el sistema operativo GNU/Linux. También se requiere tener los paquetes `gcc`, `ffmpeg` y `make` instalados.

Naturalmente, toca clonar el repositorio y efectuar `pip install -r requirements.txt`.

## Importación
Para usar cualquiera de las dos soluciones se recomienda usar un entorno virtual de python, este se puede generar con:
```
python -m venv env
```
Esta instrucción puede cambiar entre sistemas operativos, por ejemplo, en linux posiblemente es python3 para usar python.Esto nos creara una nueva carpeta evn. Luego deberiamos activar este entorno virtual. Si se encuentra en windows hagal click dereco sobre la carpeta donde tiene el repositorio y abra una consola de comandos cmd y ejecute:
```
.\env\Scrip\activate
```
Si se encuentra en linux ejecute:
```
source .\env\bin\activate
```
Despues de esto, se procede a instalar todos los paquetes necesarios para la ejecución de las librerias, esto se hace mediante:
```
pip install -r requirements.txt
```
Y esperamos a que se termine de instalar todas las dependencias. En elarchivo example_textos.py se encuentra un ejemplo de como importar la libreria y de como usar los metodos.

## Ejemplos

## Identificación objetos de interés en videos:

### Estrategia:

La estrategia para resolver el reto consistió en tres fases:
1. Identificación de las entidades de interés (vehículos, ríos, grúas, casas, etc.) de manera manual.
2. Entrenamiento de una red neuronal convolucional con los datos manualmente anotados.
3. Construcción de una librería con los insumos de las anteriores etapas, que permite generar el archivo csv con la información requerida.

El siguiente esquema permite esclarecer de manera visual cómo se llevó a cabo cada etapa. También se detallan las herramientas utilizdas:

