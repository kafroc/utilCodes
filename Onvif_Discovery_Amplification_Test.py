import socket
import sys

BUFSIZE = 4096
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(5)

msg = '''<Envelope><Header><wsa:MessageID xmlns:wsa=""></wsa:MessageID><wsa:To xmlns:wsa=""></wsa:To><wsa:Action xmlns:wsa="">http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</wsa:Action></Header><Body><Probe><Types></Types><Scopes /></Probe></Body></Envelope>'''

if len(sys.argv) != 2:
    print('Please input the ip address of destination host')
    exit(1)

ip_port = (sys.argv[1], 37810)
client.sendto(msg.encode('utf-8'), ip_port)

try:
    data, server_addr = client.recvfrom(BUFSIZE)
    print('Onvif Discovery 放大攻击测试\n\t发送长度：%d，接收长度：%d，放大倍数：%.2f' %
          (len(msg), len(data), len(data) / len(msg)))
except Exception as exp:
    print(exp)


client.close()
