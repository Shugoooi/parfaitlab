#/usr/bin/python
# -*- coding: utf-8 -*-

"""
自動化された目次生成器
"""
filename = 'resources/test.md'

doc = open(filename, 'rt')
lines = doc.readlines().decode('cp932')
lines = lines[lines.index('## 目次')+1:]
contents = filter(lambda x: x.findall('## ', '### '), lines)
contents = map(lambda x: x.replace('### ', '\t* '), contents)
contents = map(lambda x: x.replace('## ', '0. '), contents)
doc.close()

doc = open(filename, 'at')
doc.seek(doc.find('## 目次'))
doc.writelines(contents)
doc.close()
