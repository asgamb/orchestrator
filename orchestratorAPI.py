from flask import Flask
from flask_restplus import Resource, Api
import configparser
from controllers.ipm import IPM
from controllers.ipowdm import IPoWDM
from controllers.matrix import TapiMatrix
from controllers.pon import PON
import time

ip_client = None
ip_en = 0
ipm_client = None
ipm_en = 0
matrix_client = None
matrix_en = 0
pon_client = None
pon_en = 0


portx = 4000

# Flask and Flask-RestPlus configuration
app = Flask(__name__)
api = Api(app, version='1.0', title='Orch API',
          description='Orchestrator API for Turin demo. \nAuthor: Andrea Sgambelluri')
orch = api.namespace('Orchestrator', description='Orch APIs')

config = configparser.ConfigParser()


def provisioning():
    print("provisioning")
    if ip_en:
        print("IPoWDM setup")
        ip_client.conf_ip(1, 1, "Ethernt0", "192.168.1.1", "30")
        time.sleep(1)
        ip_client.set_vlan_member_single(1, 1, "Ethernet192", 10)
    if pon_en:
        print("PON setup")
        pon_client.set_pon(1, 1)
    if matrix_en:
        print("Matrix setup")
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
        ipm_client.set_constrellation1()
        time.sleep(1)
        ipm_client.set_service1()


@orch.route('/step/<int:step>')
@orch.response(200, 'Success')
@orch.response(404, 'Error, not found')
class _orchestration(Resource):
    @orch.doc(description="simpleAPI")
    @staticmethod
    def put(step):
        if step == 1:
            provisioning()
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
        if config['ipowdm']['enabled']:
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
        if config['pon']['enabled']:
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
        if config['matrix']['enabled']:
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
        if config['ipm']['enabled']:
            ipm_en_en = 1
            ipm_ip = config['ipm']['ipm_IP']
            ipm_port = config['ipm']['ipm_Port']
            ipm_user = config['ipm']['ipm_user']
            ipm_pswd = config['ipm']['ipm_pswd']
            test = config['ipm']['testing']
            ipm_client = IPM(ipm_ip, int(ipm_port), ipm_user, ipm_pswd, test)
    app.run(host='0.0.0.0', port=portx)
