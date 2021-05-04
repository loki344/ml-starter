#!/bin/bash
cd ./backend/app
uvicorn main:app --host 0.0.0.0 --port 8800
