import json
import base64
from utils import moduleColor

def getModuleData(moduleProduction, moduleData, clientId):
    productionObject = json.loads(moduleProduction)
    moduleArrayObject = json.loads(moduleData)

    positiveArrays = buildPositiveArrays(moduleArrayObject['arrays'])
    moduleArrayObject['arrays'] = positiveArrays

    moduleArrayResponse = {
        'background': moduleArrayObject['background'],
        'systemArrays': buildCustomObject(moduleArrayObject, productionObject),
        'rotation': moduleArrayObject['rotation'],
        'generalView': getImagebase64(clientId)
    }

    return moduleArrayResponse

def buildPositiveArrays(arrays):
    positiveArrays = []

    for array in arrays:
        positiveArrayObject = array
        positiveModules = []
        modules = array['modules']

        minX = abs(min(modules, key = lambda x:x['x'])['x'])
        minY = abs(min(modules, key = lambda x:x['y'])['y'])

        print(f"minX {minX}, minY {minY}")

        for module in modules:
            posiiveModule = module
            posiiveModule['x'] = module['x'] + minX
            posiiveModule['y'] = module['y'] + minY

            positiveModules.append(posiiveModule)

        positiveArrayObject['modules'] = positiveModules
        positiveArrays.append(positiveArrayObject)

    return positiveArrays

def getImagebase64(clientId):
    fileName = f"VistaGeneral/{clientId}.JPG"
    base64Image = ""

    with open(fileName, 'rb') as imageFile:
        base64Image = base64.b64encode(imageFile.read())
    
    return base64Image.decode('utf-8')

def buildCustomObject(modulesData, modulesProduction):
    customArrays = []
    maxProduction = round(max(modulesProduction['production'].values()) / 1000, 2)

    for arrayObject in modulesData['arrays']:
        customArrayObject = {}
        customArrayObject['azimuth'] = arrayObject['azimuth']
        customArrayObject['label'] = arrayObject['label']
        modules = arrayObject['modules']
        customModules = []
        
        customArrayObject['xMax'] = max(modules, key = lambda x:x['x'])['x']
        customArrayObject['yMax'] = min(modules, key = lambda y:y['y'])['y']
        
        for module in modules:
            customModuleObject = {}
            customModuleObject['inverterId'] = module['inverter']['inverter_id']
            customModuleObject['x'] = module['x']
            customModuleObject['y'] = module['y']
            customModuleObject['generatedPower'] = getModuleProduction(modulesProduction, module['inverter']['inverter_id'])
            customModuleObject['moduleColor'] = getModuleColor(customModuleObject['generatedPower'], maxProduction)
            customModuleObject['panelRotation'] = module['rotation']

            customModules.append(customModuleObject)

        customArrayObject['modules'] = customModules
        customArrays.append(customArrayObject)
    
    return customArrays

def getModuleProduction(modulesProduction, inverterId):
    return round(modulesProduction['production'][str(inverterId)] / 1000, 2)

def getModuleColor(moduleProduction, maxProduction):
    modulesColors = moduleColor.Colors
    modulePercentage = round((moduleProduction / maxProduction) * 100, 2)

    if modulePercentage >= modulesColors.C1.value['minPercentage']:
        return modulesColors.C1.value['color']
    elif modulePercentage >= modulesColors.C2.value['minPercentage'] and modulePercentage <= modulesColors.C2.value['maxPercentage']:
        return modulesColors.C2.value['color']
    elif modulePercentage >= modulesColors.C3.value['minPercentage'] and modulePercentage <= modulesColors.C3.value['maxPercentage']:
        return modulesColors.C3.value['color']
    elif modulePercentage >= modulesColors.C4.value['minPercentage'] and modulePercentage <= modulesColors.C4.value['maxPercentage']:
        return modulesColors.C4.value['color']
    elif modulePercentage >= modulesColors.C5.value['minPercentage'] and modulePercentage <= modulesColors.C5.value['maxPercentage']:
        return modulesColors.C5.value['color']
    else:
        return modulesColors.C6.value['color']
