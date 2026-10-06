@echo off
chcp 65001 > nul
title APEX Detailing Demo Bot
echo ============================================================
echo   🏎  Запуск APEX Detailing Showroom (Демо-бот PXLBOT)
echo ============================================================
echo.
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Ошибка запуска. Проверьте .env файл.
    pause
)
