# coding=utf8

# DISCIPLES II CONFIG BEGIN

name = 'Disciples II'
domain = 'disciples.fandom.com'
protocol =  'https'
pages_level_max = 3
root_path = f'/ru/wiki'
root_page = 'Категория:Disciples_II'
root_page_links_block = './/div[@id="content"]'

page_block = './/main[@class="page__main" and @lang="ru"]'
meta_block = './/div[@class="page-header__meta"]'
title_block = './/h1[@class="page-header__title"]'
content_block = './/div[@class="mw-parser-output"]'
summary_block = './/*[@class="linkPreviewText"]'

cut_blocks = '''
//table[@style="height:30px; background:#dddddd;"]
//table[@class="wikitable"]
'''


links_required = '''
/ru/wiki
'''
links_removed = '''
?
=edit
?diff
?oldid
?action
Шаблон:
Служебная:
Обсуждение:
Обсуждение_шаблона:
Стена обсуждения:
The Elder Scrolls Wiki:
Портал:
Участник:
Категория:
static.wikia.nocookie.net
ERROR:root
Файл
'''
links_negatives = '''
Disciples III
Disciples II: Blades of War
Sacred Lands
Disciples: Liberation
'''
links_positives = '''
'''
links_patches = [
lambda links: map(lambda link: f'{link}#Disciples_II_' if (any(term in link for term in ['Ашган', 'Ашкаэль', 'Видар', 'Иллюмиэлль', 'Мизраэль'])) else link, links),
lambda links: map(lambda link: f'{link}#Демон_' if (any(term in link for term in ['Утер'])) else link, links)
]

meta_required = '''
'''
meta_removed = '''
'''
meta_negatives = '''
Disciples III
Disciples II: Blades of War
Sacred Lands
Disciples: Liberation
'''
meta_positives = '''
других
'''
meta_patches = [
]

title_required = '''
'''
title_removed = '''
'''
title_negatives = '''
Disciples III
Disciples II: Blades of War
Sacred Lands
Disciples: Liberation
'''
title_positives = '''
'''
title_patches = [
]

summary_required = '''
'''
summary_removed = '''
'''
summary_negatives = '''
'''
summary_positives = '''
Disciples II
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
(Disciples II)
( )
()
[ ]
[]
'''
main_filter = '''
Disciples II Dark Prophecy
Disciples II Gallean’s Return
Disciples II Rise of the Elves
Империя
Горные Кланы
Орды Нежити
Легионы Проклятых
Альянс Эльфов
Список героев Disciples II
Список боевых единиц Disciples II
Список предметов Disciples II
Список консольных команд Disciples II
'''

# DISCIPLES II CONFIG END
