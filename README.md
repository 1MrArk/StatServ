# StatServ - monitor system utilisation and coding progress
StatServ is a simple coding project for my intership, that consists of three parts:
- Client - Python script that collects system utilization data and tracks student's progress by monitoring uptime of an IDE and total code lines in a folder
- Server - REST server, that authorizes client, receives information from it, and stores data in a MongoDB database
- Admin - admin panel for fetching and displaying information from the database through the server

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

I also included admin script to view information kept on the server DB. To launch it:
1. Install dependencies
2. Launch it in terminal: `python admin.py`

## Environmental variables
- MONGO_URI - by default it looks for local instance made while composing docker instance
- PASSWORD - admin password, by default: 'admin'
