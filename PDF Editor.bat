@echo off
cd /d "D:\Deepseek skipartner\PDF-Equilibrist-main"
call venv\Scripts\activate.bat
set PYTHONPATH=src
start "" pyw src\pdf_equilibrist\main.py