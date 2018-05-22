@echo off
title Quadrant-OTP

cd ../

:main
python -m server.base.ServerStart
pause
goto main
