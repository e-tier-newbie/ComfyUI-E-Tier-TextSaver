@echo off

set "requirements_txt=%~dp0\requirements.txt"
set "python_exec=..\..\..\python_embeded\python.exe"

echo Installing E_TierTextSaver dependencies...

if exist "%python_exec%" (
    echo Found ComfyUI Portable Python at %python_exec%
    "%python_exec%" -s -m pip install -r "%requirements_txt%"
) else (
    echo ComfyUI Portable Python not found, using system Python
    pip install -r "%requirements_txt%"
)

pause
