@echo off

set INPUT_FILE_PATH=%1
set OUTPUT_FILE_NAME=%2

set CURRENT_DIR=%CD%
set OUTPUT_FILE_PATH=%CURRENT_DIR%\%OUTPUT_FILE_NAME%

for /f "usebackq" %%a in (`where bam2egg.exe`) do set EXE=%%a

echo %EXE%
echo %OUTPUT_FILE_PATH%
echo %INPUT_FILE_PATH%

call %EXE% %INPUT_FILE_PATH% %OUTPUT_FILE_PATH%


@REM convert.bat "...\torus.bam [full path]" torus.egg [with extension]
@REM call "...\bam2egg.exe" "...\torus.bam" "...\torus.egg"