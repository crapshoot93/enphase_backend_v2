import pandas as pd
import json
import base64
import os

def consultClientList():
    df_excel = pd.read_excel('clientes_enphase.xlsx')
    lista_clientes = json.loads(df_excel.to_json(orient="records"))
    return lista_clientes

def getClient(id_cliente):
    lista_clientes = consultClientList()
    cantidad_clientes = len(lista_clientes)
    for i in range (cantidad_clientes):
        if id_cliente == lista_clientes[i]['User_id']:
            user_id = id_cliente
            response = lista_clientes[i]
            vista_general = vista_general_b64(user_id)
            response['vista_general'] = str(vista_general)
            break
        else:
            response = 'Error'
    return response

def vista_general_b64(id_cliente):
    user_id = id_cliente
    ruta_vista_general = './VistaGeneral'
    contenido = os.listdir(ruta_vista_general)
    consulta = str(user_id) + ".JPG"
    cantidad_contenido = len(contenido)
    for i in range (cantidad_contenido):
        if consulta == contenido[i]:
            nueva_consulta = ('./VistaGeneral/' + consulta)
            with open(nueva_consulta, 'rb') as img_file:
                b64_string = base64.b64encode(img_file.read())
            image_string = b64_string
            respuesta = image_string.decode('utf-8')
    return respuesta
