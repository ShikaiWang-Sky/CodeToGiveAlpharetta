#!/usr/bin/env python3
from flaskblog import app
import subprocess

if __name__ == '__main__':
    subprocess.run(["python3 flaskblog/create_db.py"], shell=True)
    app.run(debug=True)
