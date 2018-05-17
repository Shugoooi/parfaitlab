#! /usr/bin/python
#-*- coding: utf-8 -*-


import os
import types
import imp
import json


"""
テキストファイルを扱うための様々なユーティリティを規定する
"""
def find_sourceCode(filepathOrModule) :
    """
    定義された名前に対応するPythonソースコードを見つける関数
    名前にはファイルパスのほか、任意のモジュールオブジェクトないし、インポート可能なモジュール名をとり得る

    見つけられたファイルパスを表す文字列をリターンする
    """
    # モジュール名として読み込み可能か
    try :
        if isinstance(filepathOrModule,str) :
            fileObj = imp.find_module(filepathOrModule)[0]
            return fileObj.name
    except ImportError :
        pass

    # ファイル名が定義されたら読み込み可能か確認
    if isinstance(filepathOrModule,str):
        if not filepathOrModule.endswith(".py") :
            raise Exception("引数参照先 %s がpyファイルでありません" % (filepathOrModule))
        elif not os.path.isfile(filepathOrModule) :
            raise Exception("ファイル %s が存在しません" % (filepathOrModule) )
        # エラーチェックのパス
        else :
            return filepathOrModule

    # モジュールが定義されたら読み込み先ファイル名を参照してそのファイルパスをコンテキストに自己再起呼び出し
    elif type(filepathOrModule) is types.ModuleType :
        module_loadedfile = filepathOrModule.__file__
        if module_loadedfile.endswith(".py") :
            return find_sourceCode(module_loadedfile)
        elif module_loadedfile.endswith(".pyc") :
            return find_sourceCode(module_loadedfile[:-1])
        else :
            message = "予期せぬ形式のファイル名を読み込み対象にもつモジュールオブジェクト %s が引数に定義されました" % (filepathOrModule,)
            raise NotImplementedError(message)
    else :
        raise TypeError("定義された %s はpythonソースのファイルパスでもモジュールオブジェクトでもありません") % (filepathOrModule,)


def count_lineno(filePath):
    """ 定義されたファイルの行数を数える """
    if not os.path.isfile(filePath) :
        raise Exception("ファイル %s は存在しません" % filePath)
    with open(filePath) as f :
        return sum ( 1 for line in f.readlines() )

fileNames = []
def write2(file_orname,string,mode="w"):
    """ ファイル名乃至ファイルオブジェクトを取って、ライティングする"""
    # もしモードがa++なら初期化
    if mode == "a++" :
        if file_orname not in fileNames :
            fileNames.append(file_orname) # 初期化終了保存
            with open(file_orname,"w") as f :
                f.write("")
        mode = "a"

    # Nullなら標準出力
    if file_orname is None :
        print string

    # ファイルオブジェクトと同定
    elif hasattr(file_orname,"write") :
        file_orname.write(string)

    # ファイル名と同定
    else :
        with open(file_orname,mode) as f :
            f.write(string)

def write_asJSON(file_orname,data):
    """ json化して吐く"""
    json_str = json.dumps(data)
    write2(file_orname,json_str)
        
def check_file(fileName):
    """ ファイルチェックを行う """
    if not os.path.isfile(fileName) :
        raise IOError("ファイル '%s' は存在しません" % (fileName,))

def check_dir(dirname):
    """ 抑止的ディレクトリチェック """
    if not os.path.isdir(dirname):
        raise IOError("パス %s はディレクトリではありません" % (dirname))

def find_file_recursively(dirName):
    """ ファイルを再起検索するジェネレータ"""
    for root, dirs, files in os.walk(dirName):
        for f_name in files:
            yield os.path.join(root, f_name)

def find_dirs_recursively(from_):
    """ ディレクトリを再起検索するジェネレータ"""
    for root, dirs, files in os.walk(from_):
        for dir_name in dirs :
            yield os.path.join(root, dir_name) 

def get_relPath(after):
    """ モジュール基点相対パスを返す """
    base = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(base,after)




