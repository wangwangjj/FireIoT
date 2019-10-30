#!/bin/bash
nohup python3 -u ./user/serverV12.py > server.log 2>&1 &
nohup python3 -u manage.py runserver 0.0.0.0:8000 > web.log 2>&1 &
