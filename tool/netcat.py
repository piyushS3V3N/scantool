import nmap
import socket
nm = nmap.PortScanner()
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
ip_parts = get_my_ip().split('.')
base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.1/24'
print(base_ip)
nm.scan(hosts=base_ip, arguments='-n -sP -PE -PA21,23,80,3389')

hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]

for host, status in hosts_list:
    print('{0}:{1}'.format(host, status))
