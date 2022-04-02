#!/usr/bin/env python3
from flaskblog import app
import subprocess

if __name__ == '__main__':
    subprocess.run(["./flaskblog/create_db.py"])
    app.run(debug=True)
