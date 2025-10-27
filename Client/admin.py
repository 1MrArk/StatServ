from tkinter import Label, Entry, Button, Tk
import psutil
import requests

URL = 'http://127.0.0.1:5000/'

class Login:
    """Creates login page"""
    def __init__(self, rt):
        """Initializes login page"""
        self.root = rt
        self.root.title("Login")
        Label(self.root, text="URL").grid(row=0, column=0)
        self.url_entry = Entry(self.root, width=20)
        self.url_entry.grid(row=0, column=1)
        Label(rt, text="Password:").grid(row=1, column=0)
        self.password_entry = Entry(rt, show="*")
        self.password_entry.grid(row=1, column=1)
        Button(rt, text="Login", command=self.login).grid(row=2, column=1)

    def login(self):
        """Requests token based on given URL and password"""
        password = self.password_entry.get()
        token_get(password)
        if token.status_code == 200:
            for widget in self.root.winfo_children():
                widget.destroy()
            load_data()

class Table:
    """Creates table page"""
    def __init__(self, rt, data, columns_stats, columns_prog):
        """Initializes table page"""
        stats = data['stats']
        prog = data['prog']
        for i, row in enumerate(stats):
            for j, key in enumerate(columns_stats):
                s = Label(rt, text=row[key], width=10)
                s.grid(row=i+2, column=j)
                Label(rt, text="System utilisation table:").grid(row=0, column=2)
                Label(rt, text="Hostname").grid(row=1, column=0)
                Label(rt, text="CPU (%)").grid(row=1, column=1)
                Label(rt, text="RAM (%)").grid(row=1, column=2)
                Label(rt, text="Disk usage (%)").grid(row=1, column=3)
                Label(rt, text="Uptime (sec)").grid(row=1, column=4)
                (Button(rt, text="Delete", command=lambda h=row['host']: delete_user(h))
                 .grid(row=i+2, column=len(columns_stats) + 1))
        for i, row in enumerate(prog):
            for j, key in enumerate(columns_prog):
                p = Label(rt, text=row[key], width=10)
                p.grid(row=i+5+len(stats), column=j)
                Label(rt, text="Progress table:").grid(row=len(stats) + 3, column=2)
                Label(rt, text="Hostname").grid(row=len(stats) + 4, column=0)
                Label(rt, text="IDE").grid(row=len(stats) + 4, column=1)
                Label(rt, text="Time (s)").grid(row=len(stats) + 4, column=2)
                Label(rt, text="Lines of code").grid(row=len(stats) + 4, column=3)
                (Button(rt, text="Delete", command=lambda h=row['host']: delete_user(h))
                 .grid(row=i+5+len(stats), column=len(columns_stats) + 1))
for u in psutil.users():
    host = u.name

def token_get(password):
    """Requests token based on given URL and password"""
    global token
    print("Awaiting for authorization...")
    token = requests.post(f'{URL}auth?host={host}&role=admin&password={password}')

def load_data():
    """Loads data from database"""
    data = requests.get(f'{URL}admin?token={token.text}&action=view_all')
    data = data.json()
    print(data)
    columns_stats = ['host', 'cpu', 'ram', 'disk', 'uptime']
    columns_prog = ['host', 'process', 'time', 'lines']
    Table(root, data, columns_stats, columns_prog)
    root.after(2000, load_data)
def delete_user(user):
    """Deletes user from database"""
    requests.get(f'{URL}admin?token={token.text}&action=delete_user&user={user}')
    for widget in root.winfo_children():
        widget.destroy()
    load_data()


root = Tk()
l = Login(root)

root.mainloop()
