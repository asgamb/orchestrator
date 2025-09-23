import requests
import time
import json


class IPM:
    def __init__(self, ipm_address, ipm_port, user, password, test=0):
        print("IPM control enabled")
        self.ipm_address = ipm_address
        self.test = test
        self.ipm_port = ipm_port
        self.version = "1.0"
        self.user = user
        self.pswd = password
        self.token = self.create_token()
        self.token_timestamp = time.time()
        self.const_id = ""
        if self.test:
            print("IPM testing enabled")

    def create_token(self):
        body = {
            "username": self.user,
            "password": self.pswd,
            "grant_type": "password",
            "client_secret": "xr-web-client",
            "client_id": "xr-web-client"
        }
        return self.https_openid(body)

    def set_token(self, token):
        self.token = token

    def set_const_id(self, c_id):
        self.const_id = c_id

    def https_openid(self, body):
        url = f"https://{self.ipm_address}:{self.ipm_port}/realms/xr-cm/protocol/openid-connect/token"
        headers = {
            "User-Agent": self.version,
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br"
        }
        if not self.test:
            response = requests.post(url, data=body, headers=headers, verify=False)
            response.raise_for_status()  # raises error if status != 200
            # TODO
            # get the token from the response
            return str(response.json())
        else:
            return "ALJLDJKDçç;SM"

    def check_token(self):
        if time.time() - self.token_timestamp > 3000:
            print("More than 3000 seconds have elapsed")
            self.set_token(self.create_token())
        else:
            print("Token is still valid")

    def set_constrellation1(self):
        url = "https://infinera-ipm.cselt.it/api/v1/xr-networks"
        self.check_token()
        message = {
            "config": {
                "name": "H-2L-single-fiber",
                "constellationFrequency": 194000000,
                "modulation": "16QAM",
                "tcMode": True,
                "topology": "auto",
                "cTEOptimization": "disabled"
            },
            "hubModule": {
                "selector": {
                    "moduleSelectorByModuleName": {
                        "moduleName": "HUB-Edge1-P9"
                    }
                },
                "module": {
                    "plannedCapacity": "200G",
                    "fiberConnectionMode": "single",
                    "requestedNominalPsdOffset": "0dB",
                    "trafficMode": "L1Mode",
                    "fecIterations": "standard",
                    "txCLPtarget": 100
                }
            },
            "leafModules": [
                {
                    "selector": {
                        "moduleSelectorByModuleName": {
                            "moduleName": "Leaf1-Edge3-P1"
                        }
                    },
                    "module": {
                        "plannedCapacity": "100G",
                        "fiberConnectionMode": "single",
                        "requestedNominalPsdOffset": "0dB",
                        "trafficMode": "L1Mode",
                        "fecIterations": "standard",
                        "txCLPtarget": -9900
                    }
                }
            ]
        }
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        print(url)
        print(message)
        print(headers)
        if not self.test:
            response = requests.post(url, headers=headers, json=message)
            print(response.status_code)
            print(response.json())

    def set_service1(self):
        url = "https://infinera-ipm.cselt.it/api/v1/network-connections"
        self.check_token()
        message = {
            "name": "H-T1-L1",
            "serviceMode": "XR-L1",
            "implicitTransportCapacity": "portMode",
            "endpoints": [
                {
                    "selector": {
                        "moduleIfSelectorByModuleName": {
                            "moduleName": "HUB-Edge1-P9",
                            "moduleClientIfAid": "XR-T1"
                        }

                    }
                },
                {
                    "selector": {
                        "moduleIfSelectorByModuleName": {
                            "moduleName": "Leaf1-Edge3-P1",
                            "moduleClientIfAid": "XR-T1"
                        }
                    }
                }
            ]
        }
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        print(url)
        print(message)
        print(headers)
        if not self.test:
            response = requests.post(url, headers=headers, json=message)
            print(response.status_code)
            print(response.json())

    def get_constellation(self):
        url = "https://infinera-ipm.cselt.it/api/v1/xr-networks"
        self.check_token()
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        print(url)
        print(headers)
        if not self.test:
            response = requests.get(url, headers=headers)
            print(response.status_code)
            print(response.json())
            '''
            [
                {
                    "href": "/xr-networks/<ID-CONSTELLATION>",
                    "rt": [
                        "cm.xr-network"
                    ]
                }
            ]
            '''
            data = json.loads(response)
            id_constellation = data[0]["href"].split("/")[-1]
            print(id_constellation)  # 👉 ABC12345
        else:
            id_constellation = "0xxx1"
            self.set_const_id(id_constellation)

    def set_constrellation2(self):
        url = f"https://infinera-ipm.cselt.it/api/v1/xr-networks/{self.const_id}"
        self.check_token()
        message = {
            "selector": {
                "moduleSelectorByModuleName": {
                "moduleName": "Leaf2-Edge3-P5"
                }
            },
            "module": {
                "plannedCapacity": "100G",
                "fiberConnectionMode": "single",
                "requestedNominalPsdOffset": "0dB",
                "trafficMode": "L1Mode",
                "fecIterations": "standard",
                "txCLPtarget": -9900
            }
        }
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        print(url)
        print(message)
        print(headers)
        if not self.test:
            response = requests.post(url, headers=headers, json=message)
            print(response.status_code)
            print(response.json())

    def set_service2(self):
        url = "https://infinera-ipm.cselt.it/api/v1/network-connections"
        self.check_token()
        message = {
            "name": "H-T3-L1",
            "serviceMode": "XR-L1",
            "implicitTransportCapacity": "portMode",
            "endpoints": [
              {
                "selector": {
                  "moduleIfSelectorByModuleName": {
                     "moduleName": "HUB-Edge1-P9",
                     "moduleClientIfAid": "XR-T3"
                  }
                }
              },
              {
                "selector": {
                  "moduleIfSelectorByModuleName": {
                     "moduleName": "Leaf2-Edge3-P5",
                     "moduleClientIfAid": "XR-T1"
                }
              }
              }
            ]
        }
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        print(url)
        print(message)
        print(headers)
        if not self.test:
            response = requests.post(url, headers=headers, json=message)
            print(response.status_code)
            print(response.json())

'''
if __name__ == '__main__':
    print("provisioning")
    ipm = IPM("ipm", 443, "xr-user-1", "infinera11")
    ipm.set_constrellation1()
    ipm.set_service1()
    ipm.get_constellation()
    ipm.set_constrellation2()
    ipm.set_service2()
'''
