#!/usr/bin/env python
# -*- coding: utf-8 -*-

from memoized import memoized

# Global parameters, is this ok?
DEBUG = False
#DEBUG = True
VERBOSE = False
hops_max = 40
dns_server = "8.8.8.8"
dns_recursive = True
packets_per_hop = 50

# Constants, is this ok?
DNS_RCODE_OK = 0
DNS_RCODE_NAME_ERROR = 3
DNS_TYPE_A = 1
DNS_TYPE_PTR = 12

ID_GLOBAL = 1

@memoized
def is_valid_ipv4_address(address):
    """Devuelve True si la ip parámetro es válida"""
    import socket
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False
    return True

def traceroute(host):
    """
    Esta funcion recibe un hostname
    y realiza un traceroute a la
    dirección IP correspondiente

    (explicar diferencia con traceroute2)
    """
    hosts = []
    for ttl in range(1, 20):
        packet = IP(dst=url, ttl=ttl) / ICMP()
        ans = sr1(packet, verbose=0)
        host = ans[ICMP].underlayer.src
        print(host)
        hosts.append(host)
        if ans.type == 3:
            return hosts

@memoized
def dns_resolve(host):
    """
    Esta función recibe un hostname
    y lo traduce a una dirección IP.
    Es un request DNS, pero hecho a mano.

    Más info:
    http://itgeekchronicles.co.uk/2014/05/12/scapy-iterating-over-dns-responses/
    """
    from scapy.all import sr1, IP, UDP, DNS, DNSQR
    rd = 1 if dns_recursive else 0
    res = sr1(IP(dst=dns_server)/UDP()/DNS(rd=1,qd=DNSQR(qname=host)), timeout=.5, verbose=VERBOSE)
    if res == None or res[DNS].rcode != DNS_RCODE_OK:
        raise Exception('''\n\nLa query DNS para el host "%s" devolvio un código de error\nEs posible que el dominio no exista.'''%host)
    answers = res[DNS].an
    count = res[DNS].ancount
    while count > 0:
        count -= 1
        if answers[count].type == DNS_TYPE_A:
            return answers[count].rdata
    raise Exception('\n\nLa query DNS para el host "%s" no devolvió ningún registro de clase A.\nNo es posible continuar.'%host)

@memoized
def reverse_dns_resolve(ip):
    from scapy.all import sr1, IP, UDP, DNS, DNSQR
    if DEBUG: print("Resolviendo el DNS inverso de %s"%ip)
    reversed_ip = ".".join([o for o in reversed(ip.split("."))])
    res = sr1(IP(dst=dns_server)/UDP()/DNS(rd=1,qd=DNSQR(qname='%s.in-addr.arpa'%reversed_ip, qtype='PTR')), timeout=.5, verbose=VERBOSE)
    if(res == None):
        return "???"
    #if res[DNS].rcode != DNS_RCODE_OK:
    #    raise Exception('''\n\nLa query DNS para el host "%s" devolvio un código de error\nEs posible que el dominio no exista.'''%host)
    answers = res[DNS].an
    count = res[DNS].ancount
    while count > 0:
        count -= 1
        if answers[count].type == DNS_TYPE_PTR:
            return answers[count].rdata[:-1]
    #raise Exception('\n\nLa query reverse-DNS para la IP "%s" no devolvió ningún registro de clase PTR.\n'%host)
    return "???"

@memoized
def get_ip_from_parameter(host):
    """
    Esta función recibe un parámetro,
    y devuelve una IP válida a partir del mismo
    (o levanta una excepción)
    """
    dst_ip = host if is_valid_ipv4_address(host) else dns_resolve(host)
    if not is_valid_ipv4_address(dst_ip): raise Exception("\n\nLa IP %s correspondiente al parametro %s no parece ser válida."%(dst_ip,host))
    return dst_ip     

def traceroute_sr1_to_ans_i(dst_ip,ttl_seq,timeout):
    """
    Esta funcion recibe una ip destino, un ttl, y un timeout
    y realiza un echo-request; devuelve un diccionario r
    con los pormenores del resultado.

    r['ans']   = answered requests
    r['unans'] = unanswered requests
    r['time']  = tiempo desde request hasta recibir el reply
    r['host']  = host que respondio el reply
    r['hosname']  = hostname (DNS-inverso) que respondio el reply
    """
    from scapy.all import sr, sr1, ICMP, TCP, IP, RandShort
    import datetime
    r = {}
    #r['sr1'] = sr1(IP(dst=dst_ip, ttl=ttl_seq, id=RandShort()) / TCP(flags=0x2), timeout=2, retry=0, verbose=VERBOSE)
    global ID_GLOBAL
    ID_GLOBAL += 1
    packet = IP(dst=dst_ip, ttl=ttl_seq, id=ID_GLOBAL) / ICMP(type="echo-request")
    start = datetime.datetime.now()
    r['ans'],r['unans'] = sr(packet, timeout=0.5, retry=0, verbose=VERBOSE)
    end = datetime.datetime.now()
    # python time
    #r['start_time'] = start
    #r['end_time'] = end
    #r['delta_time'] = end-start
    #r['time'] = "%s ms"%int(round( r['delta_time'].total_seconds() * 1000 ))
    if r['ans'] != None and len(r['ans']) >= 1 and len(r['ans'][0]) >= 2:
        r['host'] = r['ans'][0][1][IP].src
        r['hostname'] = reverse_dns_resolve(r['host'])
        # packet time
        r['p_start_time'] = r['ans'][0][0].time
        r['p_end_time'] = r['ans'][0][1].time
        r['p_delta_time'] = r['p_end_time']-r['p_start_time']
        r['time'] = "%s ms"%int(round( r['p_delta_time'] * 1000 ))
    else:
        r['host'] = "*"
        r['hostname'] = "*"
        r['time'] = "*"
    return r

def traceroute2(parameter):
    """
    Esta funcion recibe un hostname
    y realiza un traceroute a la
    dirección IP correspondiente

    (explicar diferencia con traceroute)
    """
    dst_ip = get_ip_from_parameter(parameter)
    rcv,snd,ttl_seq = None,None,1
    print("traceroute to %s (%s), hops max %s"%(url,dst_ip,hops_max))
    hops_list = []
    while (not rcv or host!=dst_ip) and ttl_seq<=hops_max:
        print("Hop #%s"%ttl_seq)
        ans = {}
        host = "?"
        hop_list = list()
        for i in range(0,packets_per_hop):
            ans[i] = rcv = traceroute_sr1_to_ans_i(dst_ip, ttl_seq, 2)
            host = ans[i]['host']
            print("\t{:>15s} {:40s}".format(ans[i]['host'],'(%s)'%ans[i]['hostname'])),
            print("\t{:6s}".format(ans[i]['time']))
            res = {}
            res['ip'] = ans[i]["host"]
            res['hostname'] = ans[i]["hostname"]
            res["rtt"] = ans[i]["time"]
            hop_list.append(res)
        hops_list.append(hop_list)
        ttl_seq += 1
    return hops_list

if __name__ == "__main__":
    from functions import *
    import json
    check_sudo()
    import sys
    url = sys.argv[1] if len(sys.argv)>1 else 'news.ycombinator.com'
    traceroute_out = traceroute2(url)
    with open(url + '.json', 'w') as f:
        f.write(json.dumps(traceroute_out, indent=4))
