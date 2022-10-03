chcp 1251

set path="C:\Program Files\WinRAR";"D:\Games\Skyrim - Legendary Edition";%path%

REM WinRAR a Saves.zip "Saves"

@echo off
COLOR 06
:start
cls
echo         Кто я?
echo.
echo         1. Я - Козлик
echo         2. Я - Барашек
echo         3. Я - Кролик
echo.
set /p choice=        Ваш выбор [1 .. 3]: 
rem if not '%choice%'=='' set choice=%choice:~0;1%
if '%choice%'=='1' goto 1
if '%choice%'=='2' goto 2
if '%choice%'=='3' goto 3
if not '%choice%'=='' echo "%choice%" Такого нет у нас!
echo

goto action
:1
echo         Привет, Козлик!
echo         Сейчас будут подготовлены сохранения и запущена игра:
set user="Goat"
goto action

:2
echo         Привет, Барашек!
echo         Сейчас будут подготовлены специальные барашьи сохранения и запущена игра:
set user="Sheep"
goto action

:3
echo         Кролики не играют в Скайрим!
echo         Поэтому игровые сохранения для них недоступны
set user="Rabbit"
echo.
pause
goto start

:action
echo         Создание резервной копии предыдущей игры...
WinRAR a "-cpРезервная копия выбранных файлов" -y -ibck "Backup.zip" "Saves"
echo         Очистка предыдущих сохранений...
rmdir "Saves" /s /q
echo         Извлечение сохранений...
WinRAR x -y -ibck "Saves %user%.zip"
echo         Запуск игры...
set thisdir=%CD%
cd /d "D:\Games\Skyrim - Legendary Edition"
TESV.exe
cd /d %thisdir%
echo         Упаковка сохранений...
WinRAR a -y -ibck "Saves %user%.zip" "Saves"
echo         Все ОК! Теперь программу можно закрыть или продолжить играть
echo.
pause
goto start