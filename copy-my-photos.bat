@echo off
echo Copying photos from Downloads to gallery...
echo.

set SOURCE=C:\Users\yorki\Downloads
set DEST=C:\Users\yorki\.claude\.claude\worktrees\cranky-kirch-f6a33b\gallery\images

if not exist "%DEST%" mkdir "%DEST%"

xcopy /y "%SOURCE%\*.jpg"  "%DEST%\" 2>nul
xcopy /y "%SOURCE%\*.jpeg" "%DEST%\" 2>nul
xcopy /y "%SOURCE%\*.png"  "%DEST%\" 2>nul
xcopy /y "%SOURCE%\*.heic" "%DEST%\" 2>nul
xcopy /y "%SOURCE%\*.webp" "%DEST%\" 2>nul

echo.
echo Done! Here are the photos now in your gallery images folder:
echo.
dir /b "%DEST%"
echo.
pause
