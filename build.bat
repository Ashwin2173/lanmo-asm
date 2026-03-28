@echo off
setlocal

net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] This script must be run as ADMINISTRATOR.
    pause
    exit /b
)

pyinstaller --onefile main.py

if %ERRORLEVEL% EQU 0 (
    echo "[INFO] BUILD SUCCESSFULLY"
    
    if exist "dist\main.exe" (
        ren "dist\main.exe" "lasm.exe"
        
        if %ERRORLEVEL% EQU 0 (
            xcopy "dist\lasm.exe" "C:\Program Files (x86)\Lasm\bin\" /I /Y
            
            if %ERRORLEVEL% EQU 0 (
                echo "[INFO] COPIED FILE SUCCESSFULLY"
            ) else (
                echo "[ERROR] COPY FAILED"
            )
        ) else (
            echo "[ERROR] RENAMING FAILED"
        )
    ) else (
        echo "[ERROR] main.exe NOT FOUND IN DIST"
    )
) else (
    echo "[ERROR] PYINSTALLER FAILED"
)

pause