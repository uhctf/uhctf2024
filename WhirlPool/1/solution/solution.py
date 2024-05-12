from scapy.all import *

cap = rdpcap("../attachements/capture.pcap")

for p in cap:
    # https://www.rfc-editor.org/rfc/rfc3514
    if p[IP].flags == "evil":
        if Raw in p:
            print(p[Raw].load)