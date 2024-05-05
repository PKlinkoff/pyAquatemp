import requests
import json 
import hashlib
import logging
import time 



class aquatempConnect():
    _cloudURL = "https://cloud.linked-go.com:449/crmservice/api"        #requires TLSv1.1
    _token = ""
    _tokenTimestamp = 0
    _header = {"Content-Type": "application/json", "charset":"utf-8"}

    def __init__(self, username, password):
        self._username = username
        self._password = str(hashlib.md5(password.encode()).hexdigest())
        self.checkToken()               #Initial login       
        #setup devices
        r = requests.post(self._cloudURL+"/app/device/deviceList", headers=self._header)           
        self.devices = r.json()["objectResult"]

    def checkToken(self):
        if self._token == "" or (time.time()-self._tokenTimestamp>3600):     #assuming token validity for 1hour
            #get a new token
            print("Getting a new token")
            payload = {"userName":self._username, "password":self._password, "type":"2"}
            r = requests.post(self._cloudURL+"/app/user/login", headers=self._header, json=payload)
            if r.json()["error_code"] != "0": raise Exception("Connection Error "+r.json()["error_msg"])
            self._token = r.json()["objectResult"]["x-token"]
            self._header["x-token"] = self._token
            self._tokenTimestamp = time.time()
        return(self._token)

       
    def setPower(self, state, dev=0):
        payload = {"param":[{"deviceCode": self.devices[dev]["device_code"], "protocolCode": "Power","value": str(state)}]}
        r = requests.post(self._cloudURL+"/app/device/control", headers=self._header, json=payload)
        if r.json()["error_code"] != "0": logging.debug(f"Set power not successful. Error message {r.json()['error_msg']}")
        
        
    def setTemperature(self, temp, mode=None, dev=0):
        # set temperature for the current mode if not specified. R01: cooling, R02: heating, R03: auto
        if mode is None: mode = self.getStatus()["Mode"]
        payload = {"param":[{"deviceCode": self.devices[dev]["device_code"], "protocolCode": "R0"+str(mode),"value": str(temp)}]}
        r = requests.post(self._cloudURL+"/app/device/control", headers=self._header, json=payload)
        if r.json()["error_code"] != "0": logging.debug(f"Set temperature not successful. Error message {r.json()['error_msg']}")


    def setSilent(self, state="1", dev=0):
        #set silent mode. Default is to set to silent
        payload = {"param":[{"deviceCode": self.devices[dev]["device_code"], "protocolCode": "Manual-mute","value": str(state)}]}
        r = requests.post(self._cloudURL+"/app/device/control", headers=self._header, json=payload)
        if r.json()["error_code"] != "0": logging.debug(f"Set silent not successful. Error message {r.json()['error_msg']}") 
         
    def getStatus(self, dev=0):
        codes = {
                "T01":"Suction Temp",
                "T02":"Inlet Water Temp",
                "T03":"Outlet Water Temp",
                "T04":"Coil 1 Temp",
                "T05":"Ambient Temp",
                "T07":"Compressor Current",
                "T09":"Flow Rate Input"
        }
                
        payload =  {"deviceCode": self.devices[dev]["device_code"], "protocalCodes":["Power","Mode","Manual-mute","T01","T02","2074","2075","2076","2077","H03","Set_Temp","R08","R09","R10","R11","R01","R02","R03","T03","1158","1159","F17","H02","T04","T05","T07","T14","T17"] }
        r = requests.post(self._cloudURL+"/app/device/getDataByCode", headers=self._header, json=payload)
        if r.json()["error_code"] == "0":
            statusMap = {}
            for d in r.json()["objectResult"]:
                statusMap[d["code"]] = d["value"]
            return statusMap
        else:
            logging.debug(f"Get status not successful. Error message {r.json()['error_msg']}") 
    

