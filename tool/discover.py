import nmap,socket

def get_my_ip():
  """
  Find my IP address
  :return:
  """
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  ip = s.getsockname()[0]
  s.close()
  return ip

def run():
    nm = nmap.PortScanner()
    ip_parts = get_my_ip().split('.')
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.1/24'
    nm.scan(hosts=base_ip, arguments='-n -sP -PE -PA21,23,80,3389')
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    hosts_list = list(dict.fromkeys(hosts_list))
    host = []
    for hosts ,status in hosts_list:
        host.append(hosts)
    return host
