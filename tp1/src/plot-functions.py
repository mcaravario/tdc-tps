# look at http://standards.ieee.org/develop/regauth/ethertype/eth.txt
protocol_title = {
    '802.3': '802.3',
    '2048': 'IPv4',
    '2054': 'ARP',
    '26734': 'IEEE_26734',
    '33079': 'IPX',
    '34525': 'IPv6',
    '34958': '802.1X',
    '34983': 'Huawei_88A7',
    '35020': 'LLDP',
}
def get_protocol_title(s):
  if s in protocol_title:
    return protocol_title[s]
  else:
    return 'unknown_%s'%s

