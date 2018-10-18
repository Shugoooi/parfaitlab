# /usr/bin/python
# -*- coding:utf-8 -*-

"""
自動化された目次生成器
"""
filename = 'resources/test.md'

# MD読み込み
with open(filename, 'r', encoding='utf-8') as md:
    lines = md.readlines()

# MDを目次以前と目次以降に分離
index = lines.index('## 目次\n')+1
if lines[index] != '\n':  # 既に目次が生成されている、あるいは予期せぬエラー
    raise Exception("目次生成済、あるいは目次と次のコンテンツの間に空行を入れてください")

# 仕様に従って目次を生成
contents = (x for x in lines[index:] if x.startswith('### ') or x.startswith('## '))
contents = (x.replace('### ', '\t* ') for x in contents)
contents = [x.replace('## ', '0. ') for x in contents]
contents.append('\n')
lines[index] = ''.join(contents)

# 書き込み
with open('resources/output.md', 'w', encoding='utf-8') as md:
    md.writelines(lines)
