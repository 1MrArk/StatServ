import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Client')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Server')))
from script import collect, token_get, scrpt
def test_collect():
    for user in psutil.users():
        host = user.name
    collect()
    assert host in reports
    assert host in progresses
    assert isinstance(reports[host], Report)
    assert isinstance(progresses[host], Progress)

def test_token_get():
    token_get()
    assert token.status_code == 200

def test_scrpt():
    token_get()
    scrpt()
    assert token.status_code == 200

