chcp 1251

set path="C:\Program Files\WinRAR";"D:\Games\Skyrim - Legendary Edition";%path%

REM WinRAR a Saves.zip "Saves"

@echo off
COLOR 06
:start
cls
echo         ��� �?
echo.
echo         1. � - ������
echo         2. � - �������
echo         3. � - ������
echo.
set /p choice=        ��� ����� [1 .. 3]: 
rem if not '%choice%'=='' set choice=%choice:~0;1%
if '%choice%'=='1' goto 1
if '%choice%'=='2' goto 2
if '%choice%'=='3' goto 3
if not '%choice%'=='' echo "%choice%" ������ ��� � ���!
echo

goto action
:1
echo         ������, ������!
echo         ������ ����� ������������ ���������� � �������� ����:
set user="Goat"
goto action

:2
echo         ������, �������!
echo         ������ ����� ������������ ����������� ������� ���������� � �������� ����:
set user="Sheep"
goto action

:3
echo         ������� �� ������ � �������!
echo         ������� ������� ���������� ��� ��� ����������
set user="Rabbit"
echo.
pause
goto start

:action
echo         �������� ��������� ����� ���������� ����...
WinRAR a "-cp��������� ����� ��������� ������" -y -ibck "Backup.zip" "Saves"
echo         ������� ���������� ����������...
rmdir "Saves" /s /q
echo         ���������� ����������...
WinRAR x -y -ibck "Saves %user%.zip"
echo         ������ ����...
set thisdir=%CD%
cd /d "D:\Games\Skyrim - Legendary Edition"
TESV.exe
cd /d %thisdir%
echo         �������� ����������...
WinRAR a -y -ibck "Saves %user%.zip" "Saves"
echo         ��� ��! ������ ��������� ����� ������� ��� ���������� ������
echo.
pause
goto start