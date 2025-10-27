# StatServ - monitor system utilisation and coding progress
StatServ is a (not so) simple coding project for my intership, so considering that I'm far from a good programmer, I advise you to **NOT** use this as practical solution for monitoring system utils, although feel free to look at this monstrosity of a code :)

## Installation
To install StatServ you'll need:
- Docker
- Python
- Open port 5000
1. Download zip from this repo
2. Unpack zip file and open 'Server' directory in terminal
3. Run following command:
`sudo docker build -t statserv . && sudo docker compose up -d`
<br>

Server is up and running! As for the client:
1. Open 'Client' directory
2. Move script.py to a folder that contains .py scripts and open that directory in terminal
3. Install required dependencies: `pip install -r requirements.txt`
3. Launch it in terminal: `python script.py`

## Environmental variables
- MONGO_URI - by default it looks for local instance made while composing docker instance
- PASSWORD - admin password, by default: 'admin'