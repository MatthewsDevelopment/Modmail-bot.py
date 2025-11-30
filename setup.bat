@echo off
title Modmail-Bot.py Setup Script

:menu
cls
echo Modmail-Bot.py
echo Provided by: Matthew's Development.
echo 1) Install Python packages
echo 2) List installed Python packages
echo 3) Source Codes
echo 4) Exit
set /p menu=
if %menu%==1 goto install
if %menu%==2 goto start
if %menu%==3 goto source
if %menu%==4 goto exit
goto menu

:install
cls
echo Installing the following Python packages:
echo discord.py, discord, python-dotenv
py -m pip install discord.py
py -m pip install discord
py -m pip install python-dotenv
pause
goto menu

:start
cls
py -m python ./main.py
pause
goto menu

:source
echo 1) Back
echo 2) Codeberg Source Code
echo 3) Gitlab Source Code
echo 4) Github Source Code
set /p menu=
if %menu%==1 goto menu
if %menu%==2 start https://codeberg.org/MatthewsDevelopment/Modmail.py
if %menu%==3 start https://gitlab.com/MatthewsDevelopment/modmailpy
if %menu%==4 start https://github.com/MatthewsDevelopment/Modmail-bot.py