@echo off
pyinstaller -F -w -i icon/main.ico main.py --add-data "./icon/main.png;./icon" -n slow-mouse
