import requests
import sys
import os
from colorama import init, Fore
import argparse
import base64
import urllib.parse


parser = argparse.ArgumentParser()
parser.add_argument('-u', help='Enter domain https://site.com')
parser.add_argument('-w', help='Name and path of the wordlist')
parser.add_argument('-b64', action='store_true', help='Format Base64')
parser.add_argument('-uenc', action='store_true', help='Format URLENCODE')
parser.add_argument('-head', help='Set parameters HTTP')

args = parser.parse_args()


init(autoreset=True)
Green = Fore.GREEN
Red = Fore.RED
Blue = '\033[94m'
Reset = Fore.RESET


DOMAIN = ""
DIRS = []


def greetings():
    """Функция отображает приветствие пользователя"""
    print(Green + '''
╔═══╗╔══╗╔═══╗     ╔═══╗╔╗─╔╗╔════╗╔════╗╔═══╗╔═══╗
╚╗╔╗║╚╣║╝║╔═╗║     ║╔══╝║║─║║╚══╗═║╚══╗═║║╔══╝║╔═╗║
─║║║║─║║─║╚═╝║     ║╚══╗║║─║║──╔╝╔╝──╔╝╔╝║╚══╗║╚═╝║
─║║║║─║║─║╔╗╔╝     ║╔══╝║║─║║─╔╝╔╝──╔╝╔╝─║╔══╝║╔╗╔╝
╔╝╚╝║╔╣║╗║║║╚╗     ║║───║╚═╝║╔╝═╚═╗╔╝═╚═╗║╚══╗║║║╚╗
╚═══╝╚══╝╚╝╚═╝     ╚╝───╚═══╝╚════╝╚════╝╚═══╝╚╝╚═╝
          ''' + Reset)


def check_wordlist_file(path_to_wordlist):
    """Функция проверяет наличие файла со словарём"""
    if not os.path.isfile(path_to_wordlist.replace("\'", "")):
        print(f"{path_to_wordlist}\nФайл со словарём не найден.")
        sys.exit(0)
    fill_dirs_from_file(path_to_wordlist)


def check_site_annotaion(hostname):
    """Функция проверяет есть ли коннект с хостом"""
    headers_ = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
    try:
        hostname = hostname.replace('FUZZ', '')
        diction = {}
        if args.head is not None:
            params = args.head.replace(',', ':').replace("'", '').split(': ')
            if ',' in args.head:
                diction[params[0]] = params[1]
                diction[params[2]] = params[3]
                response = requests.get(hostname, params=diction, timeout=1)
            else:
                diction[params[0]] = params[1]
                response = requests.get(hostname, params=diction, timeout=1)
        else:
            response = requests.get(hostname, params=headers_, timeout=1)

        response.raise_for_status()
        if response.status_code == 200:
            print('OK!')
    except (requests.exceptions.HTTPError, requests.exceptions.Timeout) as e:
        print('ERROR: %s' % e)

    set_url_format(hostname)


def set_url_format(hostname):
    """Функция проверяет форматирование url сайта"""
    global DOMAIN
    hostname = hostname.replace('FUZZ', '')
    if hostname[-1] != "/":
        hostname += "/"
    DOMAIN = hostname


def check_fuzz(hostname):
    if 'FUZZ' not in hostname:
        print(f"{Blue} To use the program, specify the domain and wordlist https://site.com/FUZZ /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt {Reset}")
        sys.exit()


def check_app_keys():
    """Функция проверяет правильность аргументов"""
    check_fuzz(args.u)
    # Доступность файла словаря
    check_wordlist_file(args.w)
    # Доступность хоста
    check_site_annotaion(args.u)
    print(f"\nРаботаем с сайтом {args.u}. Путь к словарю {args.w}\n")


def fill_dirs_from_file(dirs_file):
    """Функция читает файл с адресами папок в список"""
    with open(dirs_file, "r") as reader:
        for line in reader.readlines():
            DIRS.append(line)
    print("\nЗагружено строк из словаря: " + str(len(DIRS)) + "\n")


def get_site_dirs():
    """Функция проверки директорий"""
    counter = 0
    try:
        for target_dir in DIRS:
            target_url = []

            counter += 1
            if args.b64:
                base64_ = base64.b64encode(target_dir.strip().encode('utf-8'))
                base64_str = str(base64_, 'utf-8')
                target_url.append(DOMAIN + base64_str)
            elif args.uenc:
                url_encode = urllib.parse.quote(target_dir.strip())
                target_url.append(DOMAIN + url_encode)
            else:
                target_url.append(DOMAIN + target_dir.strip())

            host_answer = requests.get(DOMAIN + target_dir.strip() + "/", allow_redirects=False)

            with open('fuzz.txt', 'w', encoding='utf-8') as writer:
                if host_answer.status_code == 404:
                    print(' '*100, '\r', f"{counter:0>8} of {len(DIRS)}\t{Red}{host_answer.status_code}{Reset}\t{target_url[0]}/", end='\r')
                else:
                    if host_answer.status_code == 200:
                        print(' '*100, '\r', f"{counter:0>8} of {len(DIRS)}\t{Green}{host_answer.status_code}{Reset}\t{target_url[0]}/")
                    elif '4' in str(host_answer.status_code)[0]:
                        print(' '*100, '\r', f"{counter:0>8} of {len(DIRS)}\t{Red}{host_answer.status_code}{Reset}\t{target_url[0]}/")
                    elif '3' in str(host_answer.status_code)[0]:
                        print(' '*100, '\r', f"{counter:0>8} of {len(DIRS)}\t{Blue}{host_answer.status_code}{Reset}\t{target_url[0]}/")
                if host_answer.status_code != 404:
                    writer.writelines(f"{counter:0>8} of {len(DIRS)}\t{host_answer.status_code}\t{target_url}\n")

    except KeyboardInterrupt:
        print(Red + '  ERROR: manually stop Ctrl+C' + Reset)


if args.u is None and args.w is None:
    parser.print_help()
else:
    if __name__ == "__main__":
        greetings()
        check_app_keys()
        get_site_dirs()
