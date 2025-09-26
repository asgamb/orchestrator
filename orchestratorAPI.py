from flask import Flask
from flask_restplus import Resource, Api
import configparser
from controllers.ipm import IPM
from controllers.ipowdm import IPoWDM
from controllers.matrix import TapiMatrix
from controllers.pon import PON
import time




portx = 4000

# Flask and Flask-RestPlus configuration
app = Flask(__name__)
api = Api(app, version='1.0', title='Orch API',
          description='Orchestrator API for Turin demo. \nAuthor: Andrea Sgambelluri')
orch = api.namespace('Orchestrator', description='Orch APIs')

config = configparser.ConfigParser()

#Edgecore1 ports
if_HUB1 = "Ethernet0"
if_HUB2 = "Ethernet0"
if_SERVER = "Ethernet8"
if_XG1 = "Ethernet256"
if_XG2 = "Ethernet257"

#Edgecore2 ports
if_L1 = "Ethernet0"
if_L2 = "Ethernet8"
if_PC1 = "Ethernet256"
if_PC2 = "Ethernet257"

#matrix ports
if_OLT1 = "port1"
if_OLT2 = "port2"
if_B1 = "port3"
if_B2 = "port4"
if_H1 = "port5"
if_H2 = "port6"
if_XR1 = "port7"
if_XR2 = "port8"
if_PON1 = "port9"
if_PON2 = "port10"
if_M1 = "port11"
if_M2 = "port12"


ip_client = None
ip_en = 0
ipm_client = None
ipm_en = 0
matrix_client = None
matrix_en = 0
pon_client = None
pon_en = 0


def provisioning1():
    print("provisioning first step")
    if matrix_en:
        print("Matrix setup")
        print("connections H1-XR1 and M1-B1")
        message = {
            "tapi-connectivity:connectivity-service": [
                {
                    "connectivity-direction": "UNIDIRECTIONAL",
                    "end-point": [
                        {
                            "direction:": "INPUT",
                            "layer-protocol-name": "PHOTONIC_MEDIA",
                            "layer-protocol-qualifier": "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_OTS",
                            "local-id": "372a015b-33d2-5a85-8cd0-3afe405777c0",
                            "service-interface-point": {
                                "service-interface-point-uuid": "372a015b-33d2-5a85-8cd0-3afe405777c0"
                            },
                        },
                        {
                            "direction:": "OUTPUT",
                            "layer-protocol-name": "PHOTONIC_MEDIA",
                            "layer-protocol-qualifier": "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_OTS",
                            "local-id": "7e843608-34e0-5393-b15d-64be5bdd6f7d",
                            "service-interface-point": {
                                "service-interface-point-uuid": "7e843608-34e0-5393-b15d-64be5bdd6f7d"
                            },
                        },
                    ],
                    "layer-protocol-name": "PHOTONIC_MEDIA",
                    "layer-protocol-qualifier": "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_OTS",
                    "route-objective-function": "UNSPECIFIED",
                    "uuid": "d58eb429-4594-46fc-a0f9-dd639762b44a",
                }
            ]
        }
        matrix_client.create_connectivity_service(message)
    if ipm_en:
        print("IPM setup")
        ipm_client.set_constrellation1()
        time.sleep(10)
        ipm_client.set_service1()
        time.sleep(10)
    if ip_en:
        print("IPoWDM setup")
        print("creating vlan 1001 in the 2 edgecore switches")
        ip_client.set_vlan(1, 1001)
        print("Edgecore1 HUB: adding interfaces to vlan 1001")
        ip_client.set_vlan_member_single(1, 1, if_HUB1, 1001, 0) #XR
        ip_client.set_vlan_member_single(1, 1, if_SERVER, 1001, 0) #client
        print("Edgecore2 leaves: adding interfaces to vlan 1001")
        ip_client.set_vlan_member_single(1, 2, if_L1, 1001, 0) #XR
        ip_client.set_vlan_member_single(1, 2, if_PC1, 1001, 1) #client


def provisioning2():
    print("provisioning second step")
    if matrix_en:
        print("Matrix setup")
        print("connections OLT1-PON1")
        message = {
            "tapi-connectivity:connectivity-service": [
                {
                    "connectivity-direction": "UNIDIRECTIONAL",
                    "end-point": [
                        {
                            "direction:": "INPUT",
                            "layer-protocol-name": "PHOTONIC_MEDIA",
                            "layer-protocol-qualifier": "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_OTS",
                            "local-id": "372a015b-33d2-5a85-8cd0-3afe405777c0",
                            "service-interface-point": {
                                "service-interface-point-uuid": "372a015b-33d2-5a85-8cd0-3afe405777c0"
                            },
                        },
                        {
                            "direction:": "OUTPUT",
                            "layer-protocol-name": "PHOTONIC_MEDIA",
                            "layer-protocol-qualifier": "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_OTS",
                            "local-id": "7e843608-34e0-5393-b15d-64be5bdd6f7d",
                            "service-interface-point": {
                                "service-interface-point-uuid": "7e843608-34e0-5393-b15d-64be5bdd6f7d"
                            },
                        },
                    ],
                    "layer-protocol-name": "PHOTONIC_MEDIA",
                    "layer-protocol-qualifier": "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_OTS",
                    "route-objective-function": "UNSPECIFIED",
                    "uuid": "d58eb429-4594-46fc-a0f9-dd639762b44a",
                }
            ]
        }
        matrix_client.create_connectivity_service(message)
    if pon_en:
        print("PON setup")
        pon_client.set_pon(1, 1)
    if ip_en:
        print("IPoWDM setup")
        print("creating vlan 333 in the HUB edgecore")
        ip_client.set_vlan_single(1, 1, 333)
        print("Edgecore1 HUB: adding interfaces to vlan 1001")
        ip_client.set_vlan_member_single(1, 1, if_XG1, 333, 0) #XG interface OLT1
        ip_client.set_vlan_member_single(1, 1, if_SERVER, 333, 0) #server


def provisioning3():
    print("provisioning third step")
    if matrix_en:
        print("Matrix setup")
        print("connections H2-XR2 and M2-B2")
        message = {
            "tapi-connectivity:connectivity-service": [
                {
                    "connectivity-direction": "UNIDIRECTIONAL",
                    "end-point": [
                        {
                            "direction:": "INPUT",
                            "layer-protocol-name": "PHOTONIC_MEDIA",
                            "layer-protocol-qualifier": "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_OTS",
                            "local-id": "372a015b-33d2-5a85-8cd0-3afe405777c0",
                            "service-interface-point": {
                                "service-interface-point-uuid": "372a015b-33d2-5a85-8cd0-3afe405777c0"
                            },
                        },
                        {
                            "direction:": "OUTPUT",
                            "layer-protocol-name": "PHOTONIC_MEDIA",
                            "layer-protocol-qualifier": "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_OTS",
                            "local-id": "7e843608-34e0-5393-b15d-64be5bdd6f7d",
                            "service-interface-point": {
                                "service-interface-point-uuid": "7e843608-34e0-5393-b15d-64be5bdd6f7d"
                            },
                        },
                    ],
                    "layer-protocol-name": "PHOTONIC_MEDIA",
                    "layer-protocol-qualifier": "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_OTS",
                    "route-objective-function": "UNSPECIFIED",
                    "uuid": "d58eb429-4594-46fc-a0f9-dd639762b44a",
                }
            ]
        }
        matrix_client.create_connectivity_service(message)
    if ipm_en:
        print("IPM setup")
        c_id = ipm_client.get_constellation()
        print(c_id)
        ipm_client.set_constrellation2()
        time.sleep(10)
        ipm_client.set_service2()
        time.sleep(10)
    if ip_en:
        print("IPoWDM setup")
        print("creating vlan 1001 in the 2 edgecore switches")
        ip_client.set_vlan(1, 1002)
        print("Edgecore1 HUB: adding interfaces to vlan 1001")
        ip_client.set_vlan_member_single(1, 1, if_HUB2, 1002, 0) #XR
        ip_client.set_vlan_member_single(1, 1, if_SERVER, 1002, 0) #client
        print("Edgecore2 leaves: adding interfaces to vlan 1001")
        ip_client.set_vlan_member_single(1, 2, if_L2, 1002, 0) #XR
        ip_client.set_vlan_member_single(1, 2, if_PC2, 1002, 1) #client


def provisioning4():
    print("provisioning fourth step")
    if matrix_en:
        print("Matrix setup")
        print("connections OLT2-PON2")
        message = {
            "tapi-connectivity:connectivity-service": [
                {
                    "connectivity-direction": "UNIDIRECTIONAL",
                    "end-point": [
                        {
                            "direction:": "INPUT",
                            "layer-protocol-name": "PHOTONIC_MEDIA",
                            "layer-protocol-qualifier": "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_OTS",
                            "local-id": "372a015b-33d2-5a85-8cd0-3afe405777c0",
                            "service-interface-point": {
                                "service-interface-point-uuid": "372a015b-33d2-5a85-8cd0-3afe405777c0"
                            },
                        },
                        {
                            "direction:": "OUTPUT",
                            "layer-protocol-name": "PHOTONIC_MEDIA",
                            "layer-protocol-qualifier": "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_OTS",
                            "local-id": "7e843608-34e0-5393-b15d-64be5bdd6f7d",
                            "service-interface-point": {
                                "service-interface-point-uuid": "7e843608-34e0-5393-b15d-64be5bdd6f7d"
                            },
                        },
                    ],
                    "layer-protocol-name": "PHOTONIC_MEDIA",
                    "layer-protocol-qualifier": "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_OTS",
                    "route-objective-function": "UNSPECIFIED",
                    "uuid": "d58eb429-4594-46fc-a0f9-dd639762b44a",
                }
            ]
        }
        matrix_client.create_connectivity_service(message)
    if pon_en:
        print("PON setup")
        pon_client.set_pon(1, 2)
    if ip_en:
        print("IPoWDM setup")
        print("creating vlan 222 in the HUB edgecore")
        ip_client.set_vlan_single(1, 1, 222)
        print("Edgecore1 HUB: adding interfaces to vlan 1001")
        ip_client.set_vlan_member_single(1, 1, if_XG2, 222, 0) #XG interface OLT1
        ip_client.set_vlan_member_single(1, 1, if_SERVER, 222, 0) #server




@orch.route('/step/<int:step>')
@orch.response(200, 'Success')
@orch.response(404, 'Error, not found')
class _orchestration(Resource):
    @orch.doc(description="simpleAPI")
    @staticmethod
    def put(step):
        if step == 1:
            provisioning1()
        if step == 2:
            provisioning2()
        if step == 3:
            provisioning3()
        if step == 4:
            provisioning4()
        return "OK", 200


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.conf')
    """
    [ipowdm]
    enabled=0
    ip1 = 10.5.1.131
    ip2 = 10.5.1.132
    """
    if 'ipowdm' in config:
        if config['ipowdm']['enabled'] == "1":
            ip_en = 1
            ip1 = config['ipowdm']['ip1']
            ip2 = config['ipowdm']['ip2']
            test = config['ipowdm']['testing']
            ip_client = IPoWDM(ip1, ip2, test)

    """
    [pon]
    enabled=0
    ponIP = 10.5.1.131
    ponPort = 9092
    """
    if 'pon' in config:
        if config['pon']['enabled'] == "1":
            pon_en = 1
            pon_ip = config['pon']['ponIP']
            pon_port = config['pon']['ponPort']
            test = config['pon']['testing']
            pon_client = PON(pon_ip, pon_port, test)
    """
    [matrix]
    enabled=0
    matrixIP = 10.5.1.153
    matrixPort = 8888
    """
    if 'matrix' in config:
        if config['matrix']['enabled'] == "1":
            matrix_en = 1
            m_ip = config['matrix']['matrixIP']
            m_port = config['matrix']['matrixPort']
            test = config['matrix']['testing']
            matrix_client = TapiMatrix(m_ip, m_port, test)
    """
    [ipm]
    enabled=0
    ipm_IP = "192.168.1.1"
    ipm_Port = "8888"
    ipm_user = "xr-user-1"
    ipm_pswd = "infinera11"
    """
    if 'ipm' in config:
        if config['ipm']['enabled'] == "1":
            ipm_en_en = 1
            ipm_ip = config['ipm']['ipm_IP']
            ipm_port = config['ipm']['ipm_Port']
            ipm_user = config['ipm']['ipm_user']
            ipm_pswd = config['ipm']['ipm_pswd']
            test = config['ipm']['testing']
            ipm_client = IPM(ipm_ip, int(ipm_port), ipm_user, ipm_pswd, test)
    app.run(host='0.0.0.0', port=portx)
