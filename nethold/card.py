from itertools import permutations, combinations, combinations_with_replacement
from random import randint, shuffle

class Card:
    ## ранг карты
    rank = ''
    ## масть карты
    color = ''
    ## полное имя карты (ранг + масть)
    name = ''
    ## определение полных имен карты (ранг + масть)
    NAMES = (\
    '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', 'В♣', 'Д♣', 'К♣', 'Т♣', \
    '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦', '10♦', 'В♦', 'Д♦', 'К♦', 'Т♦', \
    '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', 'В♥', 'Д♥', 'К♥', 'Т♥', \
    '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', '10♠', 'В♠', 'Д♠', 'К♠', 'Т♠')
    ## определение рангов карты
    RANKS = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9' : 9, \
             '10': 10, 'В' : 11, 'Д' : 12, 'К' : 13, 'Т': 14}
    ## определение мастей карты
    COLORS = {'♣' : 1, '♦' : 2, '♥': 3, '♠' : 4}
    ## текущий владелец карты: игрок 0 .. X, колода 1000, доска 100, вышла из игры -1
    owner = 1000
    ## инициализация
    def __init__(self, name=None):
        if name == None:
            name = self.NAMES[randint(0,51)]
        if name not in self.NAMES:
            raise ValueError('карты {} не существует в колоде'.format(name))
        self.name = name
        self.rank = self.name[:-1:]
        self.color = self.name[-1::]
        self.owner = 1000
    ## !=  карты идентичны по масти
    def __ne__(self, other):
        return True if self.COLORS[self.color] == self.COLORS[other.color] else False
    ## == карты равнозначны по рангу
    def __eq__(self, other):
        return True if self.RANKS[self.rank] == self.RANKS[other.rank] else False
    ## >  карта больше по рангу другой
    def __gt__(self, other):
        return True if self.RANKS[self.rank] > self.RANKS[other.rank] else False
    ## <  карта меньше по рангу другой
    def __lt__(self, other):
        return True if self.RANKS[self.rank] < self.RANKS[other.rank] else False
    ## <=  карта рядом До другой
    def __le__(self, other):
        return True if self.RANKS[self.rank] == self.RANKS[other.rank] - 1 or self.RANKS[self.rank] == 14 and self.RANKS[other.rank] == 2 else False
    ## >=  рядом рядом После другой
    def __ge__(self, other):
        return True if self.RANKS[self.rank] == self.RANKS[other.rank] + 1 or self.RANKS[self.rank] == 2 and self.RANKS[other.rank] == 14 else False
    ## +   собрать карты в [массив карт]
    def __add__(self, other):
        return [self, other]
    ## интерфейс просмотра карты
    def showinfo(self):
        print('карта {}: ранг {}, масть {}'.format(\
            self.name, self.rank, self.color))
    ## смена владельца карты
    def owning(self, owner = None):
        if owner != None and self.owner != owner:
            self.owner = owner
        text = 'карта {} '.format(self.name)
        if self.owner > 0:
            if self.owner == 0:
                text += 'на столе'
            else:
                text += 'у игрока №: {}'.format(owner)
        else:
            text += 'в колоде или вышла из игры'
        print(text)
            

class Cards:
    ## карты
    cards = []
    ## указатель на активную карту
    point = 0    
    ## инициализация (имя карты)
    def __init__(self, cards=None):
        self.cards = []
        if cards != None:
            for card in cards:
                self.cards.append(card)
        else:
            for name in Card.NAMES:
                self.cards.append(Card(name))
                shuffle(self.cards)
        self.point = 0
    ## деинициализация
    def __del(self):
        del self.cards
    ## выборка карт []
    def __getitem__(self, key):
        if isinstance(key, slice):
##            print('[{}:{}:{}]'.format(key.start, key.stop, key.step))
            return Cards(self.cards[key.start:key.stop:key.step])
        else:
            return self.cards[key]
    ## смена владельца карты (через []=)
    def __setitem__(self, key, value):
        self.cards[key].owner = value
    ## раздача карт
    def distribution(self, target, amount):
        for card_index in range(self.point, self.point+amount):
             self.cards[card_index].owner = target
             self.point += 1
    ## интерфейс просмотра карт
    def showinfo(self):
        print('{}'.format(' '.join(list(card.name for card in self.cards))))
    ## анализ набора карт
    def analize(self):
        combs = set()
        result = set()
        for combs in permutations(self.cards):
            ## Роял-флэш (англ. royal flush — «королевская масть»): 5 старших (туз, король, дама, валет, десять) карт одной масти
            if ((combs[0] <= combs[1] <= combs[2] <= combs[3] <= combs[4]) and (combs[0] != combs[1] != combs[2] != combs[3] != combs[4]) and (Card.RANKS[combs[0].rank] == 10 and Card.RANKS[combs[4].rank] == 14)):
                result.add('9. РОЯЛ ФЛЭШ: {}->{}->{}->{}->{}'.format(combs[0].name, combs[1].name, combs[2].name, combs[3].name, combs[4].name))
            ## Стрит-флэш (англ. straight flush — «масть по порядку»): любые пять карт одной масти по порядку
            if (combs[0] <= combs[1] <= combs[2] <= combs[3] <= combs[4]) and (combs[0] != combs[1] != combs[2] != combs[3] != combs[4]):
                result.add('8. СТРИТ ФЛЭШ: {}->{}->{}->{}->{}'.format(combs[0].name, combs[1].name, combs[2].name, combs[3].name, combs[4].name))
            ## Каре (англ. four of a kind — «четыре одинаковых»): четыре карты одного достоинства
            if (combs[0] == combs[1] == combs[2] == combs[3]):
                result.add('7. КАРЕ: {} {} {} {}'.format(combs[0].name, combs[1].name, combs[2].name, combs[3].name))
            ## Фулл-хаус (англ. full house — «полный дом»): одна тройка и одна пара
            if (combs[0] == combs[1] == combs[2] and combs[3] == combs[4]):
                result.add('6. ФУЛЛ ХАУС: {} {} {} и {} {}'.format(combs[0].name, combs[1].name, combs[2].name, combs[3].name, combs[4].name))
            ## Флэш (англ. flush — «масть»): пять карт одной масти
            if (combs[0] != combs[1] != combs[2] != combs[3] != combs[4]):
                result.add('5. ФЛЭШ: {} {} {} {} {}'.format(combs[0].name, combs[1].name, combs[2].name, combs[3].name, combs[4].name))
            ## Стрит (англ. straight — «порядок»): пять карт по порядку любых мастей
            if (combs[0] <= combs[1] <= combs[2] <= combs[3] <= combs[4]):
                result.add('4. СТРИТ: {}->{}->{}->{}->{}'.format(combs[0].name, combs[1].name, combs[2].name, combs[3].name, combs[4].name))
            ## Сет (англ. three of a kind — «три одинаковых»): три карты одного достоинства
            if (combs[0] == combs[1] == combs[2]):
                result.add('3. СЕТ: ({} {} {}) {} {}'.format(combs[0].name, combs[1].name, combs[2].name, combs[3].name, combs[4].name))
            ## Две пары (англ. two pairs): две пары карт
            if (combs[0] == combs[1] and combs[2] == combs[3]):
                result.add('2. ДВЕ ПАРЫ: ({} {} и {} {}) {}'.format(combs[0].name, combs[1].name, combs[2].name, combs[3].name, combs[4].name))
            ## Одна пара (англ. one pair): две карты одного достоинства
            if (combs[0] == combs[1]):
                result.add('1. ОДНА ПАРА: ({} {}) {} {} {}'.format(combs[0].name, combs[1].name, combs[2].name, combs[3].name, combs[4].name))
        ## Старшая карта
        if not result:
            result.add('0. Нет комбинаций (старшая карта)')
        ## результат
        return max(result)
    ## сброс состояний карт (новая игра)
    def reset(self):
        for card in self.cards:
            self.owner = 1000
        shuffle(self.cards)
        self.point = 0
