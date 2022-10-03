from card import Card, Cards
from player import Player, Players
from enum import Enum
from random import randint

ANTE_MIN = 5

class Board:
    ## стадии игры: Pre-flop, Flop, Turn, River, Showdown
    class Stages(Enum):
        PRE_FLOP, FLOP, TURN, RIVER = (0, 1, 2, 3)
        def __int__(self):
            return int(self.value)
    ## стадия игры
    stage = Stages.PRE_FLOP
    ## ставка раунда
    bet = 0
    ## банк раунда
    pot = 0    
    ## карты
    cards = []
    ## игроки
    players = []
    ## инициализация    
    def __init__(self, player_names):
        self.stage = self.Stages.PRE_FLOP
        self.bet = 0
        self.pot = 0        
        self.cards = Cards()
        self.players = Players(player_names)
    def __del__(self):
        del self.cards, self.players
    ## сброс состояний доски (новая игра)
    def reset(self):
        del self.cards
        self.stage = self.Stages.PRE_FLOP
        self.bet = 0
        self.pot = 0        
        self.cards = Cards()
    ## просмотр
    def view(self):
        print('стадия {}'.format(self.stage))
        print('на столе {} фишек'.format(self.pot))
    ## интерфейс ввода действия
    def player_input(self):
        val = 0
        print('1 - принять, 2 - пропустить, 3 - поднять, 4 - сбросить, 5 - ва-банк')
        act = Player.Actions(int(input()) + 1)
        if act == Player.Actions.RAISE:
            print('сколько в сумме поставить?')
            val = int(input())
##        act = Player.Actions(randint(2,4))
##        val = randint(self.bet, 2*self.bet)
        return act, val
    ## интерфейс вывода карт игрока
    def player_cards_output(self, player):
        print('Игрок {}'.format(player.position), end=': ')
        print(' '.join(card.name for card in self.cards if card.owner == player.position))
    ## интерфейс вывода карт доски
    def board_cards_output(self):
        print('Доска #', end=': ')
        print(' '.join(card.name for card in self.cards if card.owner == 100))
    ##  раунд: раздача карт
    def round_cards(self, stage):
        self.stage = stage
        ## PRE_FLOP
        if self.stage == self.Stages.PRE_FLOP:
            ## раздача карт игрокам
            for player in self.players:
                self.cards.distribution(player.position, 2)
        ## FLOP
        if self.stage == self.Stages.FLOP:
            ## раздача карт на стол
            self.cards.distribution(100, 3)
        ## TURN
        if self.stage == self.Stages.TURN:
            ## раздача карт на стол
            self.cards.distribution(100, 1)
        ## RIVER
        if self.stage == self.Stages.RIVER:
            ## раздача карт на стол
            self.cards.distribution(100, 1)
        ## показать доску и карты
        self.board_cards_output()
        for player in self.players:
            self.player_cards_output(player)
    ##  раунд: торги
    def round_trades(self, stage):
        self.players.round_states_reset()
        self.bet = 0
        ## обязательные ставки, раунд PRE_FLOP
        if self.stage == self.Stages.PRE_FLOP:
            self.players.next_player_move().post(Player.Actions.FIRST, ANTE_MIN, ANTE_MIN)
            self.players.next_player_move().post(Player.Actions.FIRST, ANTE_MIN*2, ANTE_MIN*2)
            self.bet = ANTE_MIN*2
        ## основной цикл, раунды все ALL
        while True:
            ## игрок остался один?
            if len(self.players.vote_players()) == 1:
                return 1            
            ## ход игрока
            player = self.players.next_player_move()
            print('ставка раунда: {} фишек\n'.format(self.bet))
            print('++ теперь ход игрока №{} "{}"'.format(player.position, player.name))
            while True:
                ## ввод действия пользователя
                act, val = self.player_input()
                ## ход игрока
                result = player.post(act, self.bet, val)
                ## ошибка?
                if result[0] == Player.Actions.FAILED:
                    print('повтор операции ввода:')
                    continue
                else:
                    ## сделал ставку (не сбросил карты)
                    if result[0] != Player.Actions.FOLD:
                        player.bet = result[1]
                    ## все ОК -- выход
                    break
            ## ставка игрока превысила ставку раунда?
            if self.bet < player.bet:
                self.bet = player.bet
            ## ставки уравнены? все голосующие сделали ставки?
            if (self.players.bet_min() == self.bet and self.players.vote_finished()):
                break
        self.pot += self.players.bet_sum()
        print('++ конец раунда торгов: на кону банк в размере {} фишек'.format(self.pot))
        return 0
    ##  раунд: финал (возвращает игрока-победителя)
    def round_final(self, stage):
        ## результаты, раунд SHOWDOWN
        print('Банк {} фишек'.format(self.pot))
        ## финал вариант 1: все игроки, кроме одного сбросили карты -- безусловная победа без открытия карт
        if len(self.players.active_players()) == 1:
            ## оставшийся единственный активный игрок
            self.players.active_players()[0].won = True
        ## финал вариант 2: несколько и более игроков в финале -- подсчет комбинаций            
        else:
            print('++ Комбинации:')
            for player in self.players.active_players():
                print('Игрок №{} "{}"'.format(player.position, player.name))
                cards = Cards(list(card for card in self.cards if (card.owner == player.position or card.owner == 100)))
                player.score = cards.analize()
                print(player.score)
            score_max = max(player.score for player in self.players.active_players())
            for player in self.players.active_players():
                if player.score[0] == score_max[0]:
                    player.won = True
        ## деньги победителям
        print('++ Победитель:')
        award = self.pot/len(self.players.win_players())
        for player in self.players.win_players():
            player.balance += award
            print('Игрок №{} "{}" забирает {} фишек'.format(player.position, player.name, award))
        return self.players.win_players()
        
    
    ## разыгрывание руки (матч)
    def hand(self):
        self.reset()
        self.players.reset()
        self.cards.reset()
        for stage in Board.Stages:
            text = ['РАУНД 1/4 PRE-FLOP ПРЕ-ФЛОП', 'РАУНД 2/4 FLOP ФЛОП', 'РАУНД 3/4 TURN ТЁРН', 'РАУНД 4/4 RIVER РИВЕР']
            print('{}\n{}\n{}'.format('*'*40, text[int(stage)], '*'*40))
            self.round_cards(stage)
            if (self.round_trades(stage) > 0):
                break
        print('{}\n{}\n{}'.format('*'*40, 'ФИНАЛ', '*'*40))
        self.round_final('ФИНАЛ')
        ## итого
        print('-'*40)
        self.players.player_game_losers()
        self.players.showstate()
        if self.players.check_game_win():
            return True
        else:
            return False
       
