@echo on

git pull

IF EXIST %~dp0venv (
    call %~dp0venv\Scripts\activate
) ELSE (
    py -m venv venv
    call %~dp0venv\Scripts\activate
    pip install -r requirements.txt
)

echo BOT GOTOV K RABOTE
py main.py