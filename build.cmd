@echo off
pyinstaller -F -w -i icon/main.ico slow-mouse.py --add-data "./icon/main.png;./icon"
