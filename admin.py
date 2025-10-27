from tkinter import *
import psutil
import requests

URL = 'http://127.0.0.1:5000/'

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        Label(self.root, text="URL").grid(row=0, column=0)
        self.url_entry = Entry(self.root, width=20)
        self.url_entry.grid(row=0, column=1)
        Label(root, text="Password:").grid(row=1, column=0)
        self.password_entry = Entry(root, show="*")
        self.password_entry.grid(row=1, column=1)
        Button(root, text="Login", command=self.login).grid(row=2, column=1)

    def login(self):
        password = self.password_entry.get()
        token_get(password)
        if token.status_code == 200:
            for widget in self.root.winfo_children():
                widget.destroy()
            load_data()

class Table:
    def __init__(self, root, data, columns_stats, columns_prog):
        stats = data['stats']
        prog = data['prog']
        for i, row in enumerate(stats):
            for j, key in enumerate(columns_stats):
                s = Label(root, text=row[key], width=10)
                s.grid(row=i+2, column=j)
                Label(root, text="System utilisation table:").grid(row=0, column=2)
                Label(root, text="Hostname").grid(row=1, column=0)
                Label(root, text="CPU (%)").grid(row=1, column=1)
                Label(root, text="RAM (%)").grid(row=1, column=2)
                Label(root, text="Disk usage (%)").grid(row=1, column=3)
                Label(root, text="Uptime (sec)").grid(row=1, column=4)
                Button(root, text="Delete", command=lambda h=row['host']: delete_user(h)).grid(row=i+2, column=len(
                    columns_stats) + 1)
        for i, row in enumerate(prog):
            for j, key in enumerate(columns_prog):
                p = Label(root, text=row[key], width=10)
                p.grid(row=i+5+len(stats), column=j)
                Label(root, text="Progress table:").grid(row=len(stats)+3, column=2)
                Label(root, text="Hostname").grid(row=len(stats)+4, column=0)
                Label(root, text="IDE").grid(row=len(stats)+4, column=1)
                Label(root, text="Time (s)").grid(row=len(stats)+4, column=2)
                Label(root, text="Lines of code").grid(row=len(stats)+4, column=3)
                Button(root, text="Delete", command=lambda h=row['host']: delete_user(h)).grid(row=i+5+len(stats), column=len(columns_stats) + 1)
for u in psutil.users():
    host = u.name

def token_get(password):
    global token
    print("Awaiting for authorization...")
    token = requests.post(f'{URL}auth?host={host}&role=admin&password={password}')

def load_data():
    data = requests.get(f'{URL}admin?token={token.text}&action=view_all')
    data = data.json()
    print(data)
    columns_stats = ['host', 'cpu', 'ram', 'disk', 'uptime']
    columns_prog = ['host', 'process', 'time', 'lines']
    Table(root, data, columns_stats, columns_prog)
    root.after(2000, load_data)
def delete_user(user):
    requests.get(f'{URL}admin?token={token.text}&action=delete_user&user={user}')
    for widget in root.winfo_children():
        widget.destroy()
    load_data()


root = Tk()
l = Login(root)

root.mainloop()
