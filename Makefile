.PHONY: build

build:
	pyinstaller -F -n img2zpl main.py
