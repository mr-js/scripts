PLAYER_START_BALANCE = 100
from enum import Enum
import itertools


class Player:
    ## имя игрока
    name = ''
    ## идентификатор/позиция игрока
    position = 1
    ## баланс игрока в игре
    balance = 0
    ## игрок проголосовал в текущем раунде торгов?
    voted = False
    ## игрок сбросил карты?
    folded = False
    ## игрок пошел ва-банк?
    allin = False
    ## игрок победил
    won = False
    ## ставка игрока в текущем раунде торгов
    bet = 0
    ## очки игрока в конце раунда игры
    score = 0
    ## действия игрока
    class Actions(Enum):
        FAILED, NONE, FIRST, CALL, CHECK, RAISE, FOLD, ALLIN = (-1, 0, 1, 2, 3, 4, 5, 6)
    ## действие игрока
    action = Actions.NONE
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.folded = False
        self.allin = False
        self.voted = False
        self.won = False
        self.balance = PLAYER_START_BALANCE
        self.score = 0
    ## интерфейс вывода информации об игроке
    def showinfo(self):
        print('Игрок №{} "{}": баланс {} фишек'.format(self.position, self.name, self.balance))
    ## действин игрока (первый аргумент - мин. текущая ставка раунда, возвращает новую мин. ставку раунда)
    def post(self, action_type, *action_args):
        self.voted = True
        self.action = action_type
        bet_round_min = action_args[0]
        ## первая ставка (сумма первой ставки, минимальная сумма обязательной ставки или раунда)
        if action_type == self.Actions.FIRST:
            bet_player_first = action_args[1]
            ## сумма предлагаемой ставки не меньше минимальной допустимой суммы?
            if bet_player_first >= bet_round_min:
                self.bet = bet_player_first
                self.balance -= bet_player_first
                ## баланс при первой ставке в минус?
                if self.balance < 0:
                    self.balance = 0
                print('Игрок №{} "{}": сделал первую ставку {} фишек и у него осталось {} фишек'.format(self.position, self.name, bet_player_first, self.balance))
                return self.action, bet_player_first
        ## пропуск хода (текущая сумма ставки раунда)
        if action_type == self.Actions.CHECK:
            ## предыдущая ставка игрока равна минимальной ставке раунда?
            if self.bet == bet_round_min:
                print('Игрок №{} "{}": не сделал ставку и пропустил ход, на его счету {} фишек'.format(self.position, self.name, self.balance))
                return self.action, bet_round_min
        ## принятие ставки (текущая ставка раунда)
        if action_type == self.Actions.CALL:
            bet_delta = bet_round_min - self.bet
            ## позволяет баланс игрока принять ставку? не в минус ли принимает?
            if self.balance >= bet_delta and bet_delta >= 0:
                self.balance -= bet_delta
                self.bet += bet_delta
                print('Игрок №{} "{}": принял ставку {}, добавив {} фишек, и у него осталось {} фишек'.format(self.position, self.name, bet_round_min, bet_delta, self.balance))
                return self.action, bet_round_min
        ## поднятие ставки (новая ставка игрока (+добавить), текущая ставка раунда)
        if action_type == self.Actions.RAISE:
            bet_player_total = action_args[1]
            bet_player_delta = bet_player_total - self.bet
            ## позволяет баланс игрока поднять ставку? ставка раунду соответствует? не в минус ли поднимает?
            if self.balance >= bet_player_total and bet_player_total >= bet_round_min and bet_player_delta > 0:
                self.balance -= bet_player_delta
                self.bet = bet_player_total
                print('Игрок №{} "{}": поднял ставку до {}, добавив {} фишек, и у него осталось {} фишек'.format(self.position, self.name, bet_player_total, bet_player_delta, self.balance))
                return self.action, bet_player_total
        ## ва-банк (текущая ставка раунда)
        if action_type == self.Actions.ALLIN:
            self.bet = bet_round_min
            self.balance = 0
            print('Игрок №{} "{}": идет ва-банк, поставив все свои фишки, его баланс сейчас {}'.format(self.position, self.name, self.balance))
            self.allin = True
            return self.action, bet_round_min
        ## сброс карт (текущая ставка раунда)
        if action_type == self.Actions.FOLD:
            print('Игрок №{} "{}": сбросил карты, покинув раунд торгов'.format(self.position, self.name))
            self.folded = True
            return self.action, bet_round_min
        ## не получилось выполнить одно из действий
        print('Игрок №{} "{}": не удалось выполнить операцию {} {}'.format(self.position, self.name, self.action, action_args))
        self.action = self.Actions.FAILED
        return self.action, bet_round_min


class Players:
    players = []
    ## индекс текущего активного игрока
    active = 1    
    ## индекс игрока-дилера
    dealer = 1
    ## инициализация
    def __init__(self, names):
        self.players = []
        counter = 1
        for name in names:
            self.players.append(Player(name, counter))
            counter += 1
        self.active = 1            
        self.dealer = 0
    ## деинициализация     
    def __del__(self):
        del self.players
    ## кол-во игроков
    def __len__(self):
        return len(self.players)
    ## выборка игроков []
    def __getitem__(self, key):
        if isinstance(key, slice):
            return Players(self.players[key.start:key.stop:key.step])
        else:
            return self.players[key]
    ## интерфейс вывода информации об игроках
    def showinfo(self):        
        for player in self.players:
            print('Игрок №{} "{}"'.format(player.position, player.name))
    ## интерфейс вывода информации об игроках
    def showstate(self):     
        for player in self.players:
            print('Игрок №{} "{}": {} фишек'.format(player.position, player.name, player.balance))            
    ## активные игроки в раунде (ни скинули карты)
    def active_players(self):
         return list(player for player in self.players if not player.folded)
    ## минимальная ставка по всем активным игрокам
    def bet_min(self):
        return min(player.bet for player in self.active_players())
    ## суммарная ставка по всем активным игрокам
    def bet_sum(self):
        return sum(player.bet for player in self.active_players())
    ## голосующие игроки в раунде (ни скинули карты, ни пошли ва-банк)
    def vote_players(self):
        return list(player for player in self.players if (not player.folded and not player.allin))
    ## все голосующие игроки проголосовали в раунде
    def vote_finished(self):
        return all(player.voted for player in self.vote_players())
    ## выигравшие игроки в раунде (кол-во очков за комбинации)
    def win_players(self):
         return list(player for player in self.players if player.won)    
    ## следующий игрок
    def next_player_move(self):
        ## игрок остался один?
        if len(self.active_players()) == 1:
            return None
        ## следующий игрок по кругу (сложная функция)
        takenext = False
        player = None
        for player in itertools.cycle(self.players):
            if (takenext and (not player.folded and not player.allin)):
                self.active = player.position
                break         
            if (not takenext and (player.position == self.active)):
                takenext = True
                continue         
        return player   
    ## сброс состояний игроков (новый раунд)
    def round_states_reset(self):
        for player in self.players:
            player.voted = False
            player.bet = 0           
        self.active = self.dealer
    ## сброс состояний игроков (новая игра)
    def reset(self):
        for player in self.players:
            player.folded = False
            player.allin = False
            player.voted = False
            player.won = False           
            player.bet = 0
            player.score = 0
        self.dealer += 1
        if self.dealer > len(self.players):
            self.dealer = 1
        self.active = self.dealer
    ## игрок выбывает из всей игры
    def player_game_losers(self):
        for player in self.players:
            if player.balance == 0:
                print('Игрок №{} "{}" выбывает из игры'.format(player.position, player.name))
                self.players.remove(player)
    ## окончательная победа во всей игре
    def check_game_win(self):
        if  len(self.players) == 1:
            player = self.players[0]
            print('Игрок №{} "{}" выиграл эту игру'.format(player.position, player.name))
            return True
        else:
            return False
            
