import requests
import sys
import yagmail
import socket


def get_ip(_provider):
    try:
        resp = requests.get(_provider).text.rstrip('\n')
    except Exception as ex:
        print(f'Cannot get ip from provider {_provider} because {ex}')
        sys.exit(1)
    else:
        return resp

def get_local_ip(_dns):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((_dns, 80))
    except Exception as ex:
        print(f'Cannot get local ip because {ex}')
        s.close()
        sys.exit(1)
    else:
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip


def save_ip_to_file(_ip, _filename):
    with open(_filename, 'r+') as f:
        actual = f.readline()
        if actual != _ip:
            f.write(_ip)


def send_ip_mail(_to, _ips):
    if '@' not in _to:
        print('No mail sent. Bye')
        return

    print('Insert GMAIL SMTP login:')
    user = input()
    print('Insert GMAIL SMTP password:')
    passwd = input()
    yag = yagmail.SMTP(user, passwd)
    yag.send(_to, f'Your ip addresses are {_ips}', _ips)


if __name__ == "__main__":
    print('Hi, this is the ip-notify script')

    provider = 'https://ifconfig.io/ip'
    ip = get_ip(provider)
    print(f'Your ip is {ip}')
    save_ip_to_file(ip, 'myip.txt')

    dns = '8.8.8.8'
    local_ip = get_local_ip(dns)
    print(f'Your local ip is {local_ip}')
    save_ip_to_file(local_ip, 'mylocalip.txt')

    print('Do you want to send email notification? Insert your address here:')
    to = input()
    send_ip_mail(to, [ip, local_ip])


