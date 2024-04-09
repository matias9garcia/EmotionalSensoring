import pandas as pd
import os
import json
import re

#senales=["ECG", "GSR"]
senales=["ECG"]

for senal in senales:
    ruta="datos/RawData/Multimodal/"+senal
    emociones=[ {"id": 1, "estado": "happy"},
                {"id": 2, "estado": "sad"},
                {"id": 3, "estado": "neutral"},
                {"id": 4, "estado": "surprise"},
                {"id": 5, "estado": "disgust"},
                {"id": 6, "estado": "anger"},
                {"id": 7, "estado": "fear"}]

    participantes=12
    sesiones=3

    entries=[]
    limite_de_archivos=3
    sesiones_analizadas=0
    #Lectura de datos
    for item in os.listdir(ruta):
        sesiones_analizadas=sesiones_analizadas+1
        if(sesiones_analizadas==limite_de_archivos):
            break
        else:
            with open(ruta+"/"+item, "r") as archivo:
                #participante=
                info=item.split("_")[1].split(".dat")[0]
                #Extrayendo la sesion
                auxstr=re.split('s|S', info)[1]
                id_sesion=re.split('p|P',auxstr)[0]
                #Extrayendo persona
                auxstr=re.split('p|P', info)[1]
                id_persona=re.split('v|V',auxstr)[0]
                #Extrayendo video
                id_video=re.split('v|V',info)[1]
                #print(test)

                #Guardando los datos del sensor
                # Lee el archivo .dat y separa los valores por comas
                data = archivo.read().strip().split(",")

                # Convierte los datos a flotantes
                data = [float(value) for value in data]

                # Crea un DataFrame de Pandas con una sola columna
                df = pd.DataFrame(data, columns=["Signal value"])

                # Convertir el DataFrame a una lista de diccionarios JSON
                json_data = df.to_dict(orient="records")

                #Armando el JSON        
                jsonbuffer = {
                    "id_sesion": id_sesion,
                    "id_persona": id_persona,
                    "id_video": id_video,
                    "data": json_data
                }
                
                #Agregar a la lista de entradas
                entries.append(jsonbuffer)

                # Serializing json
                #json_object = json.dumps(jsonbuffer, indent=4)

        # Writing to sample.json
        with open("data_"+senal+".json", "w") as outfile:
            json.dump(entries, outfile, indent=4)

           
        