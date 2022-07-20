@echo on

git pull

IF EXIST %~dp0venv (
    call %~dp0venv\Scripts\activate
) ELSE (
    py -m venv venv
    call %~dp0venv\Scripts\activate
    pip install -r requirements.txt
)

py main.py

:echoColor %start_green% Бот готов к работе, при завершении закройте командную строку