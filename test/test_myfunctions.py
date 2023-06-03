# -*- coding: utf-8 -*-
from flair.data import Sentence
from flair.models import SequenceTagger
import json
import pandas as pd
import requests
import pandas as pd
from bs4 import BeautifulSoup

tagger = SequenceTagger.load("flair/ner-spanish-large")


    # Deserializar el objeto del archivo
#pipeline = joblib.load("pipelines.joblib")



def ner_from_str(text, output_path):
    sentence = Sentence(text)
    tagger.predict(sentence)
    entities = dict()
    for entity in sentence.get_spans('ner'):
        tag = entity.tag
        text = entity.text

        if tag in entities:
            # Si la clave ya existe, agregamos el valor a la lista existente
            entities[tag].append(text)
        else:
            # Si la clave no existe, creamos una nueva lista con el valor
            entities[tag] = [text]
    
                
    
    #df2 = {'NEWS': ['hola pelicula mala triste sueño']}
    
    #df2 = pd.DataFrame(df2) 
    response = {}
    response['text'] = sentence.text
    for key in entities:
        entities[key] = list(set(entities[key]))
        response[key.lower()] = entities[key]

    #response['impact'] = pipeline.predict(df2)

        
    with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(response, file, ensure_ascii=False)
    return sentence.to_tagged_string()


def ner_from_file(text_path, output_path):
    with open(text_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return ner_from_str(text, output_path)

#Obtener el html en texto plano
def remove_tags(html):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    # parse html content
    res = requests.get(html, headers=headers, verify=False)
    soup = BeautifulSoup(res.content, "html.parser")
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

def ner_from_url(url, output_path):
    text = remove_tags(url)
    return ner_from_str(text, output_path)


#ner_from_str("Corte Suprema ordena protección inmediata de la Amazonía Colombiana | Corte Menu ≡ ╳ Inicio La  Corte Historia Funciones Estructura Organizacional Magistrados Integrantes Reglamento General de la Corporación Vicepresidencia Salas Especializadas Civil y Agraria Secretaría Relatoría VIII CONVERSATORIO NACIONAL DE LA JURISDICCIÓN CIVIL Laboral Secretaría Relatoría Penal Secretaría Relatoría Plena y Tutelas Relatoría Comité Convivencia Laboral Esquema de publicación de información Directorio telefónico Secretaría  General Circulares e Información de Interés Calendario de Salas Plena y Gobierno Actos Administrativos de Nombramiento Requisitos de Confirmación y Posesión Gestión documental Consulta de procesos Jurisprudencia Sistema de Consulta de Jurisprudencia Sistema de Consulta por Texto Completo Gacetas Judiciales Prensa Notificaciones Sala Plena Sala de Casación Civil Sala de Casación Laboral Sala de Descongestión Laboral Sala de Casación Penal Sala Especial de Primera Instancia Sala Especial de Instrucción Home Noticias Corte Suprema ordena protección inmediata de la Amazonía Colombiana Corte Suprema ordena protección inmediata de la Amazonía Colombiana 5 abril, 2018 / Claudia Fonseca / Noticias Bogotá, D. C., 5 de abril de 2018. Tras advertir el alarmante incremento del 44% en la deforestación en la región –de 56.952 a 70.074 hectáreas entre 2015 y 2016– y que el Estado no ha enfrentado eficientemente esta problemática ambiental, la Corte Suprema de Justicia ordenó a la Presidencia de la República y a las demás autoridades nacionales, regionales y municipales involucradas en esta responsabilidad, adoptar un plan de acción de corto, mediano y largo plazo para proteger a la Amazonía Colombiana. Entre las acciones ordenadas, la Sala de Casación Civil dispone la elaboración del “Pacto Intergeneracional por la Vida del Amazonas Colombiano–PIVAC” para reducir a cero la deforestación y los gases efecto invernadero, la incorporación de componentes de preservación medioambiental en los planes municipales de ordenamiento territorial, y la ejecución efectiva de medidas policivas, judiciales y administrativas por parte de las tres corporaciones autónomas regionales con jurisdicción en el territorio amazónico. En el estudio adelantado para conceder la tutela de los derechos a gozar de un ambiente sano, vida y salud de un grupo de 25 niños, niñas, adolescentes y jóvenes representados por el director del Centro de Estudios Dejusticia, la Corte Suprema estableció que el Estado colombiano no ha enfrentado eficientemente la problemática de la deforestación en la Amazonía, pese a haber suscrito numerosos compromisos internacionales y a existir en el país suficiente normatividad y jurisprudencia sobre la materia. Según la providencia, adoptada en decisión mayoritaria de la Sala de Casación Civil, las CAR no están cumpliendo sus funciones de evaluar, controlar y monitorear los recursos naturales, ni de sancionar la violación de normas de protección ambiental; la deforestación ocurre en lugares bajo la tutela de Parques Nacionales Naturales de Colombia –PNN; departamentos como Amazonas, Caquetá, Guaviare y Putumayo también \xa0incumplen las funciones de protección ambiental, y municipios del área amazónica concentran altos niveles de deforestación sin contrarrestar esa situación. Con estos y otros elementos de juicio proporcionados por investigaciones del IDEAM y el propio Ministerio de Ambiente y Desarrollo Sostenible, la Corte determinó el nexo causal entre la afectación de los derechos fundamentales de los accionantes de la tutela, y en general las personas residentes en el país, con el cambio climático generado por la reducción progresiva de la cobertura forestal, causada por la expansión de la frontera agrícola, los narco cultivos, la minería ilegal y la tala ilícitas de los bosques de la región. “Los reseñados factores generan directamente la deforestación de la Amazonía, provocando a corto, mediano y largo plazo, un perjuicio inminente y grave para los niños, adolescentes y adultos que acuden a esta acción, y en general, a todos los habitantes del territorio nacional, tanto para las generaciones presentes como las futuras, pues desboca incontroladamente la emisión de dióxido de carbono (CO2) hacia la atmósfera, produciendo el efecto invernadero, el cual transforma y fragmenta ecosistemas, alterando el recurso hídrico y con ello, el abastecimiento de agua de los centros poblados y degradación del suelo.… “Por tanto, en aras de proteger ese ecosistema vital para el devenir global, tal como la Corte Constitucional declaró al río Atrato, se reconoce a la Amazonía Colombiana como entidad, ‘sujeto de derechos’, titular de la protección, de la conservación, mantenimiento y restauración a cargo del Estado y las entidades territoriales que la integran”, consigna la sentencia de la Sala de Casación Civil. En conclusión, la Corte Suprema de Justicia encontró que el gobierno nacional y las autoridades locales y regionales no están cumpliendo adecuadamente con los compromisos adquiridos para resguardar la Amazonía. Por ello, resolvió: Ordenar a la Presidencia de la República, al Ministerio de Ambiente y Desarrollo Sostenible, y a la Cartera de Agricultura y Desarrollo Rural para que, en coordinación con los sectores del Sistema Nacional Ambiental, y la participación de los accionantes, las comunidades afectadas y la población interesada en general, dentro de los cuatro (4) meses siguientes a la notificación de la tutela, formulen un plan de acción de corto, mediano y largo plazo, que contrarreste la tasa de deforestación en la Amazonía, en donde se haga frente a los efectos del cambio climático. Ordenar a las anteriores autoridades formular en un plazo de cinco (5) meses, con la participación activa de los tutelantes, las comunidades afectadas, organizaciones científicas o grupos de investigación ambientales, y la población interesada en general, la construcción de un “pacto intergeneracional por la vida del amazonas colombiano -PIVAC”, en donde se adopten medidas encaminadas a reducir a cero la deforestación y las emisiones de gases efecto invernadero, el cual deberá contar con estrategias de ejecución nacional, regional y local, de tipo preventivo, obligatorio, correctivo, y pedagógico, dirigidas a la adaptación del cambio climático. Ordenar a todos los municipios de la Amazonía colombiana realizar, en un plazo de cinco (5) meses, actualizar e implementar los Planes de Ordenamiento Territorial, en lo pertinente, deberán contener un plan de acción de reducción cero de la deforestación en su territorio, el cual abarcará estrategias medibles de tipo preventivo, obligatorio, correctivo, y pedagógico, dirigidas a la adaptación del cambio climático. Ordenar a la Corporación para el Desarrollo Sostenible del Sur de la Amazonía –Corpoamazonia, la Corporación para el Desarrollo Sostenible del Norte y el Oriente Amazónico –CDA, y la Corporación para el Desarrollo Sostenible del Área de Manejo Especial La Macarena –Cormacarena, realizar en un plazo de cinco (5) meses, en lo que respecta a su jurisdicción, un plan de acción que contrarreste mediante medidas policivas, judiciales o administrativas, los problemas de deforestación informados por el IDEAM. Adicionalmente, en lo de sus facultades, los organismos querellados tendrán que, en las cuarenta y ocho (48) horas siguientes a la notificación de la tutela, incrementar las acciones tendientes a mitigar la deforestación. Y presentar con mensaje de urgencia las denuncias y querellas ante las entidades administrativas y judiciales correspondientes. Vea la providencia completa, STC4360-2018 (2018-00319-01) Twittear alarma ambiental , arboles protegidos por la corte , corte proteje medio ambiente , corte suprema y cambio climático , corte suprema y vida , deforestación , desarrollo sostenible , medio ambiente , sentencia ambiental Comments are closed. (c) 2019 Corte Suprema", 'si.json')

ner_from_url('https://www.nationalgeographic.es/medio-ambiente/2020/06/deforestacion-amazonas-alcanza-niveles-historicos-debido-consumo-carne','f.json')