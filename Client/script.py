import datetime
import os

import psutil
import json
import time
import requests

apps = ['pycharm64.exe', 'pycharm', 'devenv.exe', 'Code.exe', 'idea64.exe', 'clion64.exe', 'eclipse.exe']

class Report:
    def __init__(self, host, cpu, ram, disk, uptime):
        self.host = host
        self.cpu = cpu
        self.ram = ram
        self.disk = disk
        self.uptime = uptime

class Progress:
    def __init__(self, host, process, time, lines):
        self.host = host
        self.process = process
        self.time = time
        self.lines = lines

reports = {}
progresses = {}

url = 'http://127.0.0.1:5000/'

for u in psutil.users():
    host = u.name

def collect():
    global reports
    #collecting all utils
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    boot = psutil.boot_time()
    timern = datetime.datetime.now()
    uptime = (timern - datetime.datetime.fromtimestamp(boot)).total_seconds()
    reports[host] = Report(host, cpu, ram, disk, uptime)
    print(json.dumps(reports[host].__dict__))

    found = 0
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in apps:
            found = 1
            print(proc.info)
            p = psutil.Process(proc.pid)
            timern = datetime.datetime.now()
            apptime = (timern - datetime.datetime.fromtimestamp(p.create_time())).total_seconds()
            print(apptime)
            process = p.name()
            print(process)
    for f in os.listdir('..'):
        if f.endswith('.py'):
            cont = open(f, 'r').read()
            line_count = cont.count('\n')
            lines =+ line_count
    if found == 0:
        apptime = 'N/A'
        process = 'N/A'
    progresses[host] = Progress(host, process, apptime, lines)
    print(json.dumps(progresses[host].__dict__))


def token_get():
    global token
    print("Awaiting for authorization...")
    if role == 'script':
        token = requests.post(f'{url}auth?host={host}&role={role}')
    elif role == 'admin':
        token = requests.post(f'{url}auth?host={host}&role={role}&password={password}')

def scrpt():
    while True:
        if token.status_code != 200:
            print(f"Auth failed. Code: {token.status_code}\n"
                  f"Writing logs to file.\n"
                  f"Retrying connection in 10 seconds.")
            collect()
            open('latestlogs_stats.txt', 'w').write(json.dumps(reports[host].__dict__))
            open('latestlogs_progs.txt', 'w').write(json.dumps(progresses[host].__dict__))
            time.sleep(10)
            token_get()
        elif token.status_code == 200:
            print(f"Auth successful. Code: {token.status_code}")
            while True:
                if os.path.exists(f'latestlogs_stats.txt'):
                    data = json.load(open(f'latestlogs_stats.txt', 'r'))
                    reports[host] = Report(**data)
                    os.remove(f'latestlogs_stats.txt')
                    data = json.load(open(f'latestlogs_progs.txt', 'r'))
                    progresses[host] = Progress(**data)
                    os.remove(f'latestlogs_progs.txt')
                else:
                    collect()
                requests.post(f'{url}client?token={token.text}&data=stats', json=reports[host].__dict__)
                status = requests.post(f'{url}client?token={token.text}&data=prog', json=progresses[host].__dict__)
                if status.status_code != 200:
                    print(f"Connection failed. Code: {status.status_code} \n"
                        f"Reason: {status.reason}"
                        f"Saving info to file...")
                time.sleep(10)

print(f"Welcome to StatServ script! Please ensure that script is being run in directory, that contains .py files\n"
      f"Now, please enter URL of the StatServ Server to continue. (format: http://(url):5000/)")

url = input()
role = 'script'
token_get()
scrpt()
