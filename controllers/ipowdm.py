import requests


class IPoWDM:
    def __init__(self, ip1, ip2, test=0):
        print("IPoWDM control enabled")
        self.ipowdms = {1: ip1, 2: ip2}
        self.headers = {"Content-Type": "application/json"}
        self.test = test
        if self.test:
            print("IPoWDM testing enabled")

    def set_ipowdm_ip(self, idx, ip):
        self.ipowdms[idx] = ip

    def set_freq(self, freq):
        #ip address, mask, interface
        url1 = f"http://{self.ipowdms[1]}:3105/Sonic/TransceiverFreqConfig/Ethernet192/{freq}/100"
        url2 = f"http://{self.ipowdms[2]}:3105/Sonic/TransceiverFreqConfig/Ethernet192/{freq}/100"
        print(url1)
        print(url2)
        if not self.test:
            r = requests.put(url1, headers=self.headers)
            r = requests.put(url2, headers=self.headers)

    def conf_2ips(self, settings, if1, ip1, mask1, if2, ip2, mask2):
        #ip address, mask, interface
        url1 = f"http://{self.ipowdms[1]}:3105/Sonic/Interface/{ip1}/{mask1}/{if1}"
        url2 = f"http://{self.ipowdms[2]}:3105/Sonic/Interface/{ip2}/{mask2}/{if2}"
        print(url1)
        print(url2)
        if not self.test:
            if settings == 1:
                r = requests.put(url1, headers=self.headers)
                r = requests.put(url2, headers=self.headers)
            else:
                r = requests.delete(url1, headers=self.headers)
                r = requests.delete(url2, headers=self.headers)

    def conf_ip(self, settings, idx, if1, ip1, mask1):
        #ip address, mask, interface
        url1 = f"http://{self.ipowdms[idx]}:3105/Sonic/Interface/{ip1}/{mask1}/{if1}"
        print(url1)
        if not self.test:
            if settings == 1:
                 r = requests.put(url1, headers=self.headers)
            else:
                r = requests.delete(url1, headers=self.headers)

    def add_routes(self, settings):
        #prefix, mask, next-hop
        url1 = f"http://{self.ipowdms[1]}:3105/Sonic/route/2.2.2.2/32/192.168.252.2"
        url2 = f"http://{self.ipowdms[2]}:3105/Sonic/route/1.1.1.1/32/192.168.252.1"
        print(url1)
        print(url2)
        if not self.test:
            if settings == 1:
                r = requests.put(url1, headers=self.headers)
                r = requests.put(url2, headers=self.headers)
            else:
                r = requests.delete(url1, headers=self.headers)
                r = requests.delete(url2, headers=self.headers)

    def set_l2vpn(self, settings):
        #localAS number, remAS number
        url1 = f"http://{self.ipowdms[1]}:3105/Sonic/l2vpn/65001/65001"
        url2 = f"http://{self.ipowdms[2]}:3105/Sonic/l2vpn/65001/65001"
        print(url1)
        print(url2)
        if not self.test:
            if settings == 1:
                r = requests.put(url1, headers=self.headers)
                r = requests.put(url2, headers=self.headers)
            else:
                r = requests.delete(url1, headers=self.headers)
                r = requests.delete(url2, headers=self.headers)

    def set_vlan_members(self, settings, interface, vlan_id, mode):
        #vlan_id, Interface
        url1 = f"http://{self.ipowdms[1]}:3105/Sonic/vlan_member/{vlan_id}/{interface}/{mode}"
        url2 = f"http://{self.ipowdms[2]}:3105/Sonic/vlan_member/{vlan_id}/{interface}/{mode}"
        print(url1)
        print(url2)
        if not self.test:
            if settings == 1:
                r = requests.put(url1, headers=self.headers)
                r = requests.put(url2, headers=self.headers)
            else:
                r = requests.delete(url1, headers=self.headers)
                r = requests.delete(url2, headers=self.headers)

    def set_vlan_member_single(self, settings, idx, interface, vlan_id, mode):
        url1 = f"http://{self.ipowdms[idx]}:3105/Sonic/vlan_member/{vlan_id}/{interface}/{mode}"
        print(url1)
        if not self.test:
            if settings == 1:
                r = requests.put(url1, headers=self.headers)
            else:
                r = requests.delete(url1, headers=self.headers)

    def set_vlan(self, settings, vlan_id):
        #vlan_id
        url1 = f"http://{self.ipowdms[1]}:3105/Sonic/vlan/{vlan_id}"
        url2 = f"http://{self.ipowdms[2]}:3105/Sonic/vlan/{vlan_id}"
        print(url1)
        print(url2)
        if not self.test:
            if settings == 1:
                r = requests.put(url1, headers=self.headers)
                r = requests.put(url2, headers=self.headers)
            else:
                r = requests.delete(url1, headers=self.headers)
                r = requests.delete(url2, headers=self.headers)

    def set_vlan_single(self, settings, idx, vlan_id):
        #vlan_id
        url1 = f"http://{self.ipowdms[idx]}:3105/Sonic/vlan/{vlan_id}"
        print(url1)
        if not self.test:
            if settings == 1:
                r = requests.put(url1, headers=self.headers)
            else:
                r = requests.delete(url1, headers=self.headers)

    def check_reach(self, idx, ip_addr):
        url1 = f"http://{self.ipowdms[idx]}:3105/Sonic/reach/{ip_addr}"
        print(url1)
        if not self.test:
            r = requests.put(url1, headers=self.headers)

    def set_vni(self, settings, vlan_id, vni):
        #vlan_id, vni
        url1 = f"http://{self.ipowdms[1]}:3105/Sonic/vni/{vlan_id}/{vni}"
        url2 = f"http://{self.ipowdms[2]}:3105/Sonic/vni/{vlan_id}/{vni}"
        print(url1)
        print(url2)
        if not self.test:
            if settings == 1:
                r = requests.put(url1, headers=self.headers)
                r = requests.put(url2, headers=self.headers)
            else:
                r = requests.delete(url1, headers=self.headers)
                r = requests.delete(url2, headers=self.headers)

'''
if __name__ == '__main__':
    print("provisioning")
    ec = IPoWDM("10.30.8.8", "10.30.8.9")
    print("Edgecore setup")
    #ec.set_freq(freqx)
    print("step 1: config plug IP address")
    ec.conf_ip(1, 1, "Ethernet0", "192.168.2.2", "29")
    #time.sleep(30)
    #check_reach(ipowdm2, ip1)
    print("step 2: add static route")
    ec.add_routes(1)
    #time.sleep(10)
    #step 3 create vlan 10
    print("step 3: set vlan 10")
    ec.set_vlan(1, 10)
    #time.sleep(10)
    print("step 4: create bgp l2vpn and vtep")
    ec.set_l2vpn(1)
    #time.sleep(15)
    print("step 5: add interfaces to mapped vlan 10")
    #set_vlan_members(1, "Ethernet192", 10)
    ec.set_vlan_member_single(1, 2, "Ethernet256", 10)
    ec.set_vlan_member_single(1, 1, "Ethernet257", 10)
    print("step 6: create vni vlan mapping")
    ec.set_vni(1, 10, 1000)

'''
