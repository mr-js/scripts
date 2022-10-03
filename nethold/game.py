import os
from board import Board

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

players_number = 0
players = []
while players_number < 2 or players_number > 8:
    players_number = int(input('Количество игроков [2 .. 8]: '))
for i in range(players_number):
    players.append(input('Имя игрока: '))

##players = ['1', '2']
board = Board(players)
board.players.showinfo()

while True:
    print('{}\n{}\n{}'.format('='*40, 'НОВАЯ ИГРА', '='*40))
    board.players.showstate()
    if board.hand():
        break
    input('Нажмите любую клавишу для продолжения игры...')
    cls()

input('Нажмите любую клавишу для завершения игры')

