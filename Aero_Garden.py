import logging
import urllib
import requests
import base64

"""
HASS module to read Aerogarde bounty info, later there will be an option to control the light
writen by @epotex
"""




_LOGGER = logging.getLogger(__name__)



DOMAIN = 'aerogarden'
agent = "BountyWiFi/1.1.13 (iPhone; iOS 10.3.2; Scale/2.00)"
port = "8080"
host = "http://ec2-54-86-39-88.compute-1.amazonaws.com:"

#API Calls
Login_call = "/api/Admin/Login"
SetDictPushCount = "/api/CustomData/SetDictPushCount?userID="
QueryUserDevice = "/api/CustomData/QueryUserDevice"
GetUserSetted = "/api/CustomData/GetUserSetted"
QueryDeviceOnline = "/api/CustomData/QueryDeviceOnline"
QueryDeviceStatus = "/api/CustomData/QueryDeviceStatus"
UpdateDeviceConfig ="/api/CustomData/UpdateDeviceConfig"
auth_data =""
encoded_mac = ""

AERO_PARAMETERS = {}

def base64decode(b):
    return base64.b64decode(b).decode('utf-8')

def setup(hass, base_config):
    config = base_config.get(DOMAIN)
    encoded_email = urllib.parse.quote(config['mail'])
    encoded_password = urllib.parse.quote(config['password'])
    encoded_mac = urllib.parse.quote(config['aerogarden_mac_address'])
    auth_data = "mail=" + encoded_email + "&userPwd=" + encoded_password
    apiurl = str(host) + str(port) + str(Login_call)
    headers = {
        'User-Agent': 'BountyWiFi/1.1.13 (iPhone; iOS 10.3.2; Scale/2.00)',
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate"
    }
    try:
        r = requests.post(apiurl,  data=auth_data, headers=headers)
        responce = r.json()
        #userID =responce["code"]
        userID = "3122" # debug
        device_url = "airGuid=" + encoded_mac + "&userID=" + str(userID)
        apiurl = str(host) + str(port) + str(QueryDeviceStatus)
        r = requests.post(apiurl,  data=str(device_url), headers=headers)
        garden_data = r.json()
        status = 'online'
        #extracted info
        config_id= garden_data['configID']
        airGuid = garden_data['airGuid']
        lightCycle = garden_data['lightCycle']
        pumpCycle = garden_data['pumpCycle']
        lightTemp = garden_data['lightTemp']
        lightStat = garden_data['lightStat']
        clock = garden_data['clock']
        pumpStat = garden_data['pumpStat']
        pumpHydro = garden_data['pumpHydro']
        pumpRemind4Hour = garden_data['pumpRemind4Hour']
        plantedType = garden_data['plantedType']
        garden_name =base64decode(garden_data['plantedName'])
        totalDay = garden_data['totalDay']
        plantedDay = garden_data['plantedDay']
        nutriRemindDay = garden_data['nutriRemindDay']
        alarmAllow = garden_data['alarmAllow']
        plantedDate = garden_data['plantedDate']
        nutrientDate = garden_data['nutrientDate']
        updateDate = garden_data['updateDate']
        createDate = garden_data['createDate']
        swVersion = garden_data['swVersion']
        hwVersion = garden_data['hwVersion']
        bwVersion = garden_data['bwVersion']
        oldPlantedDay = garden_data['oldPlantedDay']
        deviceID = garden_data['deviceID']
        deviceIP = garden_data['deviceIP']


    except RequestException:
        _LOGGER.exception("Error communicating with AeroGarden")
        status = 'offline'
        return False
    #display extracted info 

    hass.states.set('Aerogarden.garden_name',garden_name )
    hass.states.set('Aerogarden.config_id',config_id )
    hass.states.set('Aerogarden.airGuid',airGuid )
    hass.states.set('Aerogarden.lightCycle',lightCycle )
    hass.states.set('Aerogarden.pumpCycle',pumpCycle )
    hass.states.set('Aerogarden.lightTemp',lightTemp )
    hass.states.set('Aerogarden.lightStat',lightStat )
    hass.states.set('Aerogarden.clock',clock )
    hass.states.set('Aerogarden.pumpStat',pumpStat )
    hass.states.set('Aerogarden.pumpHydro',pumpHydro )
    hass.states.set('Aerogarden.pumpRemind4Hour',pumpRemind4Hour )
    hass.states.set('Aerogarden.totalDay',totalDay )
    hass.states.set('Aerogarden.plantedDay',plantedDay )
    hass.states.set('Aerogarden.nutriRemindDay',nutriRemindDay )
    hass.states.set('Aerogarden.alarmAllow',alarmAllow )
    hass.states.set('Aerogarden.plantedDate',plantedDate )
    hass.states.set('Aerogarden.nutrientDate',nutrientDate )
    hass.states.set('Aerogarden.updateDate',updateDate )
    hass.states.set('Aerogarden.createDate',createDate )
    hass.states.set('Aerogarden.swVersion',swVersion )
    hass.states.set('Aerogarden.hwVersion',hwVersion )
    hass.states.set('Aerogarden.bwVersion',bwVersion )
    hass.states.set('Aerogarden.oldPlantedDay',oldPlantedDay )
    hass.states.set('Aerogarden.deviceID',deviceID )
    hass.states.set('Aerogarden.deviceIP',deviceIP )
    hass.states.set('Aerogarden.Status', status)





    return True
