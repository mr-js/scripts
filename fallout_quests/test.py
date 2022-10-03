import lxml.html
content = lxml.html.fromstring(r'<div><h1>HEADER</h1><div><div><p>TEXT</p><span id="INSIDER_HEADER_ID"><h3>INSIDER HEADER</h3></span></div></div><div><a href="http://....">HREF<a/></div></div>')
expaned_tags = ['div', 'section', 'span']
# # check_inline_blocks = lambda item: any(filter(lambda subitem: subitem.tag in expaned_tags, item.getchildren()))
# # while(check_inline_blocks(content)):
# for item in content.getiterator():
#     tag = item.tag
#     if tag in expaned_tags:
#         item.getparent().remove(item)
#         # item.getparent().replace(item, item)
#         # index = content.index(item)
#         # for subitem in item:
#         #     print(subitem.tag)
#         #     content.insert(index+index_add, subitem)
#         # item.getparent().remove(item)

# def expand(content):
#     expaned_tags = ['div', 'section', 'span']
#     check_inline_blocks = lambda item: len(set(filter(lambda subitem: subitem.tag in expaned_tags, item.getiterator())))
#     while(check_inline_blocks(content) > 1):
#         print(check_inline_blocks(content))
#         for item in content.getiterator():
#             tag = item.tag
#             if tag in expaned_tags:
#                 if item.getparent():
#                     index = item.getparent().index(item)
#                     index_delta = 0
#                     for subitem in item:
#                         content.insert(index+index_delta, subitem)
#                         index_delta += 1
#                     item.getparent().remove(item)
#     return content

def expand(content):
    expaned_tags = ['div', 'section', 'span']
    check_inline_blocks = lambda item: any(filter(lambda subitem: subitem.tag in ['div', 'section', 'span'], item.getiterator()))
    for item in content.getchildren():
        tag = item.tag
        if tag in expaned_tags:
            if check_inline_blocks(item):
                index = content.index(item)
                index_delta = 1
                for subitem in item:
                    if check_inline_blocks(subitem):
                        subitem = expand(subitem)
                    content.insert(index+index_delta, subitem)
                    index_delta += 1
            item.getparent().remove(item)


# for item in content.getiterator():
#     print(lxml.html.tostring(item))
print(lxml.html.tostring(expand(content)))

# import lxml.html.clean
# content_filter = lxml.html.clean.Cleaner(scripts=True, javascript=True, comments=True, style=True, inline_style=True, links=True, meta=True, page_structure=True, processing_instructions=True, embedded=True, frames=True, forms=True, annoying_tags=[], remove_tags=[], kill_tags=[], allow_tags=['a'], remove_unknown_tags=False, safe_attrs_only=True, safe_attrs=['href'], add_nofollow=False, host_whitelist=[], whitelist_tags=[])
# text = content_filter.clean_html('text')
#
# # DEMO TEST BEGIN
#
# myiter = iter([1, 2, 3, 4, 5])
# for x in myiter:
#     print(x)
#     print(dir(myiter))
#     next(myiter)

# from html.parser import HTMLParser
#
# class MyHTMLParser(HTMLParser):
#     def handle_starttag(self, tag, attrs):
#         print("Encountered a start tag:", tag)
#
#     def handle_endtag(self, tag):
#         print("Encountered an end tag :", tag)
#
#     def handle_data(self, data):
#         print("Encountered some data  :", data)
#
# parser = MyHTMLParser()
# parser.feed('<html><head><title>Test</title></head>'
#             '<body><h1>Parse me!</h1></body></html>')

# terms_required ='''
# '''
# terms_removed ='''
# '''
# terms_negatives ='''
# '''
# terms_positives ='''
# '''
#
# items = ['term A1', 'term B1', 'term B2', 'A1', 'term C3', 'term D1', 'term D3']
#
# def sample(items, terms_required, terms_removed, terms_negatives, terms_positives):
#     items_filter_all = lambda items, terms: set(filter(lambda item: item if all(set(map(lambda term: (term in item or term.replace(' ', '_') in item), terms))) else None, items))
#     items_filter_any = lambda items, terms: set(filter(lambda item: item if any(set(map(lambda term: (term in item or term.replace(' ', '_') in item), terms))) else None, items))
#     terms_filter     = lambda terms: set(filter(None, terms.split('\n'))) if len(set(filter(None, terms.split('\n')))) != 0 else {}
#     terms_required   = terms_filter(terms_required); terms_removed = terms_filter(terms_removed); terms_negatives = terms_filter(terms_negatives); terms_positives = terms_filter(terms_positives)
#     items_required   = items_filter_any(items, terms_required) if len(terms_required) > 0 else set(items)
#     items_removed    = items_filter_any(items, terms_removed)
#     items_negatives  = items_filter_any(items, terms_negatives)
#     items_positives  = items_filter_any(items, terms_positives)
#     items_result     = (items_required - items_removed) - (items_negatives - items_positives)
#     print(f'''\n{80*"-"}
#     items:\n{items}\n
#     required: {terms_required} =>\n{items_required}\n
#     removed: {terms_removed} =>\n{items_removed}\n
#     negatives: {terms_negatives} =>\n{items_negatives}\n
#     positives: {terms_positives} =>\n{items_positives}\n
#     result:\n{items_result}\n
#     {80*"-"}\n''')
#     return items_result
#
# print(sample(items, terms_required, terms_removed, terms_negatives, terms_positives))


# from urllib.parse import unquote, urljoin, urlsplit, urlunsplit, SplitResult
#
# summaries = [
# '',
# 'The Elder Scrolls III: Morrowind — компьютерная игра в жанре Action RPG, выпущенная Bethesda Softworks.',
# '',
# 'The Elder Scrolls Online — компьютерная игра в жанре MMORPG, выпущенная Bethesda Softworks.',
# 'Bethesda Softworks LLC — частная компания ... разработчик серии ролевых игр The Elder Scrolls, ... РПГ Fallout 3 ... The Elder Scrolls: Arena (1994), The Elder Scrolls II: Daggerfall (1996), An Elder Scrolls Legend: Battlespire (1997), The Elder Scrolls Adventures: Redguard (1998), The Elder Scrolls III: Morrowind (2002), The Elder Scrolls III: Tribunal (2003), The Elder Scrolls III: Bloodmoon (2003), The Elder Scrolls Travels: Stormhold (2003), The Elder Scrolls Travels: Shadowkey (2004), The Elder Scrolls Travels: Dawnstar (2004), The Elder Scrolls IV: Oblivion (2006), The Elder Scrolls IV: Knights of the Nine (2006), The Elder Scrolls IV: Shivering Isles (2007), The Elder Scrolls V: Skyrim (2011), The Elder Scrolls V: Dawnguard (2012), The Elder Scrolls V: Hearthfire (2012), The Elder Scrolls V: Dragonborn (2013)',
# 'Bethesda Softworks — американский издатель компьютерных игр. ... третья глава в истории The Elder Scrolls, Morrowind, ... началась разработка The Elder Scrolls IV: Oblivion. Игра была выпущена в марте 2006 года и повторила успех Morrowind ... права на серию Fallout ... первая игра в приобретенной франшизе — Fallout 3 ... очередная игра серии Fallout: New Vegas ... продолжения серий The Elder Scrolls и Fallout.',
# 'Эбонитовый Клинок (ориг. Ebony Blade) — меч, двуручный меч, даэдрический артефакт. Присутствует в нескольких играх серии The Elder Scrolls.',
# 'Бтанченд (ориг. Bthanchend) — двемерские руины в игре The Elder Scrolls III: Morrowind.',
# 'Эта страница содержит перечень квестов из игры The Elder Scrolls III: Morrowind.',
# 'Если вы попали сюда из другой статьи The Elder Scrolls Wiki, пожалуйста, вернитесь и исправьте ссылку так, чтобы она указывала на конкретную статью. Алхимия (Morrowind) — статья о навыке в игре The Elder Scrolls III: Morrowind; Алхимия (Oblivion) — статья о навыке в игре The Elder Scrolls IV: Oblivion; Алхимия (Skyrim) — статья о навыке в игре The Elder Scrolls V: Skyrim; Алхимия (Online) — статья о профессии в игре The Elder Scrolls Online; Алхимия (персонаж) — статья о персонаже в игре The Elder Scrolls Online: Summerset. Алхимия (карта) — статья о карте в игре The Elder Scrolls: Legends.',
# 'Алхимия (ориг. Alchemy) — один из навыков группы мага в игре The Elder Scrolls III: Morrowind. Навык зависит от характеристики «Интеллект».',
# 'Алхимия (ориг. Alchemy) — навык из игры The Elder Scrolls V: Skyrim, особо полезный ворам. Алхимики создают различные полезные и ядовитые зелья. Способы изготовления большинства из них являются тайными или и вовсе утерянными, но некоторые из них описаны в рецептах, встречающихся в продаже и во время исследования мира. На рост этого навыка влияет прикосновение к Камням Вора и Любовника.',
# 'Alchemy is the process of combining ingredients into potions or poisons. In most TES titles, alchemy is also a skill that determines the potency of the created potions and poisons.',
# 'Alchemy is a magic specialization skill that appears in The Elder Scrolls III: Morrowind. The Alchemy discipline is the mastery of crafting potions from mundane substances, with intelligence being its governing attribute.',
# 'Alchemy is a skill in The Elder Scrolls V: Skyrim and is one of the six skills that falls under The Thief play-style. Alchemy is the art of combining raw ingredients with matching effects to produce potions and poison. It is one of the three crafting skills in Skyrim, together with Smithing and Enchanting. It is affected by The Thief Stone and, as with all skills, by The Lover Stone.',
# ]
#
# links = [
# 'https://elderscrolls.fandom.com/ru/wiki/Portal/The_Elder_Scrolls_III:_Morrowind',
# 'https://elderscrolls.fandom.com/ru/wiki/The_Elder_Scrolls_III:_Morrowind',
# '/ru/wiki/Главный_квест_(Morrowind)',
# 'https://elderscrolls.fandom.com/ru/wiki/The_Elder_Scrolls_Online',
# 'https://elderscrolls.fandom.com/ru/wiki/Bethesda_Game_Studios',
# 'https://ru.wikipedia.org/wiki/Bethesda_Softworks',
# 'https://elderscrolls.fandom.com/ru/wiki/Эбонитовый_Клинок',
# 'https://elderscrolls.fandom.com/ru/wiki/Бтанченд',
# 'https://elderscrolls.fandom.com/ru/wiki/Квесты_(Morrowind)',
# 'https://elderscrolls.fandom.com/ru/wiki/Алхимия',
# 'https://elderscrolls.fandom.com/ru/wiki/Обсуждение:Алхимия',
# 'https://elderscrolls.fandom.com/ru/wiki/Алхимия_(Morrowind)',
# 'https://elderscrolls.fandom.com/ru/wiki/Алхимия_(Skyrim)',
# 'https://elderscrolls.fandom.com/wiki/Alchemy',
# 'https://elderscrolls.fandom.com/wiki/Alchemy_(Morrowind)',
# 'https://elderscrolls.fandom.com/wiki/Alchemy_(Skyrim)',
# ]
#
# items = links
# required = links_required
# removed = links_removed
# negatives = links_negatives
# positives = links_positives
#
# # items = summaries
# # required = summary_required
# # removed = summary_removed
# # negatives = summary_negatives
# # positives = summary_positives
#
# delim = f'{80*"-"}'
# print(delim)
# print(f'SOURCE: {len(items)}')
# items_index_table = dict()
# index = 0
# print(delim)
# for item in items:
#     index += 1
#     print(f'#{index:<2} {item:>3}\n')
#     items_index_table[item] = index
# print(delim)
# result = sample(items, required, removed, negatives, positives)
# # result.sort(key=lambda f: int(''.join(filter(str.isdigit, f)) or -1))
# print(f'DESTINATION: {len(result)}')
# index = 0
# print(delim)
# for item in result:
#     index += 1
#     print(f'#{items_index_table[item]:<2} {item:>3}\n')
# print(delim)

# DEMO TEST END

# def test(page_file='test.html'):
#     if not os.path.isfile(page_file):
#         print(f'test file is missing: expected {page_file} in {os.getcwd()}')
#         return
#     source = page_to_source(page_file, page_block, meta_block, title_block, summary_block, content_block, cut_blocks)
#     page, meta, title, summary, content = source
#     delim_single = 80*'-' + '\n'
#     delim_double = 80*'=' + '\n'
#     print(f'{delim_double}meta\n{delim_double}{text_extract(meta)}\n')
#     print(f'{delim_double}title\n{delim_double}{text_extract(title)}\n')
#     print(f'{delim_double}summary\n{delim_double}{text_extract(summary)}\n')
#     print(f'{delim_double}content\n{delim_double}{text_extract(content)[:2048]}\n')
#     print(f'{delim_double}page\n{delim_double}{text_extract(page)[:2048]}\n')
#     print(f'{delim_double}')
#     for instance in page.getiterator():
#         if isinstance(instance, lxml.html.HtmlComment):
#             instance.getparent().remove(instance)
#     links = sorted(source_links(content, netloc, links_required, links_removed, links_negatives, links_positives))
#     print(f'{delim_double}page_links_page\n{delim_double}')
#     list(map(lambda link: print(link), links))
#     print(f'{delim_double}')
#     if meta is not None and not len(sample([text_extract(meta)], meta_required, meta_removed, meta_negatives, meta_positives)):
#         print(f'{page_file} does not match meta => passed')
#         return
#     elif title is not None and not len(sample([text_extract(title)], title_required, title_removed, title_negatives, title_positives)):
#         print(f'{page_file} does not match title => passed')
#         return
#     elif summary is not None and not len(sample([text_extract(summary)], summary_required, summary_removed, summary_negatives, summary_positives)):
#         print(f'{page_file} does not match summary => passed')
#         return
#     elif content is not None and not len(sample([text_extract(content)], content_required, content_removed, content_negatives, content_positives)):
#         print(f'{page_file} does not match content => passed')
#         return
#     else:
#         print(f'{page_file} matched => OK!')
#     html = transform(page, meta, title, summary, content)
#     file = 'result.html'
#     with codecs.open(file, 'w', 'utf-8') as f:
#         f.write(html)
#     print(f'{delim_double}html (transformed)\n{delim_double}{html}\n')
#     print(f'{delim_single}')
#     print(f'{page_file} => {file}')
#

# test()
