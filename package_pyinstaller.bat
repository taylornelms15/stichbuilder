@echo off
setlocal

:: Check if PyInstaller is installed
where pyinstaller >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] PyInstaller was not found on your system.
    echo.
    echo To install it, please run the following command:
    echo pip install pyinstaller
    echo.
    pause
    exit /b 1
)

:: If it exists, run your build command
echo Building StitchBuilder...
pyinstaller --name="StitchBuilder" --onefile --windowed .\StitchBuilderGraphical\stitchbuildergraphical.py
:: pyinstaller --name="StitchBuilder" --onefile --windowed .\StitchBuilderGraphical\stitchbuildergraphical.py

if %ERRORLEVEL% eq 0 (
    echo.
    echo Build successful! Check the "dist" folder.
) else (
    echo.
    echo [ERROR] The build failed. Check the output above for details.
)

pause
