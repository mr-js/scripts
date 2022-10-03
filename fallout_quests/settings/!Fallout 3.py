# coding=utf8

# FALLOUT 3 CONFIG BEGIN

name = 'Fallout 3'
domain = 'fallout.fandom.com'
protocol =  'https'
pages_level_max = 3
root_path = f'/ru/wiki'
root_page = '/ru/wiki/Fallout_3'
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
Fallout: New Vegas
Fallout New Vegas
Fallout 76
Fallout Extreme
Fallout Tactics 2
Van Buren
Brotherhood of Steel 2
Project V13
Fallout Online
'''
links_positives = '''
Fallout: 3
Fallout 3
'''
links_patches = [
]

meta_required = '''
Fallout 3
The Pitt
Mothership Zeta
Operation: Anchorage
Broken Steel
Point Lookout
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
Fallout: New Vegas
Fallout New Vegas
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
Fallout 3
The Pitt
Mothership Zeta
Operation: Anchorage
Broken Steel
Point Lookout
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
Fallout: New Vegas
Fallout New Vegas
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
Fallout 3
The Pitt
Mothership Zeta
Operation: Anchorage
Broken Steel
Point Lookout
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
Fallout 3
The Pitt
Mothership Zeta
Operation: Anchorage
Broken Steel
Point Lookout
( )
()
[ ]
[]
'''
main_filter = '''
Fallout 3
Fallout_3_SPECIAL
Активаторы Fallout_3
Баги Fallout_3
Боеприпасы Fallout_3
Броня и одежда Fallout_3
Голодиски Fallout_3
Дополнения Fallout_3
Заметки Fallout_3
Квесты Fallout_3
Ключи Fallout_3
Книги Fallout_3
Компьютеры и роботы Fallout_3
Контейнеры Fallout_3
Концовки Fallout_3
Локации Fallout_3
Медпрепараты и еда Fallout_3
Навыки Fallout_3
Напарники Fallout_3
Организации Fallout_3
Оружие Fallout_3
Патчи Fallout_3
Персонажи Fallout_3
Предметы Fallout_3
Пупсы Fallout_3
Радиостанции Fallout_3
Разные предметы Fallout_3
Случайные встречи Fallout_3
Способности Fallout_3
Существа Fallout_3
Терминалы Fallout_3
Титры Fallout_3
Торговцы Fallout_3
'''

# FALLOUT 3 CONFIG END
