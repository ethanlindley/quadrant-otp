@echo off
title Quadrant-OTP

cd ../

:main
ppython -m server.base.ServerStart
pause
goto main
