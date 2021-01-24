import socket
from multiprocessing import Process


def port_scan(hostname, port_num):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((hostname, port_num))
        print(hostname, 'Port:', port_num, "is open")
    except socket.error:
        pass
    finally:
        s.close()


print('-' * 36)
user_host = input('Введите название сайта: ')
host = user_host.replace('http://', '').replace('https://', '').replace('/', '')
remote_ip = socket.gethostbyname(host)
print('-' * 36)


if __name__ == '__main__':
    for port in range(65535):
        p = Process(target=port_scan, args=(remote_ip, port))
        p.start()
