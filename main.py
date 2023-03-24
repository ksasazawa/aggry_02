import os
import subprocess
import time


cmd = "pip install -r requirements.txt"
subprocess.run(cmd.split(' '))

cmd = "python aggry/manage.py collectstatic --noinput"
subprocess.run(cmd.split(' '))

cmd = "python aggry/manage.py makemigrations"
subprocess.run(cmd.split(' '))

cmd = "python aggry/manage.py migrate"
subprocess.run(cmd.split(' '))

cmd = "python aggry/manage.py runserver 0.0.0.0:3000"
subprocess.run(cmd.split(' '))