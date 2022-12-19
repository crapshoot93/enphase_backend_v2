import json
from flask import jsonify, abort, request, Blueprint
import pandas as pd
import json

from service import clients, modules

NSOLAR_API = Blueprint('nsolar_api', __name__)


def get_blueprint():
    return NSOLAR_API

@NSOLAR_API.route('/')
def index():
    return 'App de Enphase _ Backend en Flask Python'

@NSOLAR_API.route('/lista_clientes')
def consultClientList():
    df_excel = pd.read_excel('clientes_enphase.xlsx')
    lista_clientes = json.loads(df_excel.to_json(orient="records"))
    return lista_clientes

@NSOLAR_API.route('/cliente', methods=['GET'])
def setDataClient():
    if request.method == 'GET':
        id_cliente = int(request.args.get('id_cliente'))
        try:
            clientData = clients.getClient(id_cliente)
            return clientData
        except:
            clientData = 'Error'
    return clientData

@NSOLAR_API.route('/getModuleData', methods = ['POST'])
def getModuleData():
    return modules.getModuleData(request.json['moduleProduction'], request.json['moduleData'], request.json['clientId'])
