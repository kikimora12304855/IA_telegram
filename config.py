import os

API_GITHUB = os.environ.get('API_GITHUB')

DBuser = os.environ.get("DBUSER")
DBhost = os.environ.get("DBHOST") if os.environ.get("DBHOST") != None else "127.0.0.1"
DBpass = os.environ.get("DBPASS")
DBname = os.environ.get("DBNAME")
DBport = os.environ.get("DBPORT") if os.environ.get("DBPORT") != None else "5432"
