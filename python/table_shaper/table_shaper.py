#/usr/bin/python
# -*- coding:utf-8 -*-

import unicodedata

'''
MDファイルにおけるテーブルの整形器
'''

def shape_table(table):
	'''
	テーブルを整形する
	テーブルは文字列のリストである
	'''
	table = [s.strip() for s in table]
	columns = table[0].count('|') + 1
	table = [t.split("|") for t in table]
	table = shape_table2(table)
	table = [('| ').join(s) for s in table]
	table = [s+'\n' for s in table]
	return table

def shape_table2(table, list=[]):
	'''
	テーブルを整形する再帰関数
	'''
	if table[0] == []:
		return list
	else:
		list.append(insert_tab([t.pop(0) for t in table]))
		return shape_table2(table, list)

def get_text_width(text):
	'''
	textが半角何文字分か数える
	'''
	count = 0
	for c in text:
		if unicodedata.east_asian_width(c) in 'FWA':
			count += 2
		else:
			count += 1
	return count

def insert_tab(text_list):
	'''
	テーブルを整形するタブを挿入する
	'''
	max_text_width = max([get_text_width(s) for s in text_list])
	tab_count = [max_text_width // 4 - get_text_width(s) // 4 + 1 for s in text_list] # 必要なタブの数を計算
	return [text + '\t'*tab for text, tab in zip(text_list, tab_count)]


# ファイル名定義
filename = 'resources/test.md'

# MD読み込んで行毎のリストを生成
md = open(filename, 'rt', encoding='utf-8')
md.seek(0)
lines = md.readlines()

# 全テーブルの位置をダブルで取得
table_signs = filter(lambda x: ('---' in x)and('|' in x), lines) # テーブル2行目検出
table_index = [lines.index(i) for i in table_signs]
table_start = [i-1 for i in table_index]
table_end = [lines.index('\n', i)-1 for i in table_index]
table_index = list(zip(table_start, table_end))

# テーブルの整形、移し替え
table_lines = [lines[i[0]: i[1]] for i in table_index]
shaped_table = [shape_table(s) for s in table_lines]
print(list(shaped_table))
print(list(table_index))
for (table, index) in zip(shaped_table, table_index):
	print(table)
	print(index)
	lines = lines[:index[0]] + table + lines[index[1]+1:]
md.close()

md = open(filename, 'wt', encoding='utf-8')
md.writelines(lines)
md.close()
