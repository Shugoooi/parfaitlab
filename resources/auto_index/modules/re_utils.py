#! /usr/bin/python
#-*- coding: utf-8 -*-

import re

# Global Patterns 
alphabets = re.compile("[a-zA-Z]+")
alnum = re.compile("[a-zA-Z0-9]+")
rulename = re.compile("[a-zA-Z0-9_]+")
printable = re.compile("\S+")
includeBR = re.compile("^\S[\S\ ]*$")
except_nl = re.compile("[^\\n]+")
post_marked = re.compile("〒[0-9]+[-][0-9]+")
all = re.compile('.*')

dummy = re.compile("")
compiled_reClass = dummy.__class__

def is_json(text):
    """ JSONか判定 """
    return text.startswith("{") and text.endswith("}")

def is_compiled_regExpr(obj):
	""" コンパイル済み正規表現オブジェクトであるか否か """
	return isinstance(obj,compiled_reClass)
	
def match_in(text,reList):
    """ テキストとreのリストをとってまっちんぐ """
    return any( pattern.match(text) for pattern in reList )
    
def search_in(text,reList):
    """ テキストとreのリストをとってまっちんぐ """
    for pattern in reList :
        match = pattern.search(text)
        if match :
            return match

def slice_max(text,max_):
    """ 最大長を指定してそれ以上ならスライシングして返す """
    if not text or len(text) <= max_ :
        return text
    else :
        return text[:max_-3] +"..."

def remove_quote(src):
    """ クオートをはずす """
    if src.startswith("'") and src.endswith("'") :
        return src[1:-1] 
    elif src.startswith('"') and src.endswith('"') :
        return src[1:-1] 
    else :
        return src

encodeList = ('utf-8', 'shift-jis', 'euc-jp', 'x-mac-japanese', 'latin-1', 'shift-jis-2004', 'shift-jisx0213',
            'iso2022jp', 'iso2022-jp-1', 'iso2022-jp-2', 'iso2022-jp-3',
            'iso2022-jp-ext','ascii')

def decode_anyway(text):
    """
    むりくりデコードする
    """
    for enc in encodeList :
        try :
            unicodeObj = text.decode(enc)
            return unicodeObj
        except :
            pass # 例外もみ消し

    else :
        raise LookupError("デコードに失敗しました")

def convert_anyway(text,encoding="utf-8"):
    """ 無理くりもじこーど変換する """
    return decode_anyway(text).encode(encoding)






