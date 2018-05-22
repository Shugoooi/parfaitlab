#/usr/bin/python
# -*- coding:utf-8 -*-

```
MDファイルにおけるテーブルの整形器
```
filename = 'resources/test.md'

md = open('filename', 'rt')
md.seek()
lines = md.readlines()

# 全テーブルの位置をレンジで取得
table_signs = filter(lambda x: ('---' in x)and('|' in x), lines)
table_signs = map(lambda x: lines.index(x), table_signs)
table_signs = map(lambda x: lines[x-1, lines.index('\n', x)-1], table_signs)
shaped_table = map(shape_table, table_signs)
tables = list(table_signs)

def shape_table(table):
	'''
	テーブルを整形する
	テーブルは文字列のリストである
	'''
	table = list(map(strip, table))
	columns = table[0].count('|') + 1
	table = [t.split("|") for t in table]
	table = shape_table2(table, [])
	table = [('| ').join(s) for s in table]
	return table

def shape_table2(table, list):
	'''
	'''
	if table[0] is []:
		return list
	else:
		list.append(insert_tab([t.pop(0) for t in table]))
		shape_table2(table, list)

def get_text_width(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count

def insert_tab(text_list):
	max_text_width = max([get_text_width(s) for s in text_list])
	tab_count = [max_text_width // 4 - get_text_width(s) // 4 + 1 for s in text_list] # 必要なタブの数を計算
	return [text + '\t'*tab for text, tab in zip(text_list, tab_count)]
