import requests
import json
from requests.models import Response


def fake_response(status=200, json_data=None, text_data=None):
    resp = Response()
    resp.status_code = status

    if json_data is not None:
        import json
        resp._content = json.dumps(json_data).encode("utf-8")
        resp.headers["Content-Type"] = "application/json"
    elif text_data is not None:
        resp._content = text_data.encode("utf-8")
        resp.headers["Content-Type"] = "text/plain"
    else:
        resp._content = b""

    return resp


class TapiMatrix:
    def __init__(self, ip, port, test=0):
        print("TAPI matrix control enabled")
        self.name = f"{ip}:{port}"
        self.headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json"}
        self.test = test
        if self.test:
            print("TAPI matrix testing enabled")


    def create_connectivity_service(self, payload: dict):
        url = f"https://{self.name}/restconf/data/tapi-common:context/tapi-connectivity:connectivity-context"
        print(url)
        if not self.test:
            response = requests.post(url, headers=self.headers, json=payload)
            return response
        else:
            return fake_response(200)


'''
if __name__ == "__main__":
    # Example usage
    matrix = TapiMatrix("ip", 4900)
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

    resp = matrix.create_connectivity_service(message)
    print("Status:", resp.status_code)
    try:
        print("Response JSON:", resp.json())
    except json.JSONDecodeError:
        print("Response Text:", resp.text)
'''
