@echo off
chcp 65001 > nul
title Generatore ASCII Art & Braille Ultra HD
cd /d "%~dp0"

if "%~1"=="" (
    python image.py
) else (
    python image.py "%~1"
)

pause
