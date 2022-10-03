import itertools
import codecs
import time
import csv


class AlchemyLab():
    def __init__(self):
        self.ingreditents = {}
        with codecs.open('data.csv', 'r', 'utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter = ';', quoting=csv.QUOTE_NONE)
##            next(reader, None)
            for row in reader:
                self.ingreditents.update({row[0]:row[1:]})
        self.all_effects = []
        for group in list(self.ingreditents.values()):
            for item in group:
                if len(item) > 3:
                    self.all_effects.append(item)                    
        self.all_effects = (list(set(self.all_effects)))
        self.all_effects.sort()

        print('Загружено ингредиентов: {}'.format(len(self.ingreditents)))
        print('Количество возможных комбинаций ингредиентов (макс): {}'.format(len(list(itertools.combinations(self.ingreditents, 4)))))


    def potion(self, potion_ingredients):
        all_effects = []
        for ingredient_name in potion_ingredients:
            for ingredient_effect in self.ingreditents[ingredient_name]:
                all_effects.append(ingredient_effect)
        double_effects = []
        for effect in all_effects:
            if all_effects.count(effect) > 1 and effect != '':
                double_effects.append(effect)
        potion_effects = set(double_effects)
        if potion_effects == set():
            return [], []
        else:
            return potion_ingredients, potion_effects


    def analize(self, target_effects):
        counter = 0
        print('Эффекты для поиска комбинации (зелья):\n')
        print('\n'.join('{}'.format(target_effect) for target_effect in target_effects))
        if len(target_effects) == 1: target_effects += target_effects
        for target_slots in range(len(target_effects), 4+1):
            result = {}
            print('-'*80)
            print('Количество слотов для комбинаций: {}'.format(target_slots))            
            ingredients_combinations = itertools.combinations(self.ingreditents, target_slots)
            ingredients_combinations_max = len(list(itertools.combinations(self.ingreditents, target_slots)))
            print('Количество комбинаций для анализа: {}'.format(ingredients_combinations_max))
            for combination in ingredients_combinations:
                counter += 1
                if not(all(set(target_effects) & set(self.ingreditents[ingredient_name]) for ingredient_name in combination)):
                    continue
                potion_ingredients, potion_effects = self.potion(combination)
                if set(target_effects) == set(potion_effects):
                    result.update({', '.join(potion_ingredients) : ''})
            print('Количество подходящих комбинаций: {}\n'.format(len(result)))
            print('\n'.join('{}\t{}'.format(k, v) for k, v in result.items()))
        print('-'*80)



    def analize_full(self):
        counter = 0
        result = {}
        target_effects = 4
        for target_slots in range(2, 4+1):
            print('-'*80)
            print('Количество слотов для комбинаций: {}'.format(target_slots))
            print('Количество эффектов комбинации (мин): {}'.format(target_effects))
            ingredients_combinations = itertools.combinations(self.ingreditents, target_slots)
            ingredients_combinations_max = len(list(itertools.combinations(self.ingreditents, target_slots)))
            print('Количество комбинаций для анализа: {}'.format(ingredients_combinations_max))
            for combination in ingredients_combinations:
                counter += 1
                potion_ingredients, potion_effects = self.potion(combination)
                if len(potion_effects) >= target_effects:
                    result.update({', '.join(potion_ingredients) : potion_effects})
        print('-'*80)
        print('Количество подходящих комбинаций: {}\n'.format(len(result)))
        with codecs.open('output.txt', 'w', 'utf-8') as output:
            for k, v in result.items():
                output.write(k + '\r\n')
                output.write(', '.join(str(effect) for effect in list(v)))
                output.write('\r\n'*2)
        print('Завершено. Данные в файле {}'.format('output.txt'))
        print('-'*80)    


alchemyLab = AlchemyLab()
##alchemyLab.potion(['Болотный тростник', 'Изумруд', 'Мясо гончей', 'Лепестки каменевки'])
##alchemyLab.analize(['Восстановить здоровье', 'Восстановить запас сил', 'Увеличить здоровье', 'Увеличить магию'])
##alchemyLab.analize(['Восстановить здоровье', 'Восстановить запас сил', 'Увеличить здоровье'])
##alchemyLab.analize(['Восстановить здоровье', 'Восстановить запас сил'])
##alchemyLab.analize(['Левитация'])

target_effect = ''
target_effects = []
for i in range(4):
    while (True):
        print('Введите название эффекта {} (Enter для пропуска, ? для вывода списка эффектов)'.format(i+1))
        target_effect = input()
        if target_effect == '':
            break
        elif target_effect == '?':
            print('\n'.join(effect for effect in alchemyLab.all_effects))
        elif target_effect in alchemyLab.all_effects:
            target_effects.append(target_effect)
            print('Эффект {} добавлен'.format(target_effect))
            break
        else:
            print('Эффекта {} не существует. Проверьте написание и повторите ввод.'.format(target_effect))

start_time = time.time()
if all(target_effect == None for target_effect in target_effects):
    print('Режим полного анализа без параметров...')
    alchemyLab.analize_full()
else:
    target_effects = list(filter(None, target_effects))
    alchemyLab.analize(target_effects)
print('~ Время выполнения: {} сек. ~'.format(int(time.time() - start_time)))
input()


