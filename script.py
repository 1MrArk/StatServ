import datetime
import os

import psutil
import json
import time
import requests

class Report:
    def __init__(self, host, cpu, ram, disk, uptime):
        self.host = host
        self.cpu = cpu
        self.ram = ram
        self.disk = disk
        self.uptime = uptime

reports = {}

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
            open('latest_logs.txt', 'w').write(json.dumps(reports[host].__dict__))
            time.sleep(10)
            token_get()
        elif token.status_code == 200:
            print(f"Auth successful. Code: {token.status_code}")
            while True:
                if os.path.exists(f'latest_logs.txt'):
                    data = json.load(open(f'latest_logs.txt', 'r'))
                    reports[host] = Report(**data)
                    os.remove(f'latest_logs.txt')
                else:
                    collect()
                status = requests.post(f'{url}client?token={token.text}', json=reports[host].__dict__)
                if status.status_code != 200:
                    print(f"Connection failed. Code: {status.status_code} \n"
                        f"Reason: {status.reason}"
                        f"Saving info to file...")
                time.sleep(10)
def admin():
    while True:
        if token.status_code != 200:
            print(f"Auth failed. Code: {token.status_code}")
            time.sleep(10)
        elif token.status_code == 200:
            print(f"Auth successful. Code: {token.status_code}")
            while True:
                print(f"Choose an action:\n"
                      f"1. View all clients\n"
                      f"2. View client\n"
                      f"3. Delete client\n"
                      f"4. Delete specific user metric\n"
                      f"5. Exit\n")
                try:
                    action = int(input())
                    match action:
                        case 1:
                            data = requests.get(f'{url}admin?token={token.text}&action=view_all')
                            data = data.json()
                            for item in data:
                                print(f"Host: {item['host']}\n"
                                    f"CPU: {item['cpu']}\n"
                                    f"RAM: {item['ram']}\n"
                                    f"Disk: {item['disk']}\n"
                                    f"Uptime: {item['uptime']} seconds\n")
                        case 2:
                            user = input('Enter hostname: ')
                            data = requests.get(f'{url}admin?token={token.text}&action=view_user&user={user}')
                            data = data.json()
                            print(data)
                            if 'code' not in data:
                                print(f"Host: {data['host']}\n"
                                    f"CPU: {data['cpu']}\n"
                                    f"RAM: {data['ram']}\n"
                                    f"Disk: {data['disk']}\n"
                                    f"Uptime: {data['uptime']} seconds\n")
                            else:
                                print(f"No such user exists.\n")
                        case 3:
                            user = input('Enter hostname: ')
                            requests.get(f'{url}admin?token={token.text}&action=delete_user&user={user}')
                        case 4:
                            user = input('Enter hostname: ')
                            metric = input('Enter metric: ')
                            requests.get(f'{url}admin?token={token.text}&action=delete_metric&user={user}&metric={metric}')
                        case 5:
                            exit(0)
                        case _:
                            print("Invalid action")
                except ValueError:
                    print("Invalid input. Please try again.")

print(f"Welcome to StatServ script! Please ensure that: \n"
      f"1. You are using Windows operating system\n"
      f"2. Script is being run in directory, that contains .py files")

choice = input()
if choice == '1':
    role = 'script'
    token_get()
    scrpt()
elif choice == '2':
    role = 'admin'
    password = input('Enter password: ')
    token_get()
    admin()
else:
    print("Invalid choice")
    exit(0)