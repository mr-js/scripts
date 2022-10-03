# coding=utf8

# FALLOUT NV CONFIG BEGIN

name = 'Fallout NV'
domain = 'fallout.fandom.com'
protocol =  'https'
pages_level_max = 3
root_path = f'/ru/wiki'
root_page = '/ru/wiki/Fallout:_New_Vegas'
root_page_links_block = './/table[@class="va-navbox-brick va-navbox-columncont va-navbox-formatlist va-navbox-nowraplinks"]'

page_block = './/main[@class="page__main" and @lang="ru"]'
meta_block = './/div[@class="page-header__meta"]'
title_block = './/h1[@class="page-header__title"]'
content_block = './/div[@class="mw-parser-output"]'
summary_block = './/*[@class="intro-bullets"]'
cut_blocks = '''
.//table[@class="va-navbox-border va-navbox-right"]
.//table[@class="va-navbox-border va-navbox-bottom"]
.//table[@class="mbox dabhide"]
.//table[@class="intro"]
'''

links_required = '''
/ru/wiki
'''
links_removed = '''
?
#
=edit
?diff
?oldid
?action
Шаблон:
Служебная:
Обсуждение:
Обсуждение_шаблона:
Стена обсуждения:
Fallout_Wiki:
Портал:
Участник:
Категория:
static.wikia.nocookie.net
ERROR:root
Файл
'''
links_negatives = '''
Fallout Tactics
Brotherhood of Steel
Fallout Shelter
Fallout 2
Fallout 3
Fallout 76
Fallout Extreme
Fallout Tactics 2
Van Buren
Brotherhood of Steel 2
Project V13
Fallout Online
'''
links_positives = '''
Fallout: New Vegas
Fallout New Vegas
'''
links_patches = [
]

meta_required = '''
Fallout: New Vegas
Fallout New Vegas
Caravan Pack
Classic Pack
Courier’s Stash
Gun Runners’ Arsenal
Honest Hearts
Dead Money
Lonesome Road
Old World Blues
'''
meta_removed = '''
'''
meta_negatives = '''
'''
meta_positives = '''
'''
meta_patches = [
]

title_required = '''
'''
title_removed = '''
'''
title_negatives = '''
Fallout Tactics
Brotherhood of Steel
Fallout Shelter
Fallout 2
Fallout 3
Fallout 76
Fallout Extreme
Fallout Tactics 2
Van Buren
Brotherhood of Steel 2
Project V13
Fallout Online
G.E.C.K.
'''
title_positives = '''
Fallout: New Vegas
Fallout New Vegas
Caravan Pack
Classic Pack
Courier’s Stash
Gun Runners’ Arsenal
Honest Hearts
Dead Money
Lonesome Road
Old World Blues
'''
title_patches = [
]

summary_required = '''
'''
summary_removed = '''
'''
summary_negatives = '''
Fallout Tactics
Brotherhood of Steel
Fallout Shelter
Fallout 2
Fallout 3
Fallout 76
Fallout Extreme
Fallout Tactics 2
Van Buren
Brotherhood of Steel 2
Project V13
Fallout Online
Lore
G.E.C.K.
'''
summary_positives = '''
Fallout: New Vegas
Fallout New Vegas
Caravan Pack
Classic Pack
Courier’s Stash
Gun Runners’ Arsenal
Honest Hearts
Dead Money
Lonesome Road
Old World Blues
нескольких играх серии
игр серии
'''
summary_patches = [
]

content_required = '''
'''
content_removed = '''
'''
content_negatives = '''
'''
content_positives = '''
'''
content_patches = [
]

print_filters = '''
_
Fallout: New Vegas
Fallout New Vegas
Caravan Pack
Classic Pack
Courier’s Stash
Gun Runners’ Arsenal
Honest Hearts
Dead Money
Lonesome Road
Old World Blues
( )
()
[ ]
[]
'''
main_filter = '''
Fallout_New_Vegas
Fallout_New_Vegas SPECIAL
Активаторы Fallout_New_Vegas
Баги Fallout_New_Vegas
Боеприпасы Fallout_New_Vegas
Броня и одежда Fallout_New_Vegas
Голодиски Fallout_New_Vegas
Дополнения Fallout_New_Vegas
Достижения и трофеи Fallout_New_Vegas
Журналы Fallout_New_Vegas
Заметки Fallout_New_Vegas
Имплантаты Fallout_New_Vegas
Испытания Fallout_New_Vegas
Карты для игры в Караван
Квесты Fallout_New_Vegas
Ключи Fallout_New_Vegas
Книги Fallout_New_Vegas
Компьютеры и роботы Fallout_New_Vegas
Контейнеры Fallout_New_Vegas
Концовки Fallout_New_Vegas
Ловушки Fallout_New_Vegas
Локации Fallout_New_Vegas
Медпрепараты и еда Fallout_New_Vegas
Модификация оружия Fallout_New_Vegas
Напарники Fallout_New_Vegas
Организации Fallout_New_Vegas
Оружие Fallout_New_Vegas
Особенности Fallout_New_Vegas
Патчи Fallout_New_Vegas
Персонажи Fallout_New_Vegas
Предметы Fallout_New_Vegas
Радиостанции Fallout_New_Vegas
Разные предметы Fallout_New_Vegas
Рецепты Fallout_New_Vegas
Снежные шары
Способности Fallout_New_Vegas
Спутниковый круг
Существа Fallout_New_Vegas
Терминалы Fallout_New_Vegas
Титры Fallout_New_Vegas
Торговцы Fallout_New_Vegas
'''

# FALLOUT NV CONFIG END
