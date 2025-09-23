import requests


class PON:
    def __init__(self, ip, port, test=0):
        print("PON control enabled")
        self.headers = {"Content-Type": "application/json"}
        self.name = f"{ip}:{port}"
        self.test = test
        if self.test:
            print("PON testing enabled")

    def set_pon(self, setting, idx):
        url1 = f"http://{self. name}/api/service"
        print(url1)
        if setting == 1:
            if idx == 2:
                data_message = {"ont_id": "2", "cvlan": "0", "ethernet_port": "2", "svlan": "333", "profile": "be", "bw": "0"}
            elif idx == 1:
                data_message = {"ont_id": "1", "cvlan": "0", "ethernet_port": "1", "svlan": "222", "profile": "be", "bw": "0"}
            print(data_message)
            if not self.test:
                r = requests.post(url1, headers=self.headers, json=data_message)
                print(r.text)
                print(r)
        elif setting == 0:
            if idx == 2:
                data_message = {"ont_id": "2", "cvlan": "0", "ethernet_port": "2", "svlan": "333", "profile": "be", "bw": "0"}
            elif idx == 1:
                data_message = {"ont_id": "1", "cvlan": "0", "ethernet_port": "1", "svlan": "222", "profile": "be", "bw": "0"}
            print(data_message)
            if not self.test:
                r = requests.delete(url1, headers=self.headers, json=data_message)
                print(r.text)
                print(r)


'''
if __name__ == '__main__':
    pon = PON("10.30.2.2", 3004)
    print("PON setup")
    pon.set_pon(1, 1)
    pon.set_pon(0, 1)
    '''
