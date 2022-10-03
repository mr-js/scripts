# coding=utf8

# MORROWIND CONFIG BEGIN

name = 'Morrowind'
domain = 'elderscrolls.fandom.com'
protocol =  'https'
pages_level_max = 5
root_path = f'/ru/wiki'
root_page = 'Portal/The_Elder_Scrolls_III:_Morrowind'
root_page_links_block = './/div[@id="portal_content"]'

page_block = './/main[@class="page__main" and @lang="ru"]'
meta_block = './/div[@class="page-header__meta"]'
title_block = './/h1[@class="page-header__title"]'
content_block = './/div[@class="mw-parser-output"]'
summary_block = './/*[@class="linkPreviewText"]'
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
The Elder Scrolls Wiki:
Портал:
Участник:
Категория:
static.wikia.nocookie.net
ERROR:root
Файл
'''
links_negatives = '''
Arena
Daggerfall
Oblivion
The Elder Scrolls IV
Skyrim
The Elder Scrolls V
Online
The Elder Scrolls Online
Adventures
Eye of Argonia
Paradise Sugar
Redguard
Blades
Travels
Dawnstar
Shadowkey
Stormhold
Battlespire
Legends
Адский город
'''
links_positives = '''
The Elder Scrolls III
'''
links_patches = [
]

meta_required = '''
Morrowind
Tribunal
Bloodmoon
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
Arena
Daggerfall
Oblivion
The Elder Scrolls IV
Skyrim
The Elder Scrolls V
Online
The Elder Scrolls Online
Adventures
Eye of Argonia
Paradise Sugar
Redguard
Blades
Travels
Dawnstar
Shadowkey
Stormhold
Battlespire
Legends
Адский город
Construction Set
'''
title_positives = '''
Tribunal
Bloodmoon
'''
title_patches = [
]

summary_required = '''
'''
summary_removed = '''
'''
summary_negatives = '''
Arena
Daggerfall
Oblivion
The Elder Scrolls IV
Skyrim
The Elder Scrolls V
Online
The Elder Scrolls Online
Adventures
Eye of Argonia
Paradise Sugar
Redguard
Blades
Travels
Dawnstar
Shadowkey
Stormhold
Battlespire
Legends
Адский город
Lore
Construction Set
'''
summary_positives = '''
Морровинд
The Elder Scrolls III
The Elder Scrolls III: Morrowind
The Elder Scrolls III: Tribunal
The Elder Scrolls III: Bloodmoon
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
(Morrowind)
(Tribunal)
(Bloodmoon)
( )
()
[ ]
[]
'''
main_filter = '''
The Elder Scrolls III Tribunal
The Elder Scrolls III Morrowind
The Elder Scrolls III Bloodmoon
Локации (Morrowind)
Существа (Morrowind)
Атрибуты (Morrowind)
Навыки (Morrowind)
Специализация (Morrowind)
Знаки рождения (Morrowind)
Классы (Morrowind)
Доспехи (Morrowind)
Оружие (Morrowind)
Заклинания (Morrowind)
Магические эффекты (Morrowind)
Алхимия (Morrowind)
Артефакты (Morrowind)
Главный квест (Morrowind)
Квесты Гильдии бойцов (Morrowind)
Квесты Гильдии воров (Morrowind)
Квесты Гильдии магов (Morrowind)
Квесты Имперского культа (Morrowind)
Квесты Имперского легиона (Morrowind)
Квесты Храма Трибунала (Morrowind)
Мораг Тонг (Morrowind)
Великие дома Морровинда
Пасхальные яйца (Morrowind)
Консольные команды (Morrowind)
'''

# MORROWIND CONFIG END
