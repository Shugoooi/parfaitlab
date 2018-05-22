#/usr/bin/python
# -*- coding:utf-8 -*-

"""
自動化された目次生成器
"""
filename = 'resources/test.md'

# MD読み込み
doc = open(filename, 'rt', encoding='utf-8')
doc.seek(0)
lines = doc.readlines()

# MDを目次以前と目次以降に分離
before = lines[:lines.index('## 目次\n')+1]
lines = lines[lines.index('## 目次\n')+1:] # 目次以降を対象に目次生成
if lines[1] is not '\n' : # 既に目次が生成されている、あるいは予期せぬエラー
	raise Exception

# 仕様に従って目次を生成
contents = filter(lambda x: x.startswith('### ')|x.startswith('## '), lines)
contents = map(lambda x: x.replace('### ', '\t* '), contents)
contents = map(lambda x: x.replace('## ', '0. '), contents)
contents = list(contents)
doc.close()

# 書き込み
doc = open(filename, 'wt', encoding='utf-8')
doc.writelines(before)
doc.writelines(contents)
doc.writelines(lines)
doc.close()
