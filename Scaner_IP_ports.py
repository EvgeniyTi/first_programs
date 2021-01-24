import socket
from netaddr import IPRange
from multiprocessing import Pool


def port_scan(user_host):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect(user_host)
        return f"{user_host[0]} Port: {user_host[1]} is open"
    except socket.error:
        pass
    finally:
        s.close()


print('-' * 36)
ipStart, ipEnd = input("Enter IP-IP: ").split('-')
iprange = IPRange(ipStart, ipEnd)
port = [43, 80, 109, 110, 115, 118, 119, 143, 194, 220, 443, 540, 585, 591, 1112, 1433, 1443,
        3128, 3197, 3306, 3899, 4224, 4444, 5000, 5432, 6379, 8000, 8080, 10000]
print('-' * 36)


if __name__ == '__main__':
    pool = Pool(20)
    list_ip = []
    for ip in iprange:
        host = str(ip)
        for pt in port:
            list_ip.append((host, pt))
        if len(list_ip) == len(port):
            p = pool.map(port_scan, list_ip)
            list_ip.clear()
            for i in p:
                if i is not None:
                    print(i)
